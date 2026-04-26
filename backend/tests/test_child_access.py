"""Per-child access enforcement tests (METHEAN-6-05).

Exercises ``require_child_access`` against three representative
routes — one read, one read with a sub-resource, and one write — and
covers every branch of the access matrix:

* owner: read + write any child in the household
* co_parent: read + write any child
* observer: read OK, write 403
* linked-learner user: own child OK, other child 403
* user from another household: 404 (no leak)

Plus the ``/children`` list endpoint filtering for linked learners.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password
from app.models.identity import Child, Household, User

# ══════════════════════════════════════════════════════════════════════
# Owner + co_parent: full access
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_owner_can_read_any_child_in_household(auth_client: AsyncClient, child: Child, second_child: Child):
    r1 = await auth_client.get(f"/api/v1/children/{child.id}/dashboard")
    r2 = await auth_client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert r1.status_code != 403, r1.text
    assert r2.status_code != 403, r2.text
    assert r1.status_code != 404, r1.text
    assert r2.status_code != 404, r2.text


@pytest.mark.asyncio
async def test_owner_can_write_any_child_in_household(auth_client: AsyncClient, child: Child, second_child: Child):
    """PUT /children/{id}/preferences is a representative write route."""
    r = await auth_client.put(
        f"/api/v1/children/{second_child.id}/preferences",
        json={"daily_duration_minutes": 60},
    )
    # Not 403/404; success or schema-level pushback both acceptable.
    assert r.status_code not in (403, 404), r.text


@pytest.mark.asyncio
async def test_co_parent_can_read_any_child(co_parent_client: AsyncClient, child: Child, second_child: Child):
    r1 = await co_parent_client.get(f"/api/v1/children/{child.id}/dashboard")
    r2 = await co_parent_client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert r1.status_code != 403, r1.text
    assert r2.status_code != 403, r2.text


@pytest.mark.asyncio
async def test_co_parent_can_write_any_child(co_parent_client: AsyncClient, child: Child):
    r = await co_parent_client.put(
        f"/api/v1/children/{child.id}/preferences",
        json={"daily_duration_minutes": 90},
    )
    assert r.status_code not in (403, 404), r.text


# ══════════════════════════════════════════════════════════════════════
# Observer: read OK, write 403
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_observer_can_read_any_child(observer_client: AsyncClient, child: Child):
    r = await observer_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert r.status_code != 403, r.text


@pytest.mark.asyncio
async def test_observer_cannot_write_any_child(observer_client: AsyncClient, child: Child):
    r = await observer_client.put(
        f"/api/v1/children/{child.id}/preferences",
        json={"daily_duration_minutes": 60},
    )
    assert r.status_code == 403, r.text
    assert "Observers cannot modify" in r.json().get("detail", "")


# ══════════════════════════════════════════════════════════════════════
# Linked-learner: only own child
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_self_learner_can_access_own_child(self_learner_client: AsyncClient, child: Child):
    r = await self_learner_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert r.status_code != 403, r.text


@pytest.mark.asyncio
async def test_self_learner_cannot_access_other_child(self_learner_client: AsyncClient, second_child: Child):
    r = await self_learner_client.get(f"/api/v1/children/{second_child.id}/dashboard")
    assert r.status_code == 403, r.text
    assert "Not authorized for this learner" in r.json().get("detail", "")


@pytest.mark.asyncio
async def test_list_children_filters_to_linked_child_for_self_learner(
    self_learner_client: AsyncClient, child: Child, second_child: Child
):
    r = await self_learner_client.get("/api/v1/children")
    assert r.status_code == 200, r.text
    items = r.json()
    ids = {item["id"] for item in items}
    assert str(child.id) in ids
    assert str(second_child.id) not in ids, "self-learner must not see siblings via /children"


# ══════════════════════════════════════════════════════════════════════
# Cross-household: 404 (do not leak existence)
# ══════════════════════════════════════════════════════════════════════


@pytest_asyncio.fixture
async def other_household_user(db_session: AsyncSession, client: AsyncClient) -> tuple[User, AsyncClient]:
    """A separate household + owner. Returns (user, authed client)."""
    other_hh = Household(name="Other Family", timezone="UTC")
    db_session.add(other_hh)
    await db_session.flush()
    other_user = User(
        household_id=other_hh.id,
        email="other-owner@test.local",
        password_hash=hash_password("xxxxxxxx"),
        display_name="Other Owner",
        role="owner",
    )
    db_session.add(other_user)
    await db_session.flush()
    token = create_access_token(other_user.id, other_hh.id, "owner")
    client.cookies.set("access_token", token)
    return other_user, client


@pytest.mark.asyncio
async def test_user_from_other_household_gets_404(other_household_user: tuple[User, AsyncClient], child: Child):
    """Reaching for a child in a household you don't belong to is a
    404 — the dep returns the same response it would for a missing id,
    so existence isn't leaked.
    """
    _, other_client = other_household_user
    r = await other_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert r.status_code == 404, r.text


# ══════════════════════════════════════════════════════════════════════
# Dependency return value
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_dependency_returns_child_object_to_route_handler(auth_client: AsyncClient, child: Child):
    """The factory-built dep returns a Child row. Smoke-test by hitting
    a route that goes through the dep and checking the response is
    well-formed — a misbehaving dep would 500 on the first attribute
    access.
    """
    r = await auth_client.get(f"/api/v1/children/{child.id}/dashboard")
    assert r.status_code == 200, r.text


# ══════════════════════════════════════════════════════════════════════
# Boundary guards on co_parent authority (paired with the write fix)
# ══════════════════════════════════════════════════════════════════════
#
# These three tests guard the upper edges of co_parent authority so a
# future "make co_parent more permissive" change can't silently leak
# household-deletion or billing-mutation rights.


@pytest.mark.skip(reason="endpoint not yet implemented in this build")
@pytest.mark.asyncio
async def test_co_parent_cannot_delete_household(co_parent_client: AsyncClient):
    """Co-parents must never be able to delete the household.

    Skipped: no DELETE /household endpoint exists today. Re-enable when
    the household-delete route lands so the boundary stays guarded.
    """
    r = await co_parent_client.delete("/api/v1/household")
    assert r.status_code == 403, r.text


@pytest.mark.asyncio
async def test_co_parent_cannot_change_billing(co_parent_client: AsyncClient):
    """Billing mutations are owner-only. A co_parent attempting to start
    a subscription must be rejected (403) — or 401 if the auth gate
    fires first, or 503 when Stripe isn't configured in the test
    environment. The point of the assertion is that the co_parent
    never gets a 200.
    """
    r = await co_parent_client.post("/api/v1/billing/subscribe", json={})
    assert r.status_code in (401, 403, 503), r.text
