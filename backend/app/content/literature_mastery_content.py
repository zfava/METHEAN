"""Literary mastery strand content.

Two node shapes live here: lit-craft-NNN (craft spine) and
lit-work-NNN / lit-work-inh-NNN (Western classics and the inheritance
canon). The schemas and validation are in app.services.node_content;
see literary_craft_node and literary_work_node in NODE_CONTENT_SCHEMA
and validate_literature.

Philosophy handling follows Option B: every node includes classical
and charlotte_mason as native dicts; the other philosophies are
included only where genuinely distinct, and otherwise recorded with a
reason in philosophy_neutral. Unschooling variants never carry lesson,
sequence, or graded-assessment keys.
"""

LITERATURE_MASTERY_CONTENT: dict[str, dict] = {}
