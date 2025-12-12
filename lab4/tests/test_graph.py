import copy

import pytest

from graph import Graph, GraphError


def build_graph() -> Graph[str]:
    graph = Graph[str]()
    for vertex in ["A", "B", "C", "D"]:
        graph.add_vertex(vertex)
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    return graph


def test_add_and_remove_vertex_and_edge():
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2)
    assert graph.vertex_count == 2
    assert graph.edge_count == 1
    graph.remove_vertex(1)
    assert graph.vertex_count == 1
    assert graph.edge_count == 0
    with pytest.raises(GraphError):
        graph.remove_vertex(99)


def test_degree_and_presence_checks():
    graph = build_graph()
    assert graph.degree_of_vertex("B") == 2
    assert graph.has_vertex("A")
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("A", "D")
    with pytest.raises(GraphError):
        graph.add_vertex("A")
    with pytest.raises(GraphError):
        graph.add_edge("A", "B")


def test_degree_of_loop_edge():
    graph = Graph[str]()
    graph.add_vertex("X")
    graph.add_edge("X", "X")
    assert graph.degree_of_edge(("X", "X")) == 1


def test_iterators_forward_and_reverse():
    graph = build_graph()
    assert list(graph.vertices()) == ["A", "B", "C", "D"]
    assert list(graph.vertices_reverse()) == ["D", "C", "B", "A"]
    assert list(graph.edges()) == [("A", "B"), ("B", "C"), ("C", "D")]
    assert list(graph.edges_reverse()) == [("C", "D"), ("B", "C"), ("A", "B")]


def test_incident_and_adjacent_iterators():
    graph = build_graph()
    incident = list(graph.incident_edges("B"))
    assert ("A", "B") in incident and ("B", "C") in incident
    adjacent = list(graph.adjacent_vertices("B"))
    assert adjacent == ["A", "C"]


def test_remove_via_iterators():
    graph = build_graph()
    edge_iter = graph.edges()
    next(edge_iter)
    graph.remove_edge_by_iterator(edge_iter)
    assert graph.edge_count == 2
    vertex_iter = graph.vertices()
    next(vertex_iter)
    graph.remove_vertex_by_iterator(vertex_iter)
    assert graph.vertex_count == 3


def test_comparisons_and_string_repr():
    first = build_graph()
    second = build_graph()
    assert first == second
    second.add_edge("A", "D")
    assert first < second
    assert "Vertices" in str(first) and "Edges" in str(first)


def test_missing_edge_removal_raises():
    graph = build_graph()
    with pytest.raises(GraphError):
        graph.remove_edge("A", "D")


def test_iterator_reverse_and_previous():
    graph = build_graph()
    iterator = graph.vertices()
    assert next(iterator) == "A"
    assert next(iterator) == "B"
    assert iterator.previous() == "B"
    reversed_clone = iterator.clone_reversed()
    assert list(reversed_clone) == ["D", "C", "B", "A"]


def test_incident_and_adjacent_reverse_iterators():
    graph = build_graph()
    incident_reverse = list(graph.incident_edges_reverse("C"))
    assert incident_reverse[0] == ("C", "D")
    adjacent_reverse = list(graph.adjacent_vertices_reverse("B"))
    assert adjacent_reverse == ["C", "A"]


def test_copy_semantics_and_membership():
    graph = build_graph()
    assert graph.empty() is False
    cloned = Graph.from_graph(graph)
    shallow = copy.copy(graph)
    deep = copy.deepcopy(graph)
    assert cloned == graph == shallow == deep
    assert "A" in graph and "Z" not in graph
    fresh = Graph[int]()
    assert fresh.empty()
    fresh.add_vertex(1)
    assert not fresh.empty()


def test_degree_with_indices():
    graph = build_graph()
    assert graph.degree_of_vertex(1) == 2
    assert graph.degree_of_edge(0) == 2
