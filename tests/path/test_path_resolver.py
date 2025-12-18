from openehr_am.aom.constraints import CAttribute, CComplexObject
from openehr_am.path.resolver import resolve_path


def _example_tree() -> CComplexObject:
    # Root ("definition")
    return CComplexObject(
        rm_type_name="OBSERVATION",
        attributes=(
            CAttribute(
                rm_attribute_name="data",
                children=(
                    CComplexObject(
                        rm_type_name="HISTORY",
                        node_id="at0001",
                        attributes=(
                            CAttribute(
                                rm_attribute_name="events",
                                children=(
                                    CComplexObject(
                                        rm_type_name="EVENT",
                                        node_id="at0002",
                                    ),
                                    CComplexObject(
                                        rm_type_name="EVENT",
                                        node_id="at0003",
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def test_resolve_path_success_single_match():
    root = _example_tree()

    nodes, issues = resolve_path(root, "/definition/data[at0001]/events[at0002]")

    assert issues == []
    assert nodes is not None
    assert len(nodes) == 1
    assert nodes[0].node_id == "at0002"


def test_resolve_path_success_multiple_matches_when_no_predicate():
    root = _example_tree()

    nodes, issues = resolve_path(root, "/data[at0001]/events")

    assert issues == []
    assert nodes is not None
    assert {n.node_id for n in nodes} == {"at0002", "at0003"}


def test_resolve_path_emits_path910_when_no_nodes_match():
    root = _example_tree()

    nodes, issues = resolve_path(root, "/definition/data[at9999]")

    assert nodes == ()
    assert len(issues) == 1
    assert issues[0].code == "PATH910"
