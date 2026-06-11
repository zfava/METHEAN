"""Failed-payment recovery (dunning) state machine, migration 059.

Stripe stays authoritative for payment facts; dunning_state is
METHEAN's derived policy walk: none -> grace (day 0, full access) ->
restricted (day 7, paid routes paused, data stays reachable) ->
canceled (day 21, subscription canceled at Stripe). Any successful
payment resets the walk wherever it was. These tests pin:

1. Webhook entry and reset transitions, replay-safe.
2. The daily task's thresholds (day 6 no-op, day 8 restrict, day 22
   cancel) with time frozen by explicit ``now`` injection.
3. The 24h email throttle: transitions are never delayed by it, and a
   deferred email is sent on the next run, never lost or doubled.
4. The access matrix: grace passes the subscription gate; restricted
   and canceled are blocked on paid routes but keep the
   data-stewardship carve-outs (family record read, sealed export,
   prior exports) and household deletion.
5. The status endpoint surfaces the state and its dates.
6. The complete walk (none -> grace -> restricted -> canceled ->
   recovered) as one integration test.
"""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import func, select

from app.models.governance import GovernanceEvent
from app.models.identity import Household
from app.services.billing import (
    advance_dunning,
    advance_dunning_for_household,
    reset_dunning,
    start_dunning,
)

T0 = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


async def _dunning_household(db_session, household, user, state="none", started=None, emails=0):
    """Put the standard fixture household into a known dunning position.

    The fixture household is trialing; dunning only matters once the
    trial pass-through is gone, so the trial window is cleared and the
    Stripe linkage the webhooks key on is attached.
    """
    household.subscription_status = "past_due"
    household.trial_ends_at = None
    household.stripe_customer_id = "cus_dunning_test"
    household.dunning_state = state
    household.dunning_started_at = started
    household.dunning_emails_sent = emails
    household.last_dunning_email_at = started if emails else None
    await db_session.flush()
    return household


async def _event_count(db_session, household_id, target_type) -> int:
    return (
        await db_session.scalar(
            select(func.count())
            .select_from(GovernanceEvent)
            .where(
                GovernanceEvent.household_id == household_id,
                GovernanceEvent.target_type == target_type,
            )
        )
    ) or 0


def _webhook_event(event_type: str, customer: str = "cus_dunning_test"):
    obj = MagicMock()
    obj.customer = customer
    obj.id = "sub_dunning"
    obj.status = "active"
    obj.trial_end = None
    obj.current_period_end = None
    obj.metadata = {}
    event = MagicMock()
    event.type = event_type
    event.data.object = obj
    return event


async def _fire_webhook(db_session, event):
    from app.services.billing import handle_webhook

    with patch("app.services.billing.settings") as mock_settings, patch(
        "app.services.billing.stripe"
    ) as mock_stripe:
        mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
        mock_settings.STRIPE_SECRET_KEY = "sk_test"
        mock_settings.APP_URL = "https://methean.app"
        mock_stripe.Webhook.construct_event.return_value = event
        return await handle_webhook(b"payload", "sig", db_session)


# ── Webhook transitions ────────────────────────────────────────────────────


class TestWebhookTransitions:
    @pytest.mark.asyncio
    async def test_payment_failed_enters_grace_sends_email_logs_event(
        self, db_session, household, user
    ):
        hh = await _dunning_household(db_session, household, user)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            await _fire_webhook(db_session, _webhook_event("invoice.payment_failed"))

        assert hh.dunning_state == "grace"
        assert hh.dunning_started_at is not None
        assert hh.dunning_emails_sent == 1
        assert hh.last_dunning_email_at is not None
        assert mock_send.await_count == 1
        to, subject, html = mock_send.await_args.args[:3]
        assert to == user.email
        assert "didn't go through" in subject
        assert "Update Payment Method" in html
        assert await _event_count(db_session, hh.id, "billing_dunning_started") == 1

    @pytest.mark.asyncio
    async def test_replayed_payment_failed_does_not_double_send_or_log(
        self, db_session, household, user
    ):
        hh = await _dunning_household(db_session, household, user)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            await _fire_webhook(db_session, _webhook_event("invoice.payment_failed"))
            await _fire_webhook(db_session, _webhook_event("invoice.payment_failed"))

        assert hh.dunning_state == "grace"
        assert hh.dunning_emails_sent == 1
        assert mock_send.await_count == 1
        assert await _event_count(db_session, hh.id, "billing_dunning_started") == 1

    @pytest.mark.asyncio
    async def test_payment_succeeded_resets_from_grace(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            await _fire_webhook(db_session, _webhook_event("invoice.payment_succeeded"))

        assert hh.dunning_state == "none"
        assert hh.dunning_started_at is None
        assert hh.last_dunning_email_at is None
        assert hh.dunning_emails_sent == 0
        # Recovery is silent: the banner disappearing is the confirmation.
        assert mock_send.await_count == 0
        assert await _event_count(db_session, hh.id, "billing_dunning_recovered") == 1

    @pytest.mark.asyncio
    async def test_subscription_updated_active_resets_from_restricted(
        self, db_session, household, user
    ):
        hh = await _dunning_household(
            db_session, household, user, state="restricted", started=T0, emails=2
        )
        await _fire_webhook(db_session, _webhook_event("customer.subscription.updated"))

        assert hh.dunning_state == "none"
        assert hh.subscription_status == "active"
        assert hh.dunning_emails_sent == 0
        assert await _event_count(db_session, hh.id, "billing_dunning_recovered") == 1

    @pytest.mark.asyncio
    async def test_checkout_completed_resets_dunning(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        event = _webhook_event("checkout.session.completed")
        event.data.object.metadata = {"household_id": str(hh.id)}
        event.data.object.subscription = "sub_new"
        await _fire_webhook(db_session, event)

        assert hh.dunning_state == "none"
        assert hh.subscription_status == "active"
        assert await _event_count(db_session, hh.id, "billing_dunning_recovered") == 1

    @pytest.mark.asyncio
    async def test_subscription_deleted_mid_dunning_lands_canceled_silently(
        self, db_session, household, user
    ):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        event = _webhook_event("customer.subscription.deleted")
        event.data.object.status = "canceled"
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            await _fire_webhook(db_session, event)

        assert hh.dunning_state == "canceled"
        assert hh.subscription_status == "canceled"
        assert mock_send.await_count == 0


# ── Daily task thresholds, throttle, idempotency ──────────────────────────


class TestDailyAdvance:
    @pytest.mark.asyncio
    async def test_day_6_is_a_noop(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            state = await advance_dunning_for_household(db_session, hh, now=T0 + timedelta(days=6))

        assert state == "grace"
        assert hh.dunning_emails_sent == 1
        assert mock_send.await_count == 0
        assert await _event_count(db_session, hh.id, "billing_dunning_advanced") == 0

    @pytest.mark.asyncio
    async def test_day_8_enters_restricted_with_email(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            state = await advance_dunning_for_household(db_session, hh, now=T0 + timedelta(days=8))

        assert state == "restricted"
        assert hh.dunning_emails_sent == 2
        assert mock_send.await_count == 1
        subject = mock_send.await_args.args[1]
        assert "paused" in subject
        assert await _event_count(db_session, hh.id, "billing_dunning_advanced") == 1

    @pytest.mark.asyncio
    async def test_day_22_cancels_at_stripe_and_sends_final_email(
        self, db_session, household, user
    ):
        hh = await _dunning_household(
            db_session, household, user, state="restricted", started=T0, emails=2
        )
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send, patch(
            "app.services.billing.settings"
        ) as mock_settings, patch("app.services.billing.stripe") as mock_stripe:
            mock_settings.STRIPE_SECRET_KEY = "sk_test"
            mock_settings.APP_URL = "https://methean.app"
            sub = MagicMock()
            sub.id = "sub_to_cancel"
            mock_stripe.Subscription.list.return_value = MagicMock(data=[sub])

            state = await advance_dunning_for_household(db_session, hh, now=T0 + timedelta(days=22))

            mock_stripe.Subscription.cancel.assert_called_once_with("sub_to_cancel")

        assert state == "canceled"
        assert hh.subscription_status == "canceled"
        assert hh.dunning_emails_sent == 3
        assert mock_send.await_count == 1
        subject, html = mock_send.await_args.args[1:3]
        assert "canceled" in subject
        assert "remains intact" in html
        assert "Reactivate" in html
        assert await _event_count(db_session, hh.id, "billing_dunning_advanced") == 1

    @pytest.mark.asyncio
    async def test_email_throttle_defers_but_never_delays_the_transition(
        self, db_session, household, user
    ):
        """Grace email went out an hour before the day-7 threshold: the
        restriction applies on time, the email waits for the throttle.
        """
        day7 = T0 + timedelta(days=7, hours=1)
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        hh.last_dunning_email_at = day7 - timedelta(hours=1)
        await db_session.flush()

        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            state = await advance_dunning_for_household(db_session, hh, now=day7)
            assert state == "restricted"
            assert mock_send.await_count == 0, "throttled: no second email inside 24h"
            assert hh.dunning_emails_sent == 1

            # Next daily run, throttle clear: the deferred email goes out.
            await advance_dunning_for_household(db_session, hh, now=day7 + timedelta(days=1))
            assert mock_send.await_count == 1
            assert hh.dunning_emails_sent == 2

    @pytest.mark.asyncio
    async def test_task_rerun_changes_nothing(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        now = T0 + timedelta(days=8)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            await advance_dunning_for_household(db_session, hh, now=now)
            first = (hh.dunning_state, hh.dunning_emails_sent, hh.last_dunning_email_at)

            await advance_dunning_for_household(db_session, hh, now=now)
            second = (hh.dunning_state, hh.dunning_emails_sent, hh.last_dunning_email_at)

        assert first == second == ("restricted", 2, now)
        assert mock_send.await_count == 1
        assert await _event_count(db_session, hh.id, "billing_dunning_advanced") == 1

    @pytest.mark.asyncio
    async def test_sweep_ignores_households_not_in_the_walk(self, db_session, household, user):
        await _dunning_household(db_session, household, user, state="none")
        with patch("app.services.email.send_email", new_callable=AsyncMock):
            counts = await advance_dunning(db_session, now=T0 + timedelta(days=30))
        assert counts["checked"] == 0
        assert household.dunning_state == "none"

    @pytest.mark.asyncio
    async def test_skipped_state_sends_one_email_not_two(self, db_session, household, user):
        """A household first swept at day 22 walks grace -> restricted ->
        canceled in one run; it gets the final notice once, not a backlog.
        """
        hh = await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send, patch(
            "app.services.billing.settings"
        ) as mock_settings, patch("app.services.billing.stripe") as mock_stripe:
            mock_settings.STRIPE_SECRET_KEY = "sk_test"
            mock_settings.APP_URL = "https://methean.app"
            mock_stripe.Subscription.list.return_value = MagicMock(data=[])

            state = await advance_dunning_for_household(db_session, hh, now=T0 + timedelta(days=22))
            assert state == "canceled"
            assert mock_send.await_count == 1
            assert hh.dunning_emails_sent == 3

            await advance_dunning_for_household(db_session, hh, now=T0 + timedelta(days=23))
            assert mock_send.await_count == 1, "watermark reached; nothing more to send"


# ── Access matrix ──────────────────────────────────────────────────────────


PAID_ROUTE = "/api/v1/resources"
RECORD_READ = "/api/v1/children/{child_id}/family-record"
RECORD_EXPORT = "/api/v1/children/{child_id}/family-record/export"
EXPORTS_LIST = "/api/v1/family-record/exports"


class TestAccessMatrix:
    @pytest.mark.asyncio
    async def test_grace_passes_paid_route(self, auth_client, db_session, household, user):
        await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        resp = await auth_client.get(PAID_ROUTE)
        assert resp.status_code == 200, resp.text

    @pytest.mark.asyncio
    async def test_restricted_blocked_on_paid_route(self, auth_client, db_session, household, user):
        await _dunning_household(db_session, household, user, state="restricted", started=T0, emails=2)
        resp = await auth_client.get(PAID_ROUTE)
        assert resp.status_code == 402
        detail = resp.json()["detail"]
        assert detail["error"] == "subscription_required"
        assert detail["dunning_state"] == "restricted"

    @pytest.mark.asyncio
    async def test_restricted_keeps_family_record_read(
        self, auth_client, db_session, household, user, child
    ):
        await _dunning_household(db_session, household, user, state="restricted", started=T0, emails=2)
        resp = await auth_client.get(RECORD_READ.format(child_id=child.id))
        assert resp.status_code == 200, resp.text

    @pytest.mark.asyncio
    async def test_restricted_keeps_export_surfaces(
        self, auth_client, db_session, household, user, child
    ):
        await _dunning_household(db_session, household, user, state="restricted", started=T0, emails=2)
        listing = await auth_client.get(EXPORTS_LIST)
        assert listing.status_code == 200, listing.text
        # The export build touches object storage, which unit tests don't
        # run; the property under test is that the subscription gate
        # opens for it, so any outcome except 402 proves the carve-out.
        export = await auth_client.post(RECORD_EXPORT.format(child_id=child.id))
        assert export.status_code != 402, export.text

    @pytest.mark.asyncio
    async def test_restricted_keeps_household_deletion(
        self, auth_client, db_session, household, user
    ):
        await _dunning_household(db_session, household, user, state="restricted", started=T0, emails=2)
        status_resp = await auth_client.get("/api/v1/household/deletion-status")
        assert status_resp.status_code == 200, status_resp.text
        # The deletion route itself authenticates by password re-prompt;
        # a wrong password is 401/403/422, never the 402 paywall.
        delete_resp = await auth_client.request(
            "DELETE", "/api/v1/household", json={"password": "wrong"}
        )
        assert delete_resp.status_code != 402

    @pytest.mark.asyncio
    async def test_canceled_same_as_restricted(
        self, auth_client, db_session, household, user, child
    ):
        await _dunning_household(db_session, household, user, state="canceled", started=T0, emails=3)
        household.subscription_status = "canceled"
        await db_session.flush()

        blocked = await auth_client.get(PAID_ROUTE)
        assert blocked.status_code == 402
        assert blocked.json()["detail"]["dunning_state"] == "canceled"

        record = await auth_client.get(RECORD_READ.format(child_id=child.id))
        assert record.status_code == 200, record.text


# ── Status endpoint ────────────────────────────────────────────────────────


class TestStatusEndpoint:
    @pytest.mark.asyncio
    async def test_status_reflects_each_state_with_dates(
        self, auth_client, db_session, household, user
    ):
        # none
        resp = await auth_client.get("/api/v1/billing/status")
        body = resp.json()
        assert body["dunning_state"] == "none"
        assert body["dunning_grace_ends_at"] is None
        assert body["dunning_cancels_at"] is None
        assert body["update_payment_url"].endswith("/billing")

        # grace
        await _dunning_household(db_session, household, user, state="grace", started=T0, emails=1)
        body = (await auth_client.get("/api/v1/billing/status")).json()
        assert body["dunning_state"] == "grace"
        assert body["dunning_started_at"] == T0.isoformat()
        assert body["dunning_grace_ends_at"] == (T0 + timedelta(days=7)).isoformat()
        assert body["dunning_cancels_at"] == (T0 + timedelta(days=21)).isoformat()

        # restricted
        household.dunning_state = "restricted"
        await db_session.flush()
        body = (await auth_client.get("/api/v1/billing/status")).json()
        assert body["dunning_state"] == "restricted"
        assert body["dunning_cancels_at"] == (T0 + timedelta(days=21)).isoformat()

        # canceled
        household.dunning_state = "canceled"
        await db_session.flush()
        body = (await auth_client.get("/api/v1/billing/status")).json()
        assert body["dunning_state"] == "canceled"


# ── The complete walk ──────────────────────────────────────────────────────


class TestFullWalk:
    @pytest.mark.asyncio
    async def test_none_to_grace_to_restricted_to_canceled_to_recovered(
        self, db_session, household, user
    ):
        hh = await _dunning_household(db_session, household, user)

        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            # Day 0: the payment fails.
            await _fire_webhook(db_session, _webhook_event("invoice.payment_failed"))
            assert hh.dunning_state == "grace"
            assert mock_send.await_count == 1
            t0 = hh.dunning_started_at

            # Day 3: daily task runs, nothing changes.
            assert await advance_dunning_for_household(db_session, hh, now=t0 + timedelta(days=3)) == "grace"

            # Day 8: restriction.
            assert (
                await advance_dunning_for_household(db_session, hh, now=t0 + timedelta(days=8))
                == "restricted"
            )
            assert mock_send.await_count == 2

            # Day 22: cancellation at Stripe.
            with patch("app.services.billing.settings") as mock_settings, patch(
                "app.services.billing.stripe"
            ) as mock_stripe:
                mock_settings.STRIPE_SECRET_KEY = "sk_test"
                mock_settings.APP_URL = "https://methean.app"
                sub = MagicMock()
                sub.id = "sub_walk"
                mock_stripe.Subscription.list.return_value = MagicMock(data=[sub])
                assert (
                    await advance_dunning_for_household(db_session, hh, now=t0 + timedelta(days=22))
                    == "canceled"
                )
                mock_stripe.Subscription.cancel.assert_called_once()
            assert hh.subscription_status == "canceled"
            assert mock_send.await_count == 3

            # Reactivation: a successful payment resets everything.
            await _fire_webhook(db_session, _webhook_event("invoice.payment_succeeded"))
            assert hh.dunning_state == "none"
            assert hh.dunning_started_at is None
            assert hh.dunning_emails_sent == 0
            # Silent recovery: still exactly three dunning emails ever sent.
            assert mock_send.await_count == 3

        assert await _event_count(db_session, hh.id, "billing_dunning_started") == 1
        assert await _event_count(db_session, hh.id, "billing_dunning_advanced") == 2
        assert await _event_count(db_session, hh.id, "billing_dunning_recovered") == 1


# ── Direct service idempotency ─────────────────────────────────────────────


class TestServiceIdempotency:
    @pytest.mark.asyncio
    async def test_start_dunning_only_fires_from_none(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="restricted", started=T0, emails=2)
        with patch("app.services.email.send_email", new_callable=AsyncMock) as mock_send:
            assert await start_dunning(db_session, hh, now=T0 + timedelta(days=10)) is False
        assert hh.dunning_state == "restricted"
        assert mock_send.await_count == 0

    @pytest.mark.asyncio
    async def test_reset_dunning_noop_when_already_none(self, db_session, household, user):
        hh = await _dunning_household(db_session, household, user, state="none")
        assert await reset_dunning(db_session, hh) is False
        assert await _event_count(db_session, hh.id, "billing_dunning_recovered") == 0
