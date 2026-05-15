"""Canonical personalization library.

This module is the single source of truth for the kid-driven
personalization profile. Anything a child can pick from (vibe,
interests, voice persona, iconography pack, sound pack, affirmation
tone) is defined here as a frozen dataclass.

Validation of incoming API IDs happens against these tables at the API
layer; the database stores opaque string IDs only. Adding a new entry
is a code change that ships with a tested PR, never a runtime
configuration knob.

Voice ``voice_id_placeholder`` is empty for Part 1; Part 2 will bind
each persona to a real TTS voice id.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Vibe:
    id: str
    label: str
    description: str
    tokens: dict[str, str]


@dataclass(frozen=True)
class InterestTag:
    id: str
    label: str
    category: str
    icon_keyword: str
    content_hint: str


@dataclass(frozen=True)
class VoicePersona:
    id: str
    label: str
    default_companion_name: str
    tone_summary: str
    voice_id_placeholder: str
    # TTS fields (Sprint v2 Prompt 2). voice_id_placeholder predates
    # the live binding and is retained for back-compat; tts_voice_id
    # is the authoritative voice the OpenAI/ElevenLabs provider uses.
    tts_voice_id: str = ""
    tts_provider: str = "openai"
    speech_rate: float = 1.0
    prosody_hints: str = ""


@dataclass(frozen=True)
class IconographyPack:
    id: str
    label: str
    description: str
    icons: dict[str, str]


@dataclass(frozen=True)
class SoundPack:
    id: str
    label: str
    description: str
    cues: dict[str, str | None]


@dataclass(frozen=True)
class AffirmationTone:
    id: str
    label: str
    tone_summary: str


# Every vibe defines the same complete set of CSS variable keys so the
# token swap is deterministic on the frontend. Adding a key here means
# every existing vibe must also define it.
_VIBE_TOKEN_KEYS = (
    "--color-page",
    "--color-surface",
    "--color-accent",
    "--color-text",
    "--color-text-secondary",
    "--color-border",
    "--color-brand-gold",
    "--radius-card",
    "--font-weight-heading",
)


VIBES: tuple[Vibe, ...] = (
    Vibe(
        id="calm",
        label="Calm",
        description="The default. Off-white surfaces, navy accent, room to breathe.",
        tokens={
            "--color-page": "#FAFAF8",
            "--color-surface": "#FFFFFF",
            "--color-accent": "#4A6FA5",
            "--color-text": "#1A1A1A",
            "--color-text-secondary": "#6B6B6B",
            "--color-border": "#E5E5E0",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "16px",
            "--font-weight-heading": "600",
        },
    ),
    Vibe(
        id="field",
        label="Field",
        description="Forest green page tint, cream surfaces, a hand-drawn nature feel.",
        tokens={
            "--color-page": "#2D5F3F",
            "--color-surface": "#F5F1E6",
            "--color-accent": "#8FA37A",
            "--color-text": "#1F2A20",
            "--color-text-secondary": "#5B6B5C",
            "--color-border": "#D8D0BB",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "18px",
            "--font-weight-heading": "600",
        },
    ),
    Vibe(
        id="orbit",
        label="Orbit",
        description="Deep blue space, cyan highlights, geometric edges.",
        tokens={
            "--color-page": "#0B1426",
            "--color-surface": "#16223A",
            "--color-accent": "#7BD9F0",
            "--color-text": "#F1F4FA",
            "--color-text-secondary": "#9AA8C2",
            "--color-border": "#283755",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "12px",
            "--font-weight-heading": "600",
        },
    ),
    Vibe(
        id="workshop",
        label="Workshop",
        description="Warm wood, steel accents, the feel of a maker bench.",
        tokens={
            "--color-page": "#3A2718",
            "--color-surface": "#5C4632",
            "--color-accent": "#7B8590",
            "--color-text": "#F4ECDE",
            "--color-text-secondary": "#C8B8A0",
            "--color-border": "#704E33",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "10px",
            "--font-weight-heading": "700",
        },
    ),
    Vibe(
        id="studio",
        label="Studio",
        description="Cream paper, soft pastel pink, rounded corners, gentle and bright.",
        tokens={
            "--color-page": "#FFF8E7",
            "--color-surface": "#FFFFFF",
            "--color-accent": "#E8B4B8",
            "--color-text": "#3A2A2A",
            "--color-text-secondary": "#7A6A6A",
            "--color-border": "#F0E5D6",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "24px",
            "--font-weight-heading": "600",
        },
    ),
    Vibe(
        id="bold",
        label="Bold",
        description="Maximum contrast, bright orange accent, heavy display weight.",
        tokens={
            "--color-page": "#0A0A0A",
            "--color-surface": "#FFFFFF",
            "--color-accent": "#FF6B35",
            "--color-text": "#0A0A0A",
            "--color-text-secondary": "#3A3A3A",
            "--color-border": "#1A1A1A",
            "--color-brand-gold": "#C6A24E",
            "--radius-card": "8px",
            "--font-weight-heading": "800",
        },
    ),
)


INTEREST_TAGS: tuple[InterestTag, ...] = (
    # nature_animals
    InterestTag(
        id="dinosaurs",
        label="Dinosaurs",
        category="nature_animals",
        icon_keyword="dinosaur",
        content_hint=(
            "Uses examples involving dinosaurs, paleontology, fossils, and prehistoric "
            "ecosystems when a learning context permits."
        ),
    ),
    InterestTag(
        id="horses",
        label="Horses",
        category="nature_animals",
        icon_keyword="horse",
        content_hint=(
            "Uses examples involving horses, riding, gaits, breeds, and stable life when a learning context permits."
        ),
    ),
    InterestTag(
        id="dogs",
        label="Dogs",
        category="nature_animals",
        icon_keyword="dog",
        content_hint=(
            "Uses examples involving dogs, breeds, training, and dog behavior when a learning context permits."
        ),
    ),
    InterestTag(
        id="big_cats",
        label="Big Cats",
        category="nature_animals",
        icon_keyword="tiger",
        content_hint=(
            "Uses examples involving lions, tigers, leopards, conservation, and "
            "predator behavior when a learning context permits."
        ),
    ),
    InterestTag(
        id="marine_life",
        label="Marine Life",
        category="nature_animals",
        icon_keyword="whale",
        content_hint=(
            "Uses examples involving oceans, whales, sharks, coral reefs, and marine "
            "biology when a learning context permits."
        ),
    ),
    InterestTag(
        id="bugs",
        label="Bugs",
        category="nature_animals",
        icon_keyword="bug",
        content_hint=(
            "Uses examples involving insects, spiders, metamorphosis, and bug behavior when a learning context permits."
        ),
    ),
    InterestTag(
        id="birds",
        label="Birds",
        category="nature_animals",
        icon_keyword="bird",
        content_hint=(
            "Uses examples involving birds, migration, flight, song, and habitat when a learning context permits."
        ),
    ),
    InterestTag(
        id="hiking",
        label="Hiking",
        category="nature_animals",
        icon_keyword="mountain",
        content_hint=(
            "Uses examples involving trails, terrain, gear, maps, and outdoor "
            "exploration when a learning context permits."
        ),
    ),
    # space_science
    InterestTag(
        id="space",
        label="Space",
        category="space_science",
        icon_keyword="rocket",
        content_hint=(
            "Uses examples involving astronauts, rockets, satellites, and space "
            "missions when a learning context permits."
        ),
    ),
    InterestTag(
        id="planets",
        label="Planets",
        category="space_science",
        icon_keyword="planet",
        content_hint=(
            "Uses examples involving the solar system, planet characteristics, moons, "
            "and orbits when a learning context permits."
        ),
    ),
    InterestTag(
        id="robots",
        label="Robots",
        category="space_science",
        icon_keyword="robot",
        content_hint=(
            "Uses examples involving robots, sensors, actuators, and automated systems when a learning context permits."
        ),
    ),
    InterestTag(
        id="weather",
        label="Weather",
        category="space_science",
        icon_keyword="cloud",
        content_hint=(
            "Uses examples involving storms, forecasting, climate patterns, and "
            "atmospheric science when a learning context permits."
        ),
    ),
    InterestTag(
        id="chemistry",
        label="Chemistry",
        category="space_science",
        icon_keyword="flask",
        content_hint=(
            "Uses examples involving reactions, elements, lab procedures, and everyday "
            "chemistry when a learning context permits."
        ),
    ),
    InterestTag(
        id="geology",
        label="Geology",
        category="space_science",
        icon_keyword="rock",
        content_hint=(
            "Uses examples involving rocks, minerals, plate tectonics, and earth "
            "formation when a learning context permits."
        ),
    ),
    # vehicles
    InterestTag(
        id="trains",
        label="Trains",
        category="vehicles",
        icon_keyword="train",
        content_hint=(
            "Uses examples involving trains, conductors, locomotives, freight, "
            "signals, and rail history when a learning context permits."
        ),
    ),
    InterestTag(
        id="planes",
        label="Planes",
        category="vehicles",
        icon_keyword="plane",
        content_hint=(
            "Uses examples involving airplanes, pilots, flight physics, and aviation "
            "history when a learning context permits."
        ),
    ),
    InterestTag(
        id="cars",
        label="Cars",
        category="vehicles",
        icon_keyword="car",
        content_hint=(
            "Uses examples involving cars, engines, racing, and road systems when a learning context permits."
        ),
    ),
    InterestTag(
        id="boats",
        label="Boats",
        category="vehicles",
        icon_keyword="boat",
        content_hint=(
            "Uses examples involving boats, sailing, harbors, and naval history when a learning context permits."
        ),
    ),
    InterestTag(
        id="construction_equipment",
        label="Construction Equipment",
        category="vehicles",
        icon_keyword="excavator",
        content_hint=(
            "Uses examples involving excavators, cranes, bulldozers, and construction "
            "sites when a learning context permits."
        ),
    ),
    # sports_movement
    InterestTag(
        id="soccer",
        label="Soccer",
        category="sports_movement",
        icon_keyword="soccer",
        content_hint=("Uses examples involving soccer, positions, plays, and matches when a learning context permits."),
    ),
    InterestTag(
        id="basketball",
        label="Basketball",
        category="sports_movement",
        icon_keyword="basketball",
        content_hint=("Uses examples involving basketball, shots, plays, and stats when a learning context permits."),
    ),
    InterestTag(
        id="baseball",
        label="Baseball",
        category="sports_movement",
        icon_keyword="baseball",
        content_hint=(
            "Uses examples involving baseball, pitching, batting, fielding, and stats when a learning context permits."
        ),
    ),
    InterestTag(
        id="gymnastics",
        label="Gymnastics",
        category="sports_movement",
        icon_keyword="gymnast",
        content_hint=(
            "Uses examples involving gymnastics routines, apparatus, and athlete "
            "training when a learning context permits."
        ),
    ),
    InterestTag(
        id="martial_arts",
        label="Martial Arts",
        category="sports_movement",
        icon_keyword="martial_arts",
        content_hint=(
            "Uses examples involving martial arts forms, belt progression, and "
            "discipline when a learning context permits."
        ),
    ),
    InterestTag(
        id="climbing",
        label="Climbing",
        category="sports_movement",
        icon_keyword="climber",
        content_hint=(
            "Uses examples involving rock climbing, holds, routes, and gear when a learning context permits."
        ),
    ),
    # arts_music
    InterestTag(
        id="drawing",
        label="Drawing",
        category="arts_music",
        icon_keyword="pencil",
        content_hint=(
            "Uses examples involving drawing, sketching, and visual composition when a learning context permits."
        ),
    ),
    InterestTag(
        id="painting",
        label="Painting",
        category="arts_music",
        icon_keyword="paintbrush",
        content_hint=(
            "Uses examples involving painting, color theory, and famous works when a learning context permits."
        ),
    ),
    InterestTag(
        id="music",
        label="Music",
        category="arts_music",
        icon_keyword="music_note",
        content_hint=(
            "Uses examples involving instruments, notation, rhythm, and song structure when a learning context permits."
        ),
    ),
    InterestTag(
        id="dance",
        label="Dance",
        category="arts_music",
        icon_keyword="dancer",
        content_hint=(
            "Uses examples involving dance styles, choreography, and movement when a learning context permits."
        ),
    ),
    InterestTag(
        id="photography",
        label="Photography",
        category="arts_music",
        icon_keyword="camera",
        content_hint=(
            "Uses examples involving cameras, light, composition, and photo techniques when a learning context permits."
        ),
    ),
    # fantasy_history
    InterestTag(
        id="medieval",
        label="Medieval",
        category="fantasy_history",
        icon_keyword="castle",
        content_hint=(
            "Uses examples involving castles, knights, guilds, and medieval life when a learning context permits."
        ),
    ),
    InterestTag(
        id="ancient_egypt",
        label="Ancient Egypt",
        category="fantasy_history",
        icon_keyword="pyramid",
        content_hint=(
            "Uses examples involving pyramids, hieroglyphs, pharaohs, and the Nile when a learning context permits."
        ),
    ),
    InterestTag(
        id="mythology",
        label="Mythology",
        category="fantasy_history",
        icon_keyword="trident",
        content_hint=("Uses examples involving myths and gods from world traditions when a learning context permits."),
    ),
    InterestTag(
        id="dragons",
        label="Dragons",
        category="fantasy_history",
        icon_keyword="dragon",
        content_hint=("Uses examples involving dragons and dragon-themed adventure when a learning context permits."),
    ),
    InterestTag(
        id="vikings",
        label="Vikings",
        category="fantasy_history",
        icon_keyword="viking_helmet",
        content_hint=(
            "Uses examples involving Viking voyages, longships, sagas, and Norse "
            "culture when a learning context permits."
        ),
    ),
    InterestTag(
        id="pirates",
        label="Pirates",
        category="fantasy_history",
        icon_keyword="pirate_flag",
        content_hint=(
            "Uses examples involving pirate ships, treasure maps, and sea voyages when a learning context permits."
        ),
    ),
    # building_making
    InterestTag(
        id="lego",
        label="Lego",
        category="building_making",
        icon_keyword="brick",
        content_hint=(
            "Uses examples involving Lego builds, brick math, and design challenges when a learning context permits."
        ),
    ),
    InterestTag(
        id="woodworking",
        label="Woodworking",
        category="building_making",
        icon_keyword="saw",
        content_hint=(
            "Uses examples involving woodworking, joinery, measuring, and shop safety when a learning context permits."
        ),
    ),
    InterestTag(
        id="electronics",
        label="Electronics",
        category="building_making",
        icon_keyword="circuit",
        content_hint=(
            "Uses examples involving circuits, components, and small electronics "
            "projects when a learning context permits."
        ),
    ),
    InterestTag(
        id="coding",
        label="Coding",
        category="building_making",
        icon_keyword="code",
        content_hint=(
            "Uses examples involving programming, loops, conditionals, and small "
            "projects when a learning context permits."
        ),
    ),
    InterestTag(
        id="model_kits",
        label="Model Kits",
        category="building_making",
        icon_keyword="airplane_model",
        content_hint=(
            "Uses examples involving model kits, scale, assembly, and finishing when a learning context permits."
        ),
    ),
    # food_cooking
    InterestTag(
        id="baking",
        label="Baking",
        category="food_cooking",
        icon_keyword="bread",
        content_hint=(
            "Uses examples involving baking, measuring, ratios, and oven temperatures when a learning context permits."
        ),
    ),
    InterestTag(
        id="cooking",
        label="Cooking",
        category="food_cooking",
        icon_keyword="pot",
        content_hint=("Uses examples involving recipes, technique, and meal planning when a learning context permits."),
    ),
    InterestTag(
        id="gardening",
        label="Gardening",
        category="food_cooking",
        icon_keyword="plant",
        content_hint=(
            "Uses examples involving plants, soil, seasons, and small gardens when a learning context permits."
        ),
    ),
    InterestTag(
        id="farming",
        label="Farming",
        category="food_cooking",
        icon_keyword="barn",
        content_hint=(
            "Uses examples involving farms, livestock, crops, and rural life when a learning context permits."
        ),
    ),
    # everyday_world
    InterestTag(
        id="geography",
        label="Geography",
        category="everyday_world",
        icon_keyword="globe",
        content_hint=(
            "Uses examples involving countries, capitals, terrain, and maps when a learning context permits."
        ),
    ),
    InterestTag(
        id="languages",
        label="Languages",
        category="everyday_world",
        icon_keyword="speech_bubble",
        content_hint=(
            "Uses examples involving world languages, phrases, and writing systems when a learning context permits."
        ),
    ),
    InterestTag(
        id="money_finance",
        label="Money and Finance",
        category="everyday_world",
        icon_keyword="coin",
        content_hint=(
            "Uses examples involving currency, saving, budgeting, and small-business "
            "math when a learning context permits."
        ),
    ),
)


VOICE_PERSONAS: tuple[VoicePersona, ...] = (
    VoicePersona(
        id="default_warm",
        label="Warm",
        default_companion_name="Sage",
        tone_summary="Calm, encouraging, slightly older, focuses on effort and growth.",
        voice_id_placeholder="",
        tts_voice_id="nova",
        tts_provider="openai",
        speech_rate=0.95,
        prosody_hints="warm and unhurried",
    ),
    VoicePersona(
        id="default_bright",
        label="Bright",
        default_companion_name="Nova",
        tone_summary="Energetic, upbeat, peer-adjacent, celebrates wins audibly.",
        voice_id_placeholder="",
        tts_voice_id="shimmer",
        tts_provider="openai",
        speech_rate=1.05,
        prosody_hints="bright and energetic",
    ),
    VoicePersona(
        id="default_steady",
        label="Steady",
        default_companion_name="Atlas",
        tone_summary="Measured, factual, brief, no filler, treats the kid as capable.",
        voice_id_placeholder="",
        tts_voice_id="onyx",
        tts_provider="openai",
        speech_rate=0.92,
        prosody_hints="measured and clear",
    ),
    VoicePersona(
        id="default_playful",
        label="Playful",
        default_companion_name="Pip",
        tone_summary="Witty and light, safe jokes, never sarcastic at the child's expense.",
        voice_id_placeholder="",
        tts_voice_id="fable",
        tts_provider="openai",
        speech_rate=1.05,
        prosody_hints="light and playful",
    ),
    VoicePersona(
        id="default_gentle",
        label="Gentle",
        default_companion_name="Wren",
        tone_summary="Soft, patient, slow to push, validates struggle before asking for next step.",
        voice_id_placeholder="",
        tts_voice_id="alloy",
        tts_provider="openai",
        speech_rate=0.90,
        prosody_hints="soft and patient",
    ),
)


# Iconography packs map the six ActivityType values to icon keywords.
# The actual SVG assets ship later; the frontend looks them up by
# keyword.
_ACTIVITY_TYPES = ("lesson", "practice", "review", "assessment", "project", "field_trip")


ICONOGRAPHY_PACKS: tuple[IconographyPack, ...] = (
    IconographyPack(
        id="default",
        label="Default",
        description="The METHEAN house style. Clean line icons.",
        icons={
            "lesson": "book_open",
            "practice": "pencil",
            "review": "rotate_left",
            "assessment": "clipboard_check",
            "project": "hammer",
            "field_trip": "map_pin",
        },
    ),
    IconographyPack(
        id="orbit",
        label="Orbit",
        description="Space-themed icons. Stars, satellites, planets.",
        icons={
            "lesson": "satellite",
            "practice": "comet",
            "review": "orbit",
            "assessment": "telescope",
            "project": "rocket",
            "field_trip": "planet",
        },
    ),
    IconographyPack(
        id="field",
        label="Field",
        description="Nature-themed icons. Leaves, trails, animal tracks.",
        icons={
            "lesson": "leaf",
            "practice": "footprints",
            "review": "compass",
            "assessment": "magnifier",
            "project": "tent",
            "field_trip": "trail",
        },
    ),
    IconographyPack(
        id="workshop",
        label="Workshop",
        description="Maker icons. Tools and gears.",
        icons={
            "lesson": "blueprint",
            "practice": "wrench",
            "review": "gear",
            "assessment": "ruler",
            "project": "drill",
            "field_trip": "truck",
        },
    ),
    IconographyPack(
        id="studio",
        label="Studio",
        description="Soft, illustrated icons. Brushes, palettes, ribbons.",
        icons={
            "lesson": "open_notebook",
            "practice": "paintbrush",
            "review": "loop_arrow",
            "assessment": "ribbon",
            "project": "easel",
            "field_trip": "balloon",
        },
    ),
)


SOUND_PACKS: tuple[SoundPack, ...] = (
    SoundPack(
        id="off",
        label="Off",
        description="No sound effects.",
        cues={
            "activity_start": None,
            "correct": None,
            "hint_revealed": None,
            "activity_complete": None,
            "mastery_up": None,
            "day_complete": None,
        },
    ),
    SoundPack(
        id="soft",
        label="Soft",
        description="Subtle, low-volume cues. Quiet enough for a shared room.",
        cues={
            "activity_start": "/sounds/soft/activity_start.mp3",
            "correct": "/sounds/soft/correct.mp3",
            "hint_revealed": "/sounds/soft/hint_revealed.mp3",
            "activity_complete": "/sounds/soft/activity_complete.mp3",
            "mastery_up": "/sounds/soft/mastery_up.mp3",
            "day_complete": "/sounds/soft/day_complete.mp3",
        },
    ),
    SoundPack(
        id="full",
        label="Full",
        description="Full game-style audio: chimes, fanfares, celebration.",
        cues={
            "activity_start": "/sounds/full/activity_start.mp3",
            "correct": "/sounds/full/correct.mp3",
            "hint_revealed": "/sounds/full/hint_revealed.mp3",
            "activity_complete": "/sounds/full/activity_complete.mp3",
            "mastery_up": "/sounds/full/mastery_up.mp3",
            "day_complete": "/sounds/full/day_complete.mp3",
        },
    ),
)


AFFIRMATION_TONES: tuple[AffirmationTone, ...] = (
    AffirmationTone(
        id="warm",
        label="Warm",
        tone_summary=(
            "Encouraging, focuses on effort, gentle. Names what the child did well before suggesting next steps."
        ),
    ),
    AffirmationTone(
        id="direct",
        label="Direct",
        tone_summary=("Brief, factual, focused on the work. Limits filler words. Acknowledges correct work plainly."),
    ),
    AffirmationTone(
        id="playful",
        label="Playful",
        tone_summary=("Light, occasional playful phrasing, peer-adjacent. Avoids sarcasm and condescension."),
    ),
)


# Defensive structural assertion: every vibe must define the same
# token keys so a runtime swap can never leave a CSS variable unset.
for _vibe in VIBES:
    assert set(_vibe.tokens.keys()) == set(_VIBE_TOKEN_KEYS), (
        f"Vibe {_vibe.id!r} missing or extra token keys: "
        f"expected {sorted(_VIBE_TOKEN_KEYS)}, got {sorted(_vibe.tokens.keys())}"
    )

# Every iconography pack must cover every activity type.
for _pack in ICONOGRAPHY_PACKS:
    assert set(_pack.icons.keys()) == set(_ACTIVITY_TYPES), (
        f"Iconography pack {_pack.id!r} missing activity types: "
        f"expected {sorted(_ACTIVITY_TYPES)}, got {sorted(_pack.icons.keys())}"
    )


# ── Lookup helpers ────────────────────────────────────────────────


def list_vibes() -> list[Vibe]:
    return list(VIBES)


def get_vibe(id: str) -> Vibe | None:
    return next((v for v in VIBES if v.id == id), None)


def list_interest_tags() -> list[InterestTag]:
    return list(INTEREST_TAGS)


def get_interest_tag(id: str) -> InterestTag | None:
    return next((t for t in INTEREST_TAGS if t.id == id), None)


def list_voice_personas() -> list[VoicePersona]:
    return list(VOICE_PERSONAS)


def get_voice_persona(id: str) -> VoicePersona | None:
    return next((p for p in VOICE_PERSONAS if p.id == id), None)


def list_iconography_packs() -> list[IconographyPack]:
    return list(ICONOGRAPHY_PACKS)


def get_iconography_pack(id: str) -> IconographyPack | None:
    return next((p for p in ICONOGRAPHY_PACKS if p.id == id), None)


def list_sound_packs() -> list[SoundPack]:
    return list(SOUND_PACKS)


def get_sound_pack(id: str) -> SoundPack | None:
    return next((p for p in SOUND_PACKS if p.id == id), None)


def list_affirmation_tones() -> list[AffirmationTone]:
    return list(AFFIRMATION_TONES)


def get_affirmation_tone(id: str) -> AffirmationTone | None:
    return next((t for t in AFFIRMATION_TONES if t.id == id), None)


def expand_allowlist(policy_value: list[str], full_ids: list[str]) -> set[str]:
    """Expand the ``['*']`` sentinel into the full ID set.

    Any explicit list is returned as-is (deduplicated). IDs in the
    policy list that are not in ``full_ids`` are still returned so the
    caller can detect drift; validation is up to the caller.
    """
    if policy_value == ["*"]:
        return set(full_ids)
    return set(policy_value)
