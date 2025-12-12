from sort import SortableItem, comb_sort, tournament_sort
from graph import Graph


def run_sort_demo() -> None:
    numbers = [42, 7, 23, 4, 16]
    print("Comb sort:", comb_sort(numbers))
    print("Tournament sort:", tournament_sort(numbers, reverse=True))

    items = [
        SortableItem(3, "analytics"),
        SortableItem(1, "design"),
        SortableItem(2, "infrastructure"),
    ]
    print("Sortable items by priority:", [str(item) for item in comb_sort(items)])


def run_graph_demo() -> None:
    graph = Graph[str]()
    for vertex in ["A", "B", "C", "D"]:
        graph.add_vertex(vertex)
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("A", "D")

    print("Graph snapshot:", graph)
    print("Degrees: A ->", graph.degree_of_vertex("A"), "Edge(A,D) ->", graph.degree_of_edge(("A", "D")))
    print("Adjacent to B:", list(graph.adjacent_vertices("B")))
    print("Incident edges for C:", list(graph.incident_edges("C")))


def main() -> None:
    print("=== Sorting demo ===")
    run_sort_demo()
    print("\n=== Graph demo ===")
    run_graph_demo()


if __name__ == "__main__":
    main()
