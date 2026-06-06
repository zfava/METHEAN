"""Node content schema and validation.

Defines the structured content JSONB schema for LearningNode.content.
This tells the AI tutor how to teach, the evaluator how to assess,
and the parent what resources to gather.
"""

# Expected structure for LearningNode.content JSONB
NODE_CONTENT_SCHEMA = {
    "learning_objectives": ["list of specific, measurable objectives"],
    "teaching_guidance": {
        "introduction": "How to introduce this concept",
        "practice_activities": ["activity types that build this skill"],
        "common_misconceptions": ["what students get wrong and how to address it"],
        "scaffolding_sequence": ["step-by-step from simple to complex"],
        "socratic_questions": ["key questions to ask rather than tell"],
        "real_world_connections": ["how this concept connects to life"],
    },
    "assessment_criteria": {
        "mastery_indicators": ["observable behaviors demonstrating mastery"],
        "proficiency_indicators": ["understanding but not fluency"],
        "developing_indicators": ["grasping with support"],
        "assessment_methods": ["oral narration", "written work", "demonstration", "project"],
        "sample_assessment_prompts": ["specific questions or tasks"],
    },
    "resource_guidance": {
        "required": ["what's needed (never brand names, always types)"],
        "recommended": ["nice to have"],
    },
    "connections": {
        "prerequisite_skills_from_other_subjects": [],
        "feeds_into": [],
        "parallel_topics": [],
    },
    # philosophy_specific holds one variant per pedagogical philosophy.
    # Each philosophy has its OWN native shape (below); the shapes are
    # intentionally different. A variant may also be a plain string,
    # which is a legacy, un-upgraded form: valid, not an error. This
    # block is the source of truth for the five native shapes. The
    # classical copywork field is optional: it is omitted for oral or
    # pre-print skills that have no authentic copywork.
    "philosophy_specific": {
        "traditional": {
            "introduction": "What the skill is and what today covers",
            "gradual_release": {
                "i_do": "Teacher models the skill explicitly",
                "we_do": "Teacher and child practice together",
                "you_do": "Child practices independently",
            },
            "guided_practice": ["practice done with support"],
            "independent_practice": ["practice done alone"],
            "mastery_check": ["observable checks the child can do the skill"],
            "spiral_review": ["earlier skills revisited to confirm retention"],
        },
        "classical": {
            "narrative_introduction": "An introduction framed as a story or idea",
            "memory_work": {
                "chants": ["sequences chanted to commit to memory"],
                "recitations": ["passages or rhymes recited from memory"],
            },
            "copywork": ["optional: text or numerals copied neatly by hand; omit for oral or pre-print skills"],
            "recitation_routine": "How prior memory work is reviewed cumulatively",
            "history_integration": "How the skill ties to the chronological spine",
            "read_aloud_suggestions": ["well-written texts to read aloud"],
        },
        "charlotte_mason": {
            "lesson_length_minutes": 0,
            "living_book_suggestions": ["beautiful, real books, never workbooks"],
            "short_lesson_flow": "The calm flow of a single short lesson",
            "narration_prompt": "A prompt inviting the child to tell back",
            "real_world_objects": ["real objects the lesson uses"],
            "nature_connection": "How the skill connects to nature study",
            "habit_focus": "The habit of mind this lesson cultivates",
        },
        "montessori": {
            "prepared_materials": ["concrete materials, ordered concrete to abstract"],
            "presentation": {
                "three_period_lesson": "Naming, recognition, recall",
                "steps": ["the ordered steps of the presentation"],
            },
            "control_of_error": "How the material reveals an error to the child",
            "abstraction_pathway": "The path from concrete material to abstraction",
            "extensions": ["further work that deepens the concept"],
            "observation_focus": "What the adult watches for instead of grading",
        },
        "unschooling": {
            "invitations": ["materials left out to invite, never assign"],
            "real_world_contexts": ["where the skill already lives in real life"],
            "conversation_starters": ["genuine questions that spark curiosity"],
            "resource_bank": ["resources kept available, not assigned"],
            "parent_role": "How the parent supports without turning it into a lesson",
            "observation_documentation": "How learning is noticed over time, not tested",
        },
    },
    "practice_items": [
        {
            "type": "problem type label",
            "difficulty": "int 1 to 3",
            "prompt": "the practice question",
            "expected_type": "number | text | multiple_choice | true_false",
            "correct_answer": "optional expected answer",
            "hints": ["optional progressive hints"],
            "explanation": "optional worked explanation",
            "options": ["optional choices for multiple_choice"],
        }
    ],
    "assessment_items": [
        {
            "prompt": "the assessment question",
            "type": "number | multiple_choice | true_false | open_response",
            "target_concept": "optional concept the item assesses",
            "rubric": "optional scoring guidance",
        }
    ],
    "media": [
        {
            "id": "stable identifier",
            "kind": "image | number_line | diagram | figure",
            "src": "optional asset URL or path",
            "alt": "required text alternative",
            "caption": "optional visible caption",
            "params": {"kind-specific, e.g. number_line": "min, max, ticks, highlight"},
        }
    ],
    "passages": [
        {
            "id": "stable identifier",
            "title": "optional passage title",
            "text": "the reading passage text",
            "level": "optional reading level label",
            "decodable_focus": ["optional phonics patterns the passage targets"],
            "questions": ["optional comprehension questions"],
        }
    ],
    "widgets": [
        {
            "id": "instance id, unique within the node",
            "widget": "widget type, e.g. counting_objects or number_line",
            "params": {"widget-specific configuration": "..."},
            "prompt": "optional instruction shown above the widget",
            "target": "optional expected value used by the widget for success feedback",
        }
    ],
    "accommodations": {
        "dyslexia": "",
        "adhd": "",
        "gifted": "",
        "visual_learner": "",
        "kinesthetic_learner": "",
        "auditory_learner": "",
    },
    "time_estimates": {
        "first_exposure": 30,
        "practice_session": 20,
        "review_session": 10,
        "estimated_sessions_to_mastery": 5,
    },
    # choice_space is OPTIONAL. It is the schema hook for PARENT-FINAL,
    # CURRICULUM-AUTHORED, READINESS-INFORMED child choice (governed
    # agency). When ABSENT, the node is fully parent-directed: the child
    # proposes nothing, and the node behaves exactly as it always has.
    # This is why the 182 existing nodes (157 mf + 25 rf) stay valid:
    # they carry no choice_space, and validate_choice_space returns []
    # for any content without one.
    #
    # When PRESENT, choice_space bounds what a child may PROPOSE. The
    # child never gets an open field: every option in proposable[] is one
    # the curriculum authority asserts is acceptable regardless of which
    # the child picks. Consequential decisions (skipping a prerequisite,
    # declaring mastery, leaving a subject) are NEVER child-proposable
    # and the validator REJECTS any choice_space that tries to include
    # one. The parent remains the final authority: proposals route
    # through the existing governance queue, and a per-child parent
    # latitude setting (mirroring the AI input/oversight dial) can widen,
    # tighten, or disable each choice class.
    "choice_space": {
        "proposable": [
            {
                "class": "order | practice_path | practice_variant | pacing_within_bounds",
                "option": "stable id/label of this proposable, all-acceptable option",
                "label": "optional human-readable description of the option",
            }
        ],
        "excluded_note": (
            "required: explicit statement that consequential decisions (prerequisite-skip, "
            "mastery-declaration, subject-exit) are NOT in scope and are never child-proposable"
        ),
        "author_default_latitude": (
            "the curriculum authority's recommended default latitude for this node's choices: "
            "'auto' (low-stakes, apply on proposal) or 'review' (higher-stakes, queue for parent). "
            "May be a single string applying to every class, or a dict mapping class to latitude. "
            "The parent can override this per class; when the parent has set nothing this is the default."
        ),
    },
    # Literary mastery strand: two node shapes live alongside the
    # foundational shape above. lit-craft-NNN nodes follow
    # literary_craft_node; lit-work-NNN and lit-work-inh-NNN nodes
    # follow literary_work_node. Both shapes share a philosophy dict
    # using the foundational per-philosophy native shapes documented
    # above, but only classical and charlotte_mason are required on
    # every literary node; traditional, montessori, and unschooling
    # are included only where genuinely distinct, otherwise the reason
    # is recorded in philosophy_neutral.
    "literary_craft_node": {
        "node_type": "craft",
        "strand": "the craft strand this node sits within, e.g. narrative craft",
        "band": "one of emerging | developing | proficient | advanced | mastery",
        "prerequisites": ["other craft nodes, with band, that must precede this one"],
        "objective": "what the student is to be able to do at this band",
        "core_understanding": "the conceptual content the skill rests upon",
        "analytical_moves": ["the specific reading or thinking moves the skill comprises"],
        "seminar_questions": ["open questions a seminar can sustain on this skill"],
        "writing_invitations": ["writing tasks that exercise and demonstrate the skill"],
        "exemplar_texts": ["texts, referenced not reproduced, in which the skill is at work"],
        "philosophy": {
            "classical": "native classical shape (required)",
            "charlotte_mason": "native charlotte_mason shape (required)",
            "traditional": "optional; native traditional shape when included",
            "montessori": "optional; native montessori shape when included",
            "unschooling": (
                "optional; native unschooling shape when included; no lesson, sequence, or graded-assessment keys"
            ),
        },
        "philosophy_neutral": {
            "<philosophy>": "reason the philosophy is omitted for this node",
        },
    },
    "literary_work_node": {
        "node_type": "work",
        "track": "classics | inheritance",
        "work": {
            "title": "the work's title",
            "author": "the author or attributed source",
            "date": "the work's date or composition window",
            "genre": "the work's genre",
            "form": "the work's literary form",
        },
        "minimum_band": "one of emerging | developing | proficient | advanced | mastery (required)",
        "content_notes": "honest content information, not a gate",
        "craft_focus": ["the craft skills the work especially exercises"],
        "entry": "how the work is met at each band the student brings to it",
        "close_reading_passages": [
            ("referenced passages with opening questions, not answers; never reproduce in-copyright text"),
        ],
        "structural_analysis": "the work's structure and what the structure does",
        "thematic_lines": ["thematic readings held open, competing readings named"],
        "comparative_threads": ["other works the analysis sets this one beside; required non-empty for inheritance"],
        "seminar_questions": ["open questions a seminar can sustain on this work"],
        "writing_invitations": ["writing tasks the work invites at the appropriate band"],
        "context": "supplied as fact; interpretation left to the student",
        "philosophy": {
            "classical": "native classical shape (required)",
            "charlotte_mason": "native charlotte_mason shape (required)",
            "traditional": "optional; native traditional shape when included",
            "montessori": "optional; native montessori shape when included",
            "unschooling": (
                "optional; native unschooling shape when included; no lesson, sequence, or graded-assessment keys"
            ),
        },
        "philosophy_neutral": {
            "<philosophy>": "reason the philosophy is omitted for this node",
        },
        "lineage": "required for inheritance track; absent on classics track",
    },
    # Trades and skilled work: three node shapes per the design in
    # docs/curriculum/METHEAN_trades_design.md. A trade has one root
    # node (trade_root_node) carrying the trade-level defaults; one or
    # more safety competencies (trade_safety_competency) at the entry of
    # the trade's DAG; and many technique competencies
    # (trade_technique_competency) for the hands-on doing. Trades do not
    # carry the five-philosophy block; they carry a single apprenticeship
    # pedagogy block. Safety is gating: every hands-on competency has a
    # prerequisite edge to the trade's safety node.
    "trade_root_node": {
        "node_type": "root",
        "trade": "the trade id, matching SUBJECT_CATALOG['vocational']",
        "trade_name": "human-readable trade name",
        "description": "what the trade covers and how it is taught here",
        "default_supervision_policy": {
            "hand_tool_work": "supervision default through which band",
            "power_tool_work": "supervision default through which band",
        },
        "safety_node": "id of the trade's entry safety competency",
        "progression_bands": ["helper", "apprentice", "journeyman", "qualified"],
    },
    "trade_safety_competency": {
        "node_type": "safety",
        "trade": "the trade id",
        "competency_name": "what the safety competency teaches",
        "progression_band": "helper",
        "prerequisites": ["no prereqs: safety is the root of the trade DAG"],
        "safety_basis": {
            "hazards": ["the actual hazards in this shop"],
            "ppe_required": ["the PPE the learner must wear / not wear, with reasons"],
            "supervision_required": "true: a safety competency is always supervised",
            "supervision_basis": "why and to what standard",
            "fresh_safety_signoff_within_days": (
                "null on the safety node itself; dependent competencies set their own freshness window"
            ),
        },
        "tools_required": ["the safety equipment of the shop, not the work tools"],
        "workspace_requirements": {"surface": "...", "lighting": "...", "containment": "..."},
        "skill_description": "what the learner must know and demonstrate they can do for safety",
        "demonstration_criteria": ["measurable on the walkthrough itself"],
        "common_errors": [{"error": "...", "cause": "...", "remedy": "..."}],
        "artifact_expected": {
            "type": "photo | video | document | audio",
            "what_to_capture": "...",
            "what_the_evidence_shows": "...",
        },
        "mentor_signoff_required": "true: no self-attestation on safety",
        "pedagogy": {"i_do": "...", "we_do": "...", "you_do_supervised": "...", "you_do_unsupervised": "..."},
        "estimated_practice_sessions_to_signoff": 2,
        "signoff_validity_days": "annual re-walkthrough as the freshness check",
        "related_projects": [],
    },
    "trade_technique_competency": {
        "node_type": "technique",
        "trade": "the trade id",
        "competency_name": "the doing-shaped name of the skill",
        "progression_band": "helper | apprentice | journeyman | qualified",
        "prerequisites": [
            "must include the trade safety node",
            "and any technique competencies this one builds on",
        ],
        "safety_basis": {
            "hazards": ["named hazards specific to this technique"],
            "ppe_required": ["PPE list with reasons; honest about what is optional vs forbidden"],
            "supervision_required": ("true whenever a cutting tool is used; the validator enforces this"),
            "supervision_basis": "why and to what standard; named threshold for stepping back",
            "fresh_safety_signoff_within_days": (
                "int days: planner refuses to schedule if the trade's safety_check is stale"
            ),
        },
        "tools_required": [
            {"name": "...", "specification": "...", "alternatives": ["..."]},
        ],
        "materials_required": [
            {"name": "...", "quantity": "...", "approximate_cost_usd": "number or null"},
        ],
        "workspace_requirements": {
            "surface": "...",
            "ventilation": "...",
            "lighting": "...",
            "power": "...",
            "containment": "...",
        },
        "skill_description": "plain prose, one paragraph, what the doing looks like in the hand",
        "demonstration_criteria": [
            "each criterion measurable on the work itself (e.g. 'kerf within 1/32 inch of the line')",
        ],
        "common_errors": [{"error": "...", "cause": "...", "remedy": "..."}],
        "artifact_expected": {
            "type": "photo | video | document | audio",
            "what_to_capture": "...",
            "what_the_evidence_shows": "...",
        },
        "mentor_signoff_required": "true at apprentice and above; false at helper",
        "pedagogy": {
            "i_do": "mentor demonstrates with narration",
            "we_do": "mentor and learner share the work, with named transition points",
            "you_do_supervised": "learner performs, mentor watching, with intervention thresholds",
            "you_do_unsupervised": "the conditions under which the learner can work alone",
        },
        "estimated_practice_sessions_to_signoff": 6,
        "session_length_minutes": 30,
        "related_projects": ["ids of project nodes that exercise this competency"],
    },
    # Certification preparation: study-only nodes that map a trade's
    # competencies and bands to a real, externally administered credential
    # (federal, state, or industry). METHEAN prepares understanding and a
    # portfolio toward the credential; the exam and any required supervised
    # hours are taken through the official body, never administered by
    # METHEAN. No reproduced exam content. The shape is enforced by
    # validate_competency: credential_body must be named, a deferral
    # statement (exam_taken_through or exam_administration_deferred_to)
    # must be present, and reproduced-exam fields are rejected.
    "trade_certification_prep": {
        "node_type": "certification_prep",
        "trade": "the trade id",
        "credential_name": "the official name of the credential, exactly as the body names it",
        "credential_body": "the official organization that administers the credential (e.g. 'U.S. Environmental Protection Agency')",
        "credential_body_url": "optional; the official URL of the credential body (no fabricated URLs)",
        "authorizing_scope": "in plain language, what the credential legally authorizes the holder to do",
        "knowledge_domains_covered": [
            "general list of domains the official body publishes as covered by the credential; not reproduced exam content",
        ],
        "eligibility": {
            "minimum_age": "per the credential body's published rules; null if none",
            "experience_requirements": "per the credential body; varies",
            "prerequisites": ["list per the credential body"],
        },
        "exam_format_general": "general description (multiple choice, practical demo, oral, etc.); never specific questions",
        "legal_status": "legally_required | optional | jurisdiction_specific",
        "prepares_understanding_only": "true; this node prepares understanding only, does not administer the exam",
        "exam_taken_through": "the official body or its authorized testing partners; not METHEAN",
        "supervised_hours_through": "official apprenticeship / vocational program / employer; not METHEAN; null if no hours requirement",
        "progression_band": "the trades progression band at which the learner is genuinely ready for this credential",
        "where_in_ladder": "human-readable placement (e.g. 'late apprentice; before any refrigerant hands-on')",
        "aligned_competencies": ["ids of competencies in this trade that build toward this credential"],
        "study_resources_pointers": [
            "names of official study materials published by the credential body or recognized publishers; not reproduced",
        ],
        "mentor_model": "AI tutor mentors end-to-end (study, not hands-on)",
        "safety_review": {
            "reviewed": "false by default; set true by a qualified human reviewer with credentials in this trade and (where applicable) legal counsel",
            "reviewer": "name and credentials",
            "reviewed_on": "ISO 8601 date",
            "standard_refs": ["named standards and authorities, never reproduced text"],
        },
    },
}


def is_enriched(content: dict | None) -> bool:
    """Check if a node's content has been enriched (not empty/minimal)."""
    if not content:
        return False
    return bool(content.get("learning_objectives")) and bool(content.get("teaching_guidance"))


def validate_content(content: dict) -> list[str]:
    """Return list of missing required fields."""
    issues = []
    if not content.get("learning_objectives"):
        issues.append("learning_objectives missing")
    if not content.get("teaching_guidance"):
        issues.append("teaching_guidance missing")
    if not content.get("assessment_criteria"):
        issues.append("assessment_criteria missing")
    return issues


def validate_media(content: dict) -> list[str]:
    """Return non-fatal warnings about media and passage blocks.

    This never raises and never rejects content. Legacy nodes without
    media or passages produce no warnings. Flags media blocks missing
    the required alt text, passages missing text, and duplicate media
    or passage ids.
    """
    warnings: list[str] = []

    seen_media_ids: set[str] = set()
    for i, block in enumerate(content.get("media", []) or []):
        if not block.get("alt"):
            warnings.append(f"media[{i}] missing alt text")
        block_id = block.get("id")
        if block_id is not None:
            if block_id in seen_media_ids:
                warnings.append(f"duplicate media id: {block_id}")
            seen_media_ids.add(block_id)

    seen_passage_ids: set[str] = set()
    for i, passage in enumerate(content.get("passages", []) or []):
        if not passage.get("text"):
            warnings.append(f"passage[{i}] missing text")
        passage_id = passage.get("id")
        if passage_id is not None:
            if passage_id in seen_passage_ids:
                warnings.append(f"duplicate passage id: {passage_id}")
            seen_passage_ids.add(passage_id)

    return warnings


def validate_widgets(content: dict) -> list[str]:
    """Return non-fatal warnings about interactive widget blocks.

    This never raises and never rejects content. Legacy nodes without
    widgets produce no warnings. Flags widgets missing an id or widget
    type, duplicate instance ids, and params that are present but not
    a dict. The set of widget types is intentionally open: the
    frontend widget registry is the source of truth for renderable
    types, and unknown types degrade gracefully there.
    """
    warnings: list[str] = []

    seen_ids: set[str] = set()
    for i, widget in enumerate(content.get("widgets", []) or []):
        widget_id = widget.get("id")
        if not widget_id:
            warnings.append(f"widget[{i}] missing id")
        elif widget_id in seen_ids:
            warnings.append(f"duplicate widget id: {widget_id}")
        else:
            seen_ids.add(widget_id)

        if not widget.get("widget"):
            warnings.append(f"widget[{i}] missing widget type")

        params = widget.get("params")
        if params is not None and not isinstance(params, dict):
            warnings.append(f"widget[{i}] params is not a dict")

    return warnings


# Lesson, sequence, and assessment keys that must never appear in an
# unschooling philosophy variant: their presence contradicts the
# philosophy, which has no lessons, no fixed sequence, and no tests.
_UNSCHOOLING_FORBIDDEN_KEYS: frozenset[str] = frozenset(
    {
        "gradual_release",
        "i_do",
        "we_do",
        "you_do",
        "guided_practice",
        "independent_practice",
        "mastery_check",
        "spiral_review",
        "scaffolding",
        "assessment",
        "lesson",
        "sequence",
    }
)


def validate_philosophy(content: dict) -> list[str]:
    """Return warnings and hard-fail errors for philosophy_specific.

    Mirrors validate_content and validate_media: it returns a list of
    strings and never raises. Entries prefixed "warning:" are advisory;
    entries prefixed "error:" are hard failures the authoring pipeline
    must not ship.

    - A plain-string variant is a legacy, un-upgraded form. It is
      valid, but flagged with a warning so it can be upgraded to its
      native per-philosophy shape.
    - An unschooling variant must never carry a lesson, sequence, or
      assessment key. That contradicts the philosophy, so it is a hard
      failure that protects the philosophy's integrity.

    Field completeness is not enforced here: the per-philosophy shapes
    are advisory, so an optional field (the classical copywork field,
    for example, is omitted for oral or pre-print skills) is never
    treated as missing.
    """
    issues: list[str] = []

    philosophy_specific = content.get("philosophy_specific", {})
    if not isinstance(philosophy_specific, dict):
        return issues

    for philosophy, variant in philosophy_specific.items():
        if isinstance(variant, str):
            issues.append(f"warning: philosophy_specific[{philosophy}] is a legacy string variant")
            continue
        if philosophy == "unschooling" and isinstance(variant, dict):
            forbidden = sorted(_UNSCHOOLING_FORBIDDEN_KEYS.intersection(variant.keys()))
            if forbidden:
                issues.append(
                    "error: unschooling variant must not contain lesson, sequence, or "
                    f"assessment keys (found: {', '.join(forbidden)})"
                )

    return issues


# ---- Governed-agency choice_space validation --------------------------
#
# choice_space is the schema hook for PARENT-FINAL, CURRICULUM-AUTHORED,
# READINESS-INFORMED child choice. The validator here is the safety gate:
# it never raises (mirrors validate_media / validate_philosophy), returns
# "error:"-prefixed entries for hard violations the authoring pipeline
# must not ship, and "warning:"-prefixed entries for advisories. A node
# with NO choice_space yields [] (absent means fully parent-directed),
# which is what keeps every existing node valid.

# The bounded set of choice classes a child may PROPOSE within. Each is a
# choice among all-acceptable outcomes, never a consequential decision.
PROPOSABLE_CHOICE_CLASSES: frozenset[str] = frozenset(
    {
        "order",  # the order in which equally-ready items are met
        "practice_path",  # which of several acceptable practice paths to take
        "practice_variant",  # which variant of an activity to do
        "pacing_within_bounds",  # pacing choices that stay inside authored bounds
    }
)

# The latitude values a choice class can carry. "auto" applies a proposal
# immediately; "review" queues it for the parent; "disabled" removes child
# proposability for that class entirely. Author defaults use auto/review;
# a parent may additionally set "disabled".
CHOICE_LATITUDES: frozenset[str] = frozenset({"auto", "review", "disabled"})
AUTHOR_DEFAULT_LATITUDES: frozenset[str] = frozenset({"auto", "review"})

# The consequential decisions that are NEVER child-proposable. A
# choice_space whose proposable[] names any of these (by class or by
# option token) is REJECTED. These are the decisions that must stay with
# the parent / governance layer: skipping a prerequisite, declaring
# mastery, and leaving a subject.
CONSEQUENTIAL_DECISION_TOKENS: frozenset[str] = frozenset(
    {
        "prerequisite_skip",
        "prerequisite-skip",
        "skip_prerequisite",
        "skip-prerequisite",
        "mastery_declaration",
        "mastery-declaration",
        "declare_mastery",
        "declare-mastery",
        "subject_exit",
        "subject-exit",
        "exit_subject",
        "exit-subject",
        "leave_subject",
        "leave-subject",
    }
)


def _names_consequential_decision(value: object) -> bool:
    """Return True if a class/option string names a consequential decision.

    Matches the canonical consequential-decision tokens as substrings of a
    normalized (lowercased, whitespace-to-underscore) string, so that
    "skip prerequisite", "skip_prerequisite", and "prerequisite-skip" are
    all caught.
    """
    if not isinstance(value, str):
        return False
    normalized = "_".join(value.lower().split())
    return any(token in normalized for token in CONSEQUENTIAL_DECISION_TOKENS)


def validate_choice_space(content: dict) -> list[str]:
    """Validate the optional choice_space block of a node.

    Returns a list of strings, possibly empty, and NEVER raises. Entries
    prefixed "error:" are hard failures the authoring pipeline must not
    ship; entries prefixed "warning:" are advisory.

    The guarantees that keep every existing node valid:

    - content with NO choice_space returns [] (absent means the node is
      fully parent-directed; this is the safe default).
    - a choice_space that is not a dict is a single hard error.

    The safety invariants enforced as hard errors:

    - every proposable[] entry must be a dict carrying a class and an
      option;
    - NO proposable entry may name a consequential decision
      (prerequisite-skip, mastery-declaration, subject-exit) by class or
      by option: such a choice_space is REJECTED;
    - excluded_note must be present and non-empty (the explicit statement
      that consequential decisions are out of scope).

    Advisory warnings:

    - an unknown choice class (not one of PROPOSABLE_CHOICE_CLASSES);
    - an author_default_latitude outside {auto, review} (single value or
      per-class dict value);
    - an empty proposable list.
    """
    issues: list[str] = []

    choice_space = content.get("choice_space")
    if choice_space is None:
        # Absent means fully parent-directed. This is the safe default and
        # the reason existing nodes stay valid.
        return issues
    if not isinstance(choice_space, dict):
        return ["error: choice_space must be a dict when present"]

    proposable = choice_space.get("proposable")
    if proposable is None or not isinstance(proposable, list):
        issues.append("error: choice_space.proposable must be a list")
        proposable = []
    elif not proposable:
        issues.append("warning: choice_space.proposable is empty (no child-proposable options)")

    for i, entry in enumerate(proposable):
        if not isinstance(entry, dict):
            issues.append(f"error: choice_space.proposable[{i}] must be a dict")
            continue
        choice_class = entry.get("class")
        option = entry.get("option")
        if not choice_class:
            issues.append(f"error: choice_space.proposable[{i}] missing class")
        if not option:
            issues.append(f"error: choice_space.proposable[{i}] missing option")
        # The core safety gate: reject any consequential decision, whether
        # it is smuggled in via the class or via the option.
        if _names_consequential_decision(choice_class) or _names_consequential_decision(option):
            issues.append(
                f"error: choice_space.proposable[{i}] names a consequential decision "
                "(prerequisite-skip, mastery-declaration, or subject-exit); these are never "
                "child-proposable and must be excluded from any choice_space"
            )
        elif isinstance(choice_class, str) and choice_class not in PROPOSABLE_CHOICE_CLASSES:
            issues.append(
                f"warning: choice_space.proposable[{i}] has unknown class {choice_class!r}; "
                f"expected one of {sorted(PROPOSABLE_CHOICE_CLASSES)}"
            )

    excluded_note = choice_space.get("excluded_note")
    if not isinstance(excluded_note, str) or not excluded_note.strip():
        issues.append(
            "error: choice_space.excluded_note is required and must explicitly state that "
            "consequential decisions (prerequisite-skip, mastery-declaration, subject-exit) "
            "are not in scope and never child-proposable"
        )

    default_latitude = choice_space.get("author_default_latitude")
    if default_latitude is not None:
        if isinstance(default_latitude, str):
            if default_latitude not in AUTHOR_DEFAULT_LATITUDES:
                issues.append(
                    f"warning: choice_space.author_default_latitude {default_latitude!r} is not one of "
                    f"{sorted(AUTHOR_DEFAULT_LATITUDES)}"
                )
        elif isinstance(default_latitude, dict):
            for cls, lat in default_latitude.items():
                if lat not in AUTHOR_DEFAULT_LATITUDES:
                    issues.append(
                        f"warning: choice_space.author_default_latitude[{cls!r}] = {lat!r} is not one of "
                        f"{sorted(AUTHOR_DEFAULT_LATITUDES)}"
                    )
        else:
            issues.append("warning: choice_space.author_default_latitude must be a string or a dict")

    return issues


def choice_space_is_valid(content: dict) -> bool:
    """Return True iff the node's choice_space has no hard (error:) failures.

    A node with no choice_space is valid (fully parent-directed). This is
    the boolean the governance/runtime path consults before honoring any
    child proposal against the node.
    """
    return not any(issue.startswith("error:") for issue in validate_choice_space(content))


# ---- Literary mastery validation --------------------------------------

LITERARY_BANDS: frozenset[str] = frozenset({"emerging", "developing", "proficient", "advanced", "mastery"})
LITERARY_TRACKS: frozenset[str] = frozenset({"classics", "inheritance"})

# Heuristic public-domain cutoff (US): works whose latest indicated
# year is at or after this are treated as plausibly in copyright and
# subject to the long-passage review flag. Ancient works that carry no
# 4-digit year (e.g. "c. 8th century BCE") are treated as public domain.
_PUBLIC_DOMAIN_CUTOFF_YEAR = 1928

# Threshold (in characters) above which a single string in
# close_reading_passages on an in-copyright work is flagged for human
# review. Short, descriptive prose ("a Homeric simile, for how it
# works") passes; multi-paragraph quoted passages trip the flag.
_CLOSE_READING_PASSAGE_LIMIT = 400


def _latest_year_in(date_text: str) -> int | None:
    import re

    years = [int(m) for m in re.findall(r"\b(\d{4})\b", date_text)]
    return max(years) if years else None


def _is_in_copyright(work: dict) -> bool:
    """Conservative heuristic: a work is treated as in copyright if
    its date string contains a 4-digit year at or after the public-
    domain cutoff. Ancient works with no 4-digit year pass as public
    domain.
    """
    if not isinstance(work, dict):
        return False
    date_text = str(work.get("date", ""))
    year = _latest_year_in(date_text)
    return year is not None and year >= _PUBLIC_DOMAIN_CUTOFF_YEAR


def validate_literature(content: dict, authored_nodes: dict | None = None) -> list[str]:
    """Validate a literary mastery node.

    Returns a list of warnings, possibly empty. Raises ValueError on
    the hard violations the authoring pipeline must not ship:

    - a work node missing minimum_band, or an inheritance work node
      missing lineage or with empty comparative_threads;
    - any node whose philosophy dict lacks classical or charlotte_mason;
    - any unschooling variant containing lesson, sequence, or
      graded-assessment keys (the same rule as foundational
      unschooling, lifted to a hard fail here because the literary
      strand has no legacy form to upgrade).

    Warnings are advisory:

    - unknown band or track values;
    - on in-copyright work nodes, any close_reading_passages entry
      longer than _CLOSE_READING_PASSAGE_LIMIT characters, flagged
      for human review against the no-full-reproduction rule. Public-
      domain works may quote accurately and never trigger this flag;
    - on craft nodes, any prerequisite string that does not resolve
      against authored_nodes, when authored_nodes is supplied. A
      prerequisite resolves if it is the id of an authored node, or
      a "{strand}: {band}" string matching some authored craft node.
      When authored_nodes is None the check is skipped.
    """
    if not isinstance(content, dict):
        raise ValueError("literary node content must be a dict")

    warnings: list[str] = []
    node_type = content.get("node_type")
    if node_type not in {"craft", "work"}:
        raise ValueError(f"literary node_type must be 'craft' or 'work' (got {node_type!r})")

    if node_type == "work":
        minimum_band = content.get("minimum_band")
        if minimum_band is None:
            raise ValueError("work node missing minimum_band")
        if minimum_band not in LITERARY_BANDS:
            warnings.append(f"warning: unknown minimum_band {minimum_band!r}; expected one of {sorted(LITERARY_BANDS)}")
    else:
        band = content.get("band")
        if band is not None and band not in LITERARY_BANDS:
            warnings.append(f"warning: unknown band {band!r}; expected one of {sorted(LITERARY_BANDS)}")

    if node_type == "work":
        track = content.get("track")
        if track not in LITERARY_TRACKS:
            warnings.append(f"warning: unknown track {track!r}; expected one of {sorted(LITERARY_TRACKS)}")
        if track == "inheritance":
            if not content.get("lineage"):
                raise ValueError("inheritance work node missing lineage")
            if not content.get("comparative_threads"):
                raise ValueError("inheritance work node has empty comparative_threads")

    philosophy = content.get("philosophy")
    if not isinstance(philosophy, dict):
        raise ValueError("literary node philosophy must be a dict")
    missing_required = [p for p in ("classical", "charlotte_mason") if p not in philosophy]
    if missing_required:
        raise ValueError(
            "literary node philosophy must include classical and charlotte_mason "
            f"(missing: {', '.join(missing_required)})"
        )

    unschooling = philosophy.get("unschooling")
    if isinstance(unschooling, dict):
        forbidden = sorted(_UNSCHOOLING_FORBIDDEN_KEYS.intersection(unschooling.keys()))
        if forbidden:
            raise ValueError(
                "unschooling variant must not contain lesson, sequence, or "
                f"graded-assessment keys (found: {', '.join(forbidden)})"
            )

    if node_type == "work":
        work = content.get("work") or {}
        if _is_in_copyright(work):
            passages = content.get("close_reading_passages") or []
            for i, passage in enumerate(passages):
                if isinstance(passage, str):
                    text = passage
                elif isinstance(passage, dict):
                    text = str(passage.get("text", ""))
                else:
                    text = ""
                if len(text) > _CLOSE_READING_PASSAGE_LIMIT:
                    warnings.append(
                        f"warning: close_reading_passages[{i}] is {len(text)} chars on an "
                        "in-copyright work; review for reproduced passage"
                    )

    if node_type == "craft" and authored_nodes is not None:
        prereqs = content.get("prerequisites") or []
        if prereqs:
            authored_ids = set(authored_nodes.keys())
            valid_pairs: set[str] = set()
            for other in authored_nodes.values():
                if not isinstance(other, dict):
                    continue
                if other.get("node_type") != "craft":
                    continue
                other_strand = other.get("strand")
                other_band = other.get("band")
                if isinstance(other_strand, str) and isinstance(other_band, str):
                    valid_pairs.add(f"{other_strand}: {other_band}")
            for prereq in prereqs:
                if not isinstance(prereq, str):
                    continue
                if prereq in authored_ids:
                    continue
                if prereq in valid_pairs:
                    continue
                warnings.append(
                    f"warning: prerequisite {prereq!r} does not resolve to any authored node id or strand:band"
                )

    return warnings


# Trades and skilled work validation.
#
# Three node shapes are validated through validate_competency: the trade
# root node (node_type "root"), the trade safety competency (node_type
# "safety"), and the trade technique competency (node_type "technique").
# Safety is gating: a technique competency must carry safety_basis, must
# prereq the trade safety node when authored_nodes is supplied, must
# carry demonstration_criteria, and if it uses a cutting tool must set
# supervision_required to True. These are hard checks that raise.

TRADES_BANDS: frozenset[str] = frozenset({"helper", "apprentice", "journeyman", "qualified"})
TRADES_NODE_TYPES: frozenset[str] = frozenset({"root", "safety", "technique", "knowledge", "certification_prep"})

# Substring keywords (case-insensitive) that mark a tool as a cutting
# tool. A technique competency listing any tool whose name contains one
# of these must set supervision_required True. Conservative on purpose:
# any tool with a real edge gets supervision until the learner is signed
# off; the planner enforces the schedule, the mentor enforces the work.
_CUTTING_TOOL_KEYWORDS: frozenset[str] = frozenset(
    {
        "saw",
        "chisel",
        "knife",
        "plane",
        "drill",
        "axe",
        "hatchet",
        "auger",
        "spokeshave",
        "scraper",
        "router",
        "gouge",
        "adze",
        "drawknife",
        "froe",
    }
)


def _technique_uses_cutting_tool(tools_required: list) -> bool:
    if not isinstance(tools_required, list):
        return False
    for tool in tools_required:
        if isinstance(tool, dict):
            name = tool.get("name", "")
        elif isinstance(tool, str):
            name = tool
        else:
            continue
        if not isinstance(name, str):
            continue
        name_lower = name.lower()
        for keyword in _CUTTING_TOOL_KEYWORDS:
            if keyword in name_lower:
                return True
    return False


def validate_competency(content: dict, authored_nodes: dict | None = None) -> list[str]:
    """Validate a trades competency node.

    Returns a list of warnings, possibly empty. Raises ValueError on the
    hard violations the trades pipeline must not ship:

    - content must be a dict;
    - node_type must be one of root | safety | technique | knowledge | certification_prep;
    - on safety and technique competencies, progression_band must be one of helper | apprentice | journeyman | qualified;
    - a technique competency must carry safety_basis (a dict);
    - a technique competency must carry a non-empty demonstration_criteria list;
    - a technique competency listing any cutting tool in tools_required must set safety_basis.supervision_required to True;
    - when authored_nodes is supplied, a technique competency's prerequisites must include the trade's safety node id (the authored node with node_type "safety" and matching trade);
    - when authored_nodes is supplied, every prerequisite string must resolve to an authored node id.

    Warnings are advisory: missing artifact_expected on a technique, missing common_errors, unknown progression_band.
    """
    if not isinstance(content, dict):
        raise ValueError("trades node content must be a dict")

    warnings: list[str] = []
    node_type = content.get("node_type")
    if node_type not in TRADES_NODE_TYPES:
        raise ValueError(f"trades node_type must be one of {sorted(TRADES_NODE_TYPES)} (got {node_type!r})")

    if node_type in {"safety", "technique", "knowledge"}:
        band = content.get("progression_band")
        if band is None:
            raise ValueError(f"{node_type} competency missing progression_band")
        if band not in TRADES_BANDS:
            warnings.append(f"warning: unknown progression_band {band!r}; expected one of {sorted(TRADES_BANDS)}")

    if node_type == "technique":
        safety_basis = content.get("safety_basis")
        if not isinstance(safety_basis, dict):
            raise ValueError("technique competency missing safety_basis (must be a dict)")
        demonstration_criteria = content.get("demonstration_criteria")
        if not isinstance(demonstration_criteria, list) or not demonstration_criteria:
            raise ValueError("technique competency missing demonstration_criteria (must be a non-empty list)")
        tools_required = content.get("tools_required", [])
        if _technique_uses_cutting_tool(tools_required):
            supervision = safety_basis.get("supervision_required")
            if supervision is not True:
                raise ValueError(
                    "technique competency uses a cutting tool but safety_basis.supervision_required is not True"
                )
        if not content.get("artifact_expected"):
            warnings.append("warning: technique competency missing artifact_expected")
        if not content.get("common_errors"):
            warnings.append("warning: technique competency missing common_errors")

    if node_type == "safety":
        if not isinstance(content.get("safety_basis"), dict):
            raise ValueError("safety competency missing safety_basis (must be a dict)")
        if not content.get("demonstration_criteria"):
            raise ValueError("safety competency missing demonstration_criteria")
        if content.get("mentor_signoff_required") is not True:
            raise ValueError("safety competency must set mentor_signoff_required True (no self-attestation on safety)")

    if node_type == "root":
        if not content.get("trade"):
            raise ValueError("trade root node missing trade")
        if not content.get("safety_node"):
            raise ValueError("trade root node missing safety_node (id of the entry safety competency)")

    if node_type == "certification_prep":
        # certification_prep nodes prepare understanding toward a real,
        # externally administered credential. They must name the credential
        # body, must defer the exam to the body, and must not reproduce
        # exam content. This validator enforces those rules so the trades
        # pipeline cannot ship a node that implies METHEAN administers the
        # exam or that contains copyrighted/regulated exam material.
        credential_body = content.get("credential_body")
        if not isinstance(credential_body, str) or not credential_body.strip():
            raise ValueError(
                "certification_prep node must name credential_body "
                "(the official organization that administers the credential)"
            )
        if not content.get("credential_name"):
            raise ValueError("certification_prep node must name credential_name")
        if not content.get("authorizing_scope"):
            raise ValueError(
                "certification_prep node must state authorizing_scope "
                "(what the credential legally authorizes the holder to do)"
            )
        # The deferral statement is required: either an exam_taken_through
        # field or an explicit exam_administration_deferred_to field, naming
        # who the exam is taken through (always external to METHEAN).
        deferral_present = bool(content.get("exam_taken_through") or content.get("exam_administration_deferred_to"))
        if not deferral_present:
            raise ValueError(
                "certification_prep node must defer exam administration: "
                "set exam_taken_through (or exam_administration_deferred_to) "
                "naming the official body or its authorized testing partners"
            )
        # The understanding-only flag must be explicitly true if present;
        # absence is acceptable (the schema names it as a documentation
        # field). Presence with any non-true value is rejected, to prevent
        # silent claims that METHEAN administers the credential.
        understanding_only = content.get("prepares_understanding_only")
        if understanding_only is not None and understanding_only is not True:
            raise ValueError(
                "certification_prep node prepares_understanding_only must be True "
                "if present (no implicit claim that METHEAN administers the exam)"
            )
        # Prohibited fields: any field whose name suggests reproduced exam
        # content. The presence of any such field is a hard fail; the node
        # must describe knowledge domains generally and point to the
        # credential body's own materials, not reproduce them.
        prohibited_field_names = {
            "exam_questions",
            "exam_content",
            "reproduced_exam",
            "sample_questions",
            "practice_exam_questions",
            "exam_answer_key",
        }
        for prohibited in prohibited_field_names:
            if prohibited in content:
                raise ValueError(
                    f"certification_prep node must not contain field {prohibited!r}; "
                    "this trade does not reproduce or administer exam content"
                )

    if authored_nodes is not None and node_type in {"safety", "technique", "knowledge"}:
        prereqs = content.get("prerequisites") or []
        authored_ids = set(authored_nodes.keys())
        for prereq in prereqs:
            if not isinstance(prereq, str):
                continue
            if prereq not in authored_ids:
                warnings.append(f"warning: prerequisite {prereq!r} does not resolve to any authored node id")
        if node_type == "technique":
            trade = content.get("trade")
            safety_node_id: str | None = None
            for other_id, other in authored_nodes.items():
                if not isinstance(other, dict):
                    continue
                if other.get("node_type") == "safety" and other.get("trade") == trade:
                    safety_node_id = other_id
                    break
            if safety_node_id is None:
                warnings.append(f"warning: no authored safety competency for trade {trade!r} in authored_nodes")
            elif safety_node_id not in prereqs:
                raise ValueError(
                    f"technique competency for trade {trade!r} must prerequisite the trade "
                    f"safety node {safety_node_id!r}; prerequisites are {prereqs!r}"
                )

    # safety_review marker: a node may carry an optional safety_review block
    # of the shape {reviewed: bool, reviewer: str|null, reviewed_on: str|null,
    # standard_refs: list}. The only hard rule here is that reviewed True
    # without a named reviewer and a reviewed_on date is not accepted; that
    # rules out blank or self-claimed verification.
    review = content.get("safety_review")
    if isinstance(review, dict) and review.get("reviewed") is True:
        if not review.get("reviewer") or not review.get("reviewed_on"):
            raise ValueError(
                "safety_review.reviewed is True but reviewer or reviewed_on is empty; "
                "no blank or self-claimed verification"
            )

    return warnings


def requires_human_safety_review(node: dict) -> bool:
    """Return True iff this node must carry a current human safety review before it can be surfaced to a learner.

    True for any safety competency, and for any node whose
    safety_basis.supervision_required is True. The intent is gating: any
    node that requires a human watching the work also requires a human
    reviewing the content.

    TODO (integration): learning_context (and the planner) must refuse to
    surface any activity whose node returns True from this function while
    the node's safety_review.reviewed is False. That enforcement gate is
    deferred to the integration task; it does not live in this module.
    This helper exists now so the gate has a single, documented source of
    truth when it is wired.
    """
    if not isinstance(node, dict):
        return False
    if node.get("node_type") == "safety":
        return True
    safety_basis = node.get("safety_basis") or {}
    return bool(safety_basis.get("supervision_required"))


def is_cleared_for_surfacing(content: dict | None) -> bool:
    """Return True iff this node's content is cleared to be surfaced to a learner.

    Cleared iff EITHER:
    - the node does not require human safety review (requires_human_safety_review returns False), OR
    - the node requires human safety review AND its safety_review block is a
      well-formed dict AND safety_review.reviewed is exactly the boolean True.

    Fail-closed: any other state on safety_review.reviewed for a node that
    requires review (False, None, missing, non-bool truthy, malformed
    safety_review) means NOT cleared. This is the content-review gate.

    This function is intentionally pure: it takes a content dict and
    returns a bool, with no side effects and no I/O. It is the single
    source of truth the surfacing path consults before serving a node.

    Note: this is the CONTENT-REVIEW gate. For nodes where the supervision
    policy names a qualified human physically present at a live moment
    (see requires_qualified_human_present_at_runtime), this gate is
    necessary but NOT sufficient; the higher governance layer must
    additionally confirm the qualified human at session time.
    """
    if not isinstance(content, dict):
        # A non-dict content payload cannot itself be a hazardous-node
        # payload (the validator would reject it). Surfacing falls back
        # to the title-only path; not blocked here.
        return True
    if not requires_human_safety_review(content):
        return True
    review = content.get("safety_review")
    if not isinstance(review, dict):
        return False
    # Strict boolean True only; truthy strings ("true"), 1, etc. do NOT clear.
    return review.get("reviewed") is True


def requires_qualified_human_present_at_runtime(content: dict | None) -> bool:
    """Return True iff this node's supervision policy names a qualified human
    physically present at a live or otherwise irreducibly hazardous moment.

    Signal in authored content: the literal phrase "physically present"
    (case-insensitive) in safety_basis.supervision_basis, paired with a
    named qualified-human role (licensed electrician, licensed HVAC
    technician, licensed gas fitter, EPA-608-certified person, or
    qualified human). The authoring discipline uses these phrases
    consistently; see hc-021 and elc-021 for the canonical pattern.

    The content-review gate (is_cleared_for_surfacing) is NECESSARY but
    NOT SUFFICIENT for nodes where this function returns True. The
    runtime governance layer must additionally confirm a qualified human
    is present at the work before the activity is surfaced. This
    function is the documented seam: it identifies which nodes need the
    runtime check; the actual confirmation is enforced by the governance
    layer (not by this module).

    TODO (governance integration): wire a runtime presence check at the
    activity-surfacing layer that:
      1. Reads this function on the node's content.
      2. If True, requires a session-time record (signed by a parent /
         governance signer / the qualified human themself) that a
         qualified human matching the named role is confirmed present.
      3. Refuses to surface the activity until that record is present
         and current for the session.
    The check is NOT implemented in this module; this helper names the
    seam so the higher layer knows where to wire it.
    """
    if not isinstance(content, dict):
        return False
    safety_basis = content.get("safety_basis")
    if not isinstance(safety_basis, dict):
        return False
    basis = safety_basis.get("supervision_basis", "")
    if not isinstance(basis, str):
        return False
    basis_lower = basis.lower()
    if "physically present" not in basis_lower:
        return False
    qualified_human_phrases = (
        "licensed electrician",
        "licensed hvac technician",
        "licensed gas fitter",
        "608-certified",
        "epa-608",
        "qualified human",
    )
    return any(phrase in basis_lower for phrase in qualified_human_phrases)
