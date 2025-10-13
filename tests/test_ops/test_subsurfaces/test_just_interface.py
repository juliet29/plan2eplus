from replan2eplus.ops.subsurfaces.interfaces import EdgeGroup
import pytest


def test_init_edge_group():
    edges = [("a", "NORTH"), ("b", "SOUTH")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")
    assert eg


def test_init_edge_group_zones():
    edges = [("a", "0"), ("b", "1")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Zone")
    assert eg


def test_bad_init_edge_group():
    edges = [("a", "0"), ("b", "1")]
    with pytest.raises(AssertionError):
        EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")
