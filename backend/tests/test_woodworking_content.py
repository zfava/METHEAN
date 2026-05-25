"""Tests for the woodworking trade content.

Covers the trades validator (validate_competency), the documented
shapes in NODE_CONTENT_SCHEMA, and the authored woodworking nodes.
Each authored id is parametrized through validate_competency. Hard
checks for safety gating: every hands-on (technique) node must prereq
the trade safety node, must carry safety_basis with
supervision_required True when a cutting tool is involved, and must
carry demonstration_criteria. A separate guard test resolves every
prerequisite against the authored set.
"""

import pytest

from app.content.woodworking_content import WOODWORKING_CONTENT
from app.services.node_content import (
    NODE_CONTENT_SCHEMA,
    TRADES_BANDS,
    TRADES_NODE_TYPES,
    validate_competency,
)


def _minimal_root_node(**overrides) -> dict:
    base = {
        "node_type": "root",
        "trade": "woodworking",
        "trade_name": "Woodworking",
        "safety_node": "ws-001",
    }
    base.update(overrides)
    return base


def _minimal_safety_node(**overrides) -> dict:
    base = {
        "node_type": "safety",
        "trade": "woodworking",
        "competency_name": "shop safety",
        "progression_band": "helper",
        "prerequisites": [],
        "safety_basis": {"hazards": ["x"], "ppe_required": ["x"], "supervision_required": True},
        "demonstration_criteria": ["names the PPE"],
        "mentor_signoff_required": True,
    }
    base.update(overrides)
    return base


def _minimal_technique_node(**overrides) -> dict:
    base = {
        "node_type": "technique",
        "trade": "woodworking",
        "competency_name": "do a thing",
        "progression_band": "helper",
        "prerequisites": ["ws-001"],
        "safety_basis": {
            "hazards": ["x"],
            "ppe_required": ["x"],
            "supervision_required": False,
        },
        "tools_required": [{"name": "pencil"}],
        "demonstration_criteria": ["the mark is on the line"],
    }
    base.update(overrides)
    return base


class TestSchemaDocumentation:
    def test_trade_root_node_documented(self) -> None:
        assert "trade_root_node" in NODE_CONTENT_SCHEMA
        assert NODE_CONTENT_SCHEMA["trade_root_node"]["node_type"] == "root"

    def test_trade_safety_competency_documented(self) -> None:
        assert "trade_safety_competency" in NODE_CONTENT_SCHEMA
        assert NODE_CONTENT_SCHEMA["trade_safety_competency"]["node_type"] == "safety"

    def test_trade_technique_competency_documented(self) -> None:
        assert "trade_technique_competency" in NODE_CONTENT_SCHEMA
        assert NODE_CONTENT_SCHEMA["trade_technique_competency"]["node_type"] == "technique"

    def test_bands_and_node_types_exported(self) -> None:
        assert TRADES_BANDS == frozenset({"helper", "apprentice", "journeyman", "qualified"})
        assert {"root", "safety", "technique"}.issubset(TRADES_NODE_TYPES)


class TestValidateCompetencyBasics:
    def test_non_dict_content_raises(self) -> None:
        with pytest.raises(ValueError, match="must be a dict"):
            validate_competency("not a dict")  # type: ignore[arg-type]

    def test_unknown_node_type_raises(self) -> None:
        with pytest.raises(ValueError, match="node_type"):
            validate_competency({"node_type": "mystery"})

    def test_minimal_root_node_passes(self) -> None:
        assert validate_competency(_minimal_root_node()) == []

    def test_minimal_safety_node_passes(self) -> None:
        assert validate_competency(_minimal_safety_node()) == []

    def test_minimal_technique_node_passes(self) -> None:
        assert validate_competency(_minimal_technique_node()) != []  # warnings: missing artifact, common_errors


class TestValidateCompetencyHardChecks:
    def test_root_missing_safety_node_raises(self) -> None:
        node = _minimal_root_node()
        del node["safety_node"]
        with pytest.raises(ValueError, match="safety_node"):
            validate_competency(node)

    def test_safety_missing_safety_basis_raises(self) -> None:
        node = _minimal_safety_node()
        del node["safety_basis"]
        with pytest.raises(ValueError, match="safety_basis"):
            validate_competency(node)

    def test_safety_missing_mentor_signoff_raises(self) -> None:
        node = _minimal_safety_node()
        node["mentor_signoff_required"] = False
        with pytest.raises(ValueError, match="mentor_signoff_required"):
            validate_competency(node)

    def test_technique_missing_safety_basis_raises(self) -> None:
        node = _minimal_technique_node()
        del node["safety_basis"]
        with pytest.raises(ValueError, match="safety_basis"):
            validate_competency(node)

    def test_technique_missing_demonstration_criteria_raises(self) -> None:
        node = _minimal_technique_node()
        del node["demonstration_criteria"]
        with pytest.raises(ValueError, match="demonstration_criteria"):
            validate_competency(node)

    def test_technique_with_cutting_tool_must_set_supervision(self) -> None:
        node = _minimal_technique_node(
            tools_required=[{"name": "Panel saw, crosscut filed"}],
            safety_basis={
                "hazards": ["sharp teeth"],
                "ppe_required": ["eyes"],
                "supervision_required": False,
            },
        )
        with pytest.raises(ValueError, match="cutting tool"):
            validate_competency(node)

    def test_technique_with_cutting_tool_and_supervision_passes_hard_checks(self) -> None:
        node = _minimal_technique_node(
            tools_required=[{"name": "chisel"}],
            safety_basis={
                "hazards": ["sharp edge"],
                "ppe_required": ["eyes"],
                "supervision_required": True,
            },
        )
        validate_competency(node)

    def test_technique_progression_band_missing_raises(self) -> None:
        node = _minimal_technique_node()
        del node["progression_band"]
        with pytest.raises(ValueError, match="progression_band"):
            validate_competency(node)


class TestPrerequisiteResolutionGuard:
    def test_technique_without_trade_safety_prereq_raises(self) -> None:
        # When authored_nodes contains a safety node for the same trade
        # and the technique does not prereq it, the validator raises.
        authored = {
            "ws-001": _minimal_safety_node(competency_name="shop safety"),
            "wc-foo": _minimal_technique_node(prerequisites=["wc-bar"]),
        }
        with pytest.raises(ValueError, match="must prerequisite the trade safety node"):
            validate_competency(authored["wc-foo"], authored)

    def test_prereq_resolving_to_authored_id_passes(self) -> None:
        authored = {
            "ws-001": _minimal_safety_node(),
            "wc-foo": _minimal_technique_node(prerequisites=["ws-001"]),
        }
        warnings = validate_competency(authored["wc-foo"], authored)
        # No "does not resolve" warning.
        assert not any("does not resolve" in w for w in warnings)

    def test_unresolved_prereq_warns(self) -> None:
        authored = {
            "ws-001": _minimal_safety_node(),
            "wc-foo": _minimal_technique_node(prerequisites=["ws-001", "wc-ghost"]),
        }
        warnings = validate_competency(authored["wc-foo"], authored)
        assert any("does not resolve" in w and "wc-ghost" in w for w in warnings)


AUTHORED_NODE_IDS = tuple(sorted(WOODWORKING_CONTENT.keys()))


class TestAuthoredWoodworking:
    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(WOODWORKING_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_validates(self, node_id: str) -> None:
        validate_competency(WOODWORKING_CONTENT[node_id], WOODWORKING_CONTENT)

    def test_root_node_present_and_well_formed(self) -> None:
        assert "woodworking-root" in WOODWORKING_CONTENT
        root = WOODWORKING_CONTENT["woodworking-root"]
        assert root["node_type"] == "root"
        assert root["trade"] == "woodworking"
        assert root["safety_node"] == "ws-001"

    def test_every_technique_prereqs_safety_node(self) -> None:
        for node_id, node in WOODWORKING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            prereqs = node.get("prerequisites") or []
            assert "ws-001" in prereqs, f"{node_id} technique does not prereq ws-001"

    def test_every_technique_has_safety_basis(self) -> None:
        for node_id, node in WOODWORKING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            assert isinstance(node.get("safety_basis"), dict), node_id

    def test_every_technique_has_demonstration_criteria(self) -> None:
        for node_id, node in WOODWORKING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            criteria = node.get("demonstration_criteria")
            assert isinstance(criteria, list) and criteria, node_id

    def test_cutting_tool_techniques_require_supervision(self) -> None:
        from app.services.node_content import _technique_uses_cutting_tool

        for node_id, node in WOODWORKING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            if _technique_uses_cutting_tool(node.get("tools_required") or []):
                assert (
                    node["safety_basis"]["supervision_required"] is True
                ), f"{node_id} uses a cutting tool but supervision_required is not True"

    def test_all_prerequisites_resolve_to_authored_nodes(self) -> None:
        authored_ids = set(WOODWORKING_CONTENT.keys())
        for node_id, node in WOODWORKING_CONTENT.items():
            for prereq in node.get("prerequisites") or []:
                assert prereq in authored_ids, (
                    f"{node_id} prereq {prereq!r} does not resolve to any authored node id"
                )
