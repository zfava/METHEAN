"""Personalization API.

Endpoints for the kid-driven personalization profile and the
household-level policy that gates it.

Validation order on writes:

1. Schema (Pydantic) enforces length and range.
2. ``_validate_against_library`` rejects unknown library IDs with 400.
3. ``_validate_against_policy`` rejects out-of-policy values with 403.
4. ``_validate_interest_tags`` enforces the policy's max-tags cap.

Steps 2 and 3 are intentionally distinct so the frontend can render
"this is a typo" vs "this is locked by your parent" differently.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_child_access
from app.content.personalization_library import (
    AFFIRMATION_TONES,
    ICONOGRAPHY_PACKS,
    INTEREST_TAGS,
    SOUND_PACKS,
    VIBES,
    VOICE_PERSONAS,
    expand_allowlist,
    get_affirmation_tone,
    get_iconography_pack,
    get_interest_tag,
    get_sound_pack,
    get_vibe,
    get_voice_persona,
)
from app.models.enums import GovernanceAction, UserRole
from app.models.identity import Child, ChildPreferences, PersonalizationPolicy, User
from app.schemas.personalization import (
    AffirmationToneEntry,
    ChildPersonalizationRead,
    ChildPersonalizationUpdate,
    IconographyPackEntry,
    InterestTagEntry,
    PersonalizationLibraryRead,
    PersonalizationPolicyRead,
    PersonalizationPolicyUpdate,
    SoundPackEntry,
    VibeEntry,
    VoicePersonaEntry,
)

router = APIRouter(tags=["personalization"])


# ── Defaults ──────────────────────────────────────────────────────


# Sane defaults for a child whose personalization JSONB is empty.
# These match what the onboarding flow will set the first time a kid
# answers the introduction questions; we apply them at the read path
# so a fresh row produces a renderable profile without writing.
_PROFILE_DEFAULTS: dict[str, object] = {
    "companion_name": "",
    "companion_voice": "",
    "vibe": "calm",
    "iconography_pack": "default",
    "sound_pack": "soft",
    "affirmation_tone": "warm",
    "onboarded": False,
}


_DEFAULT_POLICY_MAX_INTEREST_TAGS = 5


def _default_policy_read() -> "PersonalizationPolicyRead":
    """Policy values applied when no row exists for the household."""
    return PersonalizationPolicyRead(
        allowed_vibes=["*"],
        allowed_interest_tags=["*"],
        allowed_voice_personas=["*"],
        allowed_iconography_packs=["*"],
        allowed_sound_packs=["*"],
        allowed_affirmation_tones=["*"],
        companion_name_requires_review=False,
        max_interest_tags_per_child=_DEFAULT_POLICY_MAX_INTEREST_TAGS,
        voice_input_enabled=True,
        voice_minutes_daily_cap=60,
        whisper_provider="openai",
    )


# ── Library ID indexes (computed once at import) ──────────────────


_VIBE_IDS: list[str] = [v.id for v in VIBES]
_INTEREST_IDS: list[str] = [t.id for t in INTEREST_TAGS]
_VOICE_IDS: list[str] = [p.id for p in VOICE_PERSONAS]
_ICONOGRAPHY_IDS: list[str] = [p.id for p in ICONOGRAPHY_PACKS]
_SOUND_IDS: list[str] = [p.id for p in SOUND_PACKS]
_TONE_IDS: list[str] = [t.id for t in AFFIRMATION_TONES]


# ── Helpers ───────────────────────────────────────────────────────


async def _load_policy(db: AsyncSession, household_id: uuid.UUID) -> PersonalizationPolicy | None:
    result = await db.execute(select(PersonalizationPolicy).where(PersonalizationPolicy.household_id == household_id))
    return result.scalar_one_or_none()


def _policy_to_read(policy: PersonalizationPolicy | None) -> PersonalizationPolicyRead:
    if policy is None:
        return _default_policy_read()
    return PersonalizationPolicyRead(
        allowed_vibes=list(policy.allowed_vibes),
        allowed_interest_tags=list(policy.allowed_interest_tags),
        allowed_voice_personas=list(policy.allowed_voice_personas),
        allowed_iconography_packs=list(policy.allowed_iconography_packs),
        allowed_sound_packs=list(policy.allowed_sound_packs),
        allowed_affirmation_tones=list(policy.allowed_affirmation_tones),
        companion_name_requires_review=policy.companion_name_requires_review,
        max_interest_tags_per_child=policy.max_interest_tags_per_child,
        voice_input_enabled=policy.voice_input_enabled,
        voice_minutes_daily_cap=policy.voice_minutes_daily_cap,
        whisper_provider=policy.whisper_provider,  # type: ignore[arg-type]
    )


def _allowed_sets(policy: PersonalizationPolicyRead) -> dict[str, set[str]]:
    return {
        "vibes": expand_allowlist(policy.allowed_vibes, _VIBE_IDS),
        "interest_tags": expand_allowlist(policy.allowed_interest_tags, _INTEREST_IDS),
        "voice_personas": expand_allowlist(policy.allowed_voice_personas, _VOICE_IDS),
        "iconography_packs": expand_allowlist(policy.allowed_iconography_packs, _ICONOGRAPHY_IDS),
        "sound_packs": expand_allowlist(policy.allowed_sound_packs, _SOUND_IDS),
        "affirmation_tones": expand_allowlist(policy.allowed_affirmation_tones, _TONE_IDS),
    }


def _merge_profile(personalization: dict, interests: list[str] | None) -> dict[str, object]:
    """Apply defaults to a stored personalization blob."""
    out: dict[str, object] = dict(_PROFILE_DEFAULTS)
    out.update(personalization or {})
    # Strip pending-companion-name from the public profile; that's an
    # internal-only key for the review workflow.
    out.pop("companion_name_pending", None)
    out.pop("legacy_theme", None)
    out["interest_tags"] = list(interests or [])
    return out


def _compute_out_of_policy(profile: dict, allowed: dict[str, set[str]]) -> list[str]:
    out: list[str] = []
    checks: list[tuple[str, str]] = [
        ("vibe", "vibes"),
        ("iconography_pack", "iconography_packs"),
        ("sound_pack", "sound_packs"),
        ("affirmation_tone", "affirmation_tones"),
        ("companion_voice", "voice_personas"),
    ]
    for field_name, allow_key in checks:
        v = profile.get(field_name)
        if isinstance(v, str) and v != "" and v not in allowed[allow_key]:
            out.append(field_name)
    interest_tags = profile.get("interest_tags") or []
    if isinstance(interest_tags, list) and any(t not in allowed["interest_tags"] for t in interest_tags):
        out.append("interest_tags")
    return out


def _profile_to_read(child_id: uuid.UUID, profile: dict, out_of_policy: list[str]) -> ChildPersonalizationRead:
    return ChildPersonalizationRead(
        child_id=child_id,
        companion_name=str(profile.get("companion_name", "")),
        companion_voice=str(profile.get("companion_voice", "")),
        vibe=str(profile.get("vibe", "calm")),
        iconography_pack=str(profile.get("iconography_pack", "default")),
        sound_pack=str(profile.get("sound_pack", "soft")),
        affirmation_tone=str(profile.get("affirmation_tone", "warm")),
        interest_tags=list(profile.get("interest_tags") or []),
        out_of_policy=out_of_policy,
        onboarded=bool(profile.get("onboarded", False)),
    )


def _is_safe_companion_name(name: str) -> bool:
    """Minimal companion-name guard.

    ``app/core`` has no shared ``is_safe_text`` helper at the time of
    writing, so we apply a conservative local rule: 1-30 chars (already
    enforced by Pydantic), no control characters, no embedded
    newlines, no pure-whitespace string. This will be replaced when a
    shared helper lands.
    """
    if not name or not name.strip():
        return False
    return not any(ord(c) < 32 for c in name)


def _structured_policy_error(field: str, value: object, allowed: list[str]) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "field": field,
            "value": value,
            "allowed": sorted(allowed),
            "reason": "outside policy",
        },
    )


def _validate_id_in_library(field: str, value: str, getter) -> None:  # type: ignore[no-untyped-def]
    if getter(value) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"field": field, "value": value, "reason": "unknown library entry"},
        )


# ── Library endpoint ──────────────────────────────────────────────


@router.get("/personalization/library", response_model=PersonalizationLibraryRead)
async def get_library(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PersonalizationLibraryRead:
    """Return the full library with per-entry availability flags.

    Each entry has ``available: bool`` reflecting whether the
    household policy permits it. Frontend renders the locked entries
    differently (greyed out with an explanation).
    """
    policy = await _load_policy(db, user.household_id)
    allowed = _allowed_sets(_policy_to_read(policy))

    return PersonalizationLibraryRead(
        vibes=[
            VibeEntry(
                id=v.id,
                label=v.label,
                description=v.description,
                tokens=dict(v.tokens),
                available=v.id in allowed["vibes"],
            )
            for v in VIBES
        ],
        interest_tags=[
            InterestTagEntry(
                id=t.id,
                label=t.label,
                category=t.category,
                icon_keyword=t.icon_keyword,
                available=t.id in allowed["interest_tags"],
            )
            for t in INTEREST_TAGS
        ],
        voice_personas=[
            VoicePersonaEntry(
                id=p.id,
                label=p.label,
                default_companion_name=p.default_companion_name,
                tone_summary=p.tone_summary,
                available=p.id in allowed["voice_personas"],
            )
            for p in VOICE_PERSONAS
        ],
        iconography_packs=[
            IconographyPackEntry(
                id=p.id,
                label=p.label,
                description=p.description,
                icons=dict(p.icons),
                available=p.id in allowed["iconography_packs"],
            )
            for p in ICONOGRAPHY_PACKS
        ],
        sound_packs=[
            SoundPackEntry(
                id=p.id,
                label=p.label,
                description=p.description,
                cues=dict(p.cues),
                available=p.id in allowed["sound_packs"],
            )
            for p in SOUND_PACKS
        ],
        affirmation_tones=[
            AffirmationToneEntry(
                id=t.id,
                label=t.label,
                tone_summary=t.tone_summary,
                available=t.id in allowed["affirmation_tones"],
            )
            for t in AFFIRMATION_TONES
        ],
        max_interest_tags_per_child=(
            policy.max_interest_tags_per_child if policy is not None else _DEFAULT_POLICY_MAX_INTEREST_TAGS
        ),
    )


# ── Per-child profile endpoints ───────────────────────────────────


@router.get("/children/{child_id}/personalization", response_model=ChildPersonalizationRead)
async def get_child_personalization(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    child: Child = Depends(require_child_access("read")),
) -> ChildPersonalizationRead:
    result = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child.id))
    prefs = result.scalar_one_or_none()
    raw_personalization: dict = (prefs.personalization if prefs is not None else {}) or {}
    raw_interests: list[str] = list(prefs.interests or []) if prefs is not None else []

    profile = _merge_profile(raw_personalization, raw_interests)

    policy = await _load_policy(db, user.household_id)
    allowed = _allowed_sets(_policy_to_read(policy))
    out_of_policy = _compute_out_of_policy(profile, allowed)

    return _profile_to_read(child.id, profile, out_of_policy)


@router.put("/children/{child_id}/personalization", response_model=ChildPersonalizationRead)
async def update_child_personalization(
    body: ChildPersonalizationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    child: Child = Depends(require_child_access("write")),
) -> ChildPersonalizationRead:
    policy = await _load_policy(db, user.household_id)
    policy_read = _policy_to_read(policy)
    allowed = _allowed_sets(policy_read)

    # 1. Library validation: unknown IDs are 400.
    if body.vibe is not None:
        _validate_id_in_library("vibe", body.vibe, get_vibe)
    if body.iconography_pack is not None:
        _validate_id_in_library("iconography_pack", body.iconography_pack, get_iconography_pack)
    if body.sound_pack is not None:
        _validate_id_in_library("sound_pack", body.sound_pack, get_sound_pack)
    if body.affirmation_tone is not None:
        _validate_id_in_library("affirmation_tone", body.affirmation_tone, get_affirmation_tone)
    if body.companion_voice is not None:
        _validate_id_in_library("companion_voice", body.companion_voice, get_voice_persona)
    if body.interest_tags is not None:
        for tag in body.interest_tags:
            if get_interest_tag(tag) is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"field": "interest_tags", "value": tag, "reason": "unknown library entry"},
                )

    # 2. Policy validation: out-of-policy is 403 with structured detail.
    if body.vibe is not None and body.vibe not in allowed["vibes"]:
        raise _structured_policy_error("vibe", body.vibe, list(allowed["vibes"]))
    if body.iconography_pack is not None and body.iconography_pack not in allowed["iconography_packs"]:
        raise _structured_policy_error("iconography_pack", body.iconography_pack, list(allowed["iconography_packs"]))
    if body.sound_pack is not None and body.sound_pack not in allowed["sound_packs"]:
        raise _structured_policy_error("sound_pack", body.sound_pack, list(allowed["sound_packs"]))
    if body.affirmation_tone is not None and body.affirmation_tone not in allowed["affirmation_tones"]:
        raise _structured_policy_error("affirmation_tone", body.affirmation_tone, list(allowed["affirmation_tones"]))
    if body.companion_voice is not None and body.companion_voice not in allowed["voice_personas"]:
        raise _structured_policy_error("companion_voice", body.companion_voice, list(allowed["voice_personas"]))
    if body.interest_tags is not None:
        for tag in body.interest_tags:
            if tag not in allowed["interest_tags"]:
                raise _structured_policy_error("interest_tags", tag, list(allowed["interest_tags"]))
        if len(body.interest_tags) > policy_read.max_interest_tags_per_child:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "field": "interest_tags",
                    "value": len(body.interest_tags),
                    "max": policy_read.max_interest_tags_per_child,
                    "reason": "too many interest tags",
                },
            )

    # 3. Companion name validation.
    if body.companion_name is not None and not _is_safe_companion_name(body.companion_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"field": "companion_name", "reason": "invalid companion name"},
        )

    # 4. Load or create the preferences row.
    result = await db.execute(select(ChildPreferences).where(ChildPreferences.child_id == child.id))
    prefs = result.scalar_one_or_none()
    if prefs is None:
        prefs = ChildPreferences(
            child_id=child.id,
            household_id=user.household_id,
            personalization={},
            interests=[],
        )
        db.add(prefs)

    # SQLAlchemy needs a fresh dict reference to detect a mutation on
    # a JSONB column; mutating in place doesn't always flush.
    personalization = dict(prefs.personalization or {})

    if body.companion_name is not None:
        if policy_read.companion_name_requires_review:
            # Hold pending; the active companion_name stays unchanged.
            personalization["companion_name_pending"] = body.companion_name
            # Audit-log the pending request so the trace shows it.
            await _log_audit(
                db,
                household_id=user.household_id,
                user_id=user.id,
                action=GovernanceAction.defer,
                target_id=child.id,
                reason="companion_name_pending_review",
                metadata={"pending_companion_name": body.companion_name},
            )
        else:
            personalization["companion_name"] = body.companion_name
            # If a prior pending value exists, retire it.
            personalization.pop("companion_name_pending", None)

    if body.companion_voice is not None:
        personalization["companion_voice"] = body.companion_voice
    if body.vibe is not None:
        personalization["vibe"] = body.vibe
    if body.iconography_pack is not None:
        personalization["iconography_pack"] = body.iconography_pack
    if body.sound_pack is not None:
        personalization["sound_pack"] = body.sound_pack
    if body.affirmation_tone is not None:
        personalization["affirmation_tone"] = body.affirmation_tone
    if body.onboarded is not None:
        personalization["onboarded"] = body.onboarded

    prefs.personalization = personalization
    if body.interest_tags is not None:
        prefs.interests = list(body.interest_tags)

    await db.flush()

    # Resolve the view.
    raw_interests: list[str] = list(prefs.interests or [])
    profile = _merge_profile(personalization, raw_interests)
    out_of_policy = _compute_out_of_policy(profile, allowed)
    return _profile_to_read(child.id, profile, out_of_policy)


# ── Policy endpoints ──────────────────────────────────────────────


@router.get("/personalization/policy", response_model=PersonalizationPolicyRead)
async def get_policy(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PersonalizationPolicyRead:
    policy = await _load_policy(db, user.household_id)
    return _policy_to_read(policy)


@router.put("/personalization/policy", response_model=PersonalizationPolicyRead)
async def update_policy(
    body: PersonalizationPolicyUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PersonalizationPolicyRead:
    # Guardians only. ``UserRole.observer`` is read-only by definition;
    # any owner or co_parent may tighten or loosen the household policy.
    if user.role == UserRole.observer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Observers cannot modify the personalization policy",
        )

    # Validate every supplied list against the library. Sentinel ["*"]
    # is always valid by itself; mixed sentinel + explicit IDs is not.
    list_field_checks: list[tuple[str, list[str] | None, list[str]]] = [
        ("allowed_vibes", body.allowed_vibes, _VIBE_IDS),
        ("allowed_interest_tags", body.allowed_interest_tags, _INTEREST_IDS),
        ("allowed_voice_personas", body.allowed_voice_personas, _VOICE_IDS),
        ("allowed_iconography_packs", body.allowed_iconography_packs, _ICONOGRAPHY_IDS),
        ("allowed_sound_packs", body.allowed_sound_packs, _SOUND_IDS),
        ("allowed_affirmation_tones", body.allowed_affirmation_tones, _TONE_IDS),
    ]
    for field_name, supplied, library_ids in list_field_checks:
        if supplied is None:
            continue
        if supplied == ["*"]:
            continue
        if any(item == "*" for item in supplied):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "field": field_name,
                    "reason": "sentinel '*' cannot be mixed with explicit IDs",
                },
            )
        for item in supplied:
            if item not in library_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "field": field_name,
                        "value": item,
                        "reason": "unknown library entry",
                    },
                )

    policy = await _load_policy(db, user.household_id)
    created = False
    if policy is None:
        policy = PersonalizationPolicy(household_id=user.household_id)
        db.add(policy)
        created = True

    # Build a before/after diff for the audit log so the governance
    # trace records exactly which knob shifted.
    before = _policy_to_read(None if created else policy).model_dump()

    if body.allowed_vibes is not None:
        policy.allowed_vibes = list(body.allowed_vibes)
    if body.allowed_interest_tags is not None:
        policy.allowed_interest_tags = list(body.allowed_interest_tags)
    if body.allowed_voice_personas is not None:
        policy.allowed_voice_personas = list(body.allowed_voice_personas)
    if body.allowed_iconography_packs is not None:
        policy.allowed_iconography_packs = list(body.allowed_iconography_packs)
    if body.allowed_sound_packs is not None:
        policy.allowed_sound_packs = list(body.allowed_sound_packs)
    if body.allowed_affirmation_tones is not None:
        policy.allowed_affirmation_tones = list(body.allowed_affirmation_tones)
    if body.companion_name_requires_review is not None:
        policy.companion_name_requires_review = body.companion_name_requires_review
    if body.max_interest_tags_per_child is not None:
        policy.max_interest_tags_per_child = body.max_interest_tags_per_child
    # Voice-input governance (migration 044).
    if body.voice_input_enabled is not None:
        policy.voice_input_enabled = body.voice_input_enabled
    if body.voice_minutes_daily_cap is not None:
        policy.voice_minutes_daily_cap = body.voice_minutes_daily_cap
    if body.whisper_provider is not None:
        policy.whisper_provider = body.whisper_provider

    await db.flush()

    after = _policy_to_read(policy).model_dump()
    diff = {k: {"before": before.get(k), "after": after.get(k)} for k in after if before.get(k) != after.get(k)}

    await _log_audit(
        db,
        household_id=user.household_id,
        user_id=user.id,
        action=GovernanceAction.modify,
        target_id=user.household_id,
        reason="personalization_policy_updated",
        metadata={"diff": diff, "created": created},
    )

    return _policy_to_read(policy)


# ── Audit ─────────────────────────────────────────────────────────


async def _log_audit(
    db: AsyncSession,
    *,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None,
    action: GovernanceAction,
    target_id: uuid.UUID,
    reason: str,
    metadata: dict | None = None,
) -> None:
    """Write a governance event for personalization changes.

    Wraps ``app.services.governance.log_governance_event`` so the
    handler bodies don't import service internals directly. The
    intelligence-pattern hook the service performs is harmless for
    personalization (it only records activity_type and difficulty
    when present), so we let it run unmodified.
    """
    from app.services.governance import log_governance_event

    await log_governance_event(
        db,
        household_id=household_id,
        user_id=user_id,
        action=action,
        target_type="personalization",
        target_id=target_id,
        reason=reason,
        metadata=metadata,
    )
