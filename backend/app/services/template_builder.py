"""Compact builder for curriculum domain templates.

Defines a small DSL on top of `Template` / `TemplateNode` / `TemplateEdge`
so new domains can be expressed as a dict with tuple-encoded nodes and
edges, instead of 600+ lines of explicit dataclass construction.

The dict shape:

    {
        "subject": "Subject Name",
        "color": "#HEXCOLOR",
        "assessment_type": "observed",   # default for all nodes
        "unit": "boolean",                # default measurement_unit
        "tiers": [
            {
                "id": "subject_name_foundations",
                "name": "Subject Name: Foundations",
                "desc": "What this tier covers",
                "nodes": [
                    # (ref, node_type, title, description, benchmark, frequency, minutes)
                    # 8-tuple adds per-node assessment_type override
                    # 9-tuple adds per-node measurement_unit override
                    ("sn1-01", "skill", "Title", "Desc", "Mastery looks like…", 3, 15),
                ],
                "edges": [
                    ("sn1-01", "sn1-02"),
                ],
            },
            …
        ],
    }
"""

from app.services.templates import Template, TemplateEdge, TemplateNode


def build_templates(domain_data: dict) -> dict[str, Template]:
    """Build a complete set of Template objects from compact domain data.

    Returns a dict keyed by template_id ready to merge into TEMPLATES.
    """
    subject = domain_data["subject"]
    color = domain_data["color"]
    default_assessment = domain_data.get("assessment_type", "observed")
    default_unit = domain_data.get("unit", "boolean")

    templates: dict[str, Template] = {}
    for tier in domain_data["tiers"]:
        nodes: list[TemplateNode] = []
        for i, n in enumerate(tier["nodes"]):
            # Support 7/8/9-tuple node specs:
            #   7: (ref, ntype, title, desc, benchmark, frequency, minutes)
            #   8: + per-node assessment_type
            #   9: + per-node measurement_unit
            if len(n) == 9:
                ref, ntype, title, desc, bench, freq, mins, assess, unit = n
            elif len(n) == 8:
                ref, ntype, title, desc, bench, freq, mins, assess = n
                unit = default_unit
            else:
                ref, ntype, title, desc, bench, freq, mins = n
                assess = default_assessment
                unit = default_unit

            nodes.append(
                TemplateNode(
                    ref=ref,
                    node_type=ntype,
                    title=title,
                    description=desc,
                    estimated_minutes=mins,
                    sort_order=i,
                    content={
                        "description": desc,
                        "benchmark_criteria": bench,
                        "assessment_type": assess,
                        "measurement_unit": unit,
                        "suggested_frequency": freq,
                    },
                )
            )

        edges = [TemplateEdge(e[0], e[1]) for e in tier["edges"]]

        t = Template(
            template_id=tier["id"],
            name=tier["name"],
            description=tier["desc"],
            subject_name=subject,
            subject_color=color,
            nodes=nodes,
            edges=edges,
        )
        templates[t.template_id] = t

    return templates


def register_domain(domain_data: dict) -> None:
    """Build templates from domain data and register them in the global TEMPLATES dict."""
    from app.services.templates import TEMPLATES

    TEMPLATES.update(build_templates(domain_data))
