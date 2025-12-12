from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, Sequence, Tuple, TypeVar, Union

from .AdjacentVertexIterator import AdjacentVertexIterator
from .EdgeIterator import EdgeIterator
from .GraphError import GraphError
from .IncidentEdgeIterator import IncidentEdgeIterator
from .VertexIterator import VertexIterator

T = TypeVar("T")


class Graph(Generic[T]):
    """
    Undirected graph backed by an incidence matrix.

    The class hides the underlying representation while exposing a STL-like API
    with iterators, comparison operators and exception-based error handling.
    """

    value_type = T
    reference = T
    const_reference = T
    pointer = T

    def __init__(self, vertices: Optional[Iterable[T]] = None):
        self._vertices: List[T] = []
        self._edges: List[Tuple[int, int]] = []
        self._incidence: List[List[bool]] = []
        if vertices is not None:
            for vertex in vertices:
                self.add_vertex(vertex)

    # Constructors and assignment equivalents
    @classmethod
    def from_graph(cls, other: "Graph[T]") -> "Graph[T]":
        clone = cls(other._vertices)
        for first_idx, second_idx in other._edges:
            clone._add_edge_by_indices(first_idx, second_idx)
        return clone

    def __copy__(self) -> "Graph[T]":
        return Graph.from_graph(self)

    def __deepcopy__(self, memo: dict) -> "Graph[T]":
        return Graph.from_graph(self)

    # Basic info
    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    def __len__(self) -> int:
        return self.vertex_count

    def empty(self) -> bool:
        return self.vertex_count == 0

    # Vertex helpers
    def has_vertex(self, vertex: T) -> bool:
        return vertex in self._vertices

    def _vertex_index(self, vertex: T) -> int:
        try:
            return self._vertices.index(vertex)
        except ValueError as exc:
            raise GraphError("Vertex not found") from exc

    def vertex_value_at(self, index: int) -> T:
        self._validate_vertex_index(index)
        return self._vertices[index]

    # Edge helpers
    def _normalize_edge_indices(self, first_index: int, second_index: int) -> Tuple[int, int]:
        return (first_index, second_index) if first_index <= second_index else (second_index, first_index)

    def _validate_vertex_index(self, index: int) -> None:
        if index < 0 or index >= self.vertex_count:
            raise GraphError(f"Vertex index {index} out of range")

    def _validate_edge_index(self, index: int) -> None:
        if index < 0 or index >= self.edge_count:
            raise GraphError(f"Edge index {index} out of range")

    def _edge_index_by_vertices(self, first_index: int, second_index: int) -> Optional[int]:
        normalized = self._normalize_edge_indices(first_index, second_index)
        for idx, edge in enumerate(self._edges):
            if edge == normalized:
                return idx
        return None

    def edge_vertices(self, edge_index: int) -> Tuple[T, T]:
        self._validate_edge_index(edge_index)
        first_idx, second_idx = self._edges[edge_index]
        return self._vertices[first_idx], self._vertices[second_idx]

    def edge_indices_for_vertex(self, vertex_index: int) -> List[int]:
        self._validate_vertex_index(vertex_index)
        return [
            idx for idx, (first_idx, second_idx) in enumerate(self._edges) if vertex_index in (first_idx, second_idx)
        ]

    def neighbor_indices(self, vertex_index: int) -> List[int]:
        self._validate_vertex_index(vertex_index)
        neighbors = {
            other if vertex_index == first else first
            for first, other in self._edges
            if vertex_index in (first, other)
        }
        return sorted(neighbors)

    # Vertex operations
    def add_vertex(self, vertex: T) -> None:
        if self.has_vertex(vertex):
            raise GraphError("Vertex already exists")
        self._vertices.append(vertex)
        self._incidence.append([False] * self.edge_count)

    def remove_vertex(self, vertex: T) -> None:
        vertex_index = self._vertex_index(vertex)
        self._remove_vertex_by_index(vertex_index)

    def _remove_vertex_by_index(self, vertex_index: int) -> None:
        self._validate_vertex_index(vertex_index)
        new_vertices = self._vertices[:vertex_index] + self._vertices[vertex_index + 1 :]
        new_edges: List[Tuple[int, int]] = []
        for first_idx, second_idx in self._edges:
            if vertex_index in (first_idx, second_idx):
                continue
            adjusted_first = first_idx - 1 if first_idx > vertex_index else first_idx
            adjusted_second = second_idx - 1 if second_idx > vertex_index else second_idx
            new_edges.append((adjusted_first, adjusted_second))
        self._vertices = new_vertices
        self._rebuild_from_edges(new_edges)

    def remove_vertex_by_iterator(self, iterator: VertexIterator[T]) -> None:
        self._remove_vertex_by_index(iterator.current_index)

    # Edge operations
    def add_edge(self, first: T, second: T) -> None:
        first_idx, second_idx = self._vertex_index(first), self._vertex_index(second)
        self._add_edge_by_indices(first_idx, second_idx)

    def _add_edge_by_indices(self, first_idx: int, second_idx: int) -> None:
        self._validate_vertex_index(first_idx)
        self._validate_vertex_index(second_idx)
        edge = self._normalize_edge_indices(first_idx, second_idx)
        if edge in self._edges:
            raise GraphError("Edge already exists")
        for row in self._incidence:
            row.append(False)
        self._edges.append(edge)
        edge_index = len(self._edges) - 1
        self._incidence[edge[0]][edge_index] = True
        self._incidence[edge[1]][edge_index] = True

    def remove_edge(self, first: T, second: T) -> None:
        first_idx, second_idx = self._vertex_index(first), self._vertex_index(second)
        edge_index = self._edge_index_by_vertices(first_idx, second_idx)
        if edge_index is None:
            raise GraphError("Edge not found")
        self._remove_edge_by_index(edge_index)

    def remove_edge_by_iterator(self, iterator: EdgeIterator[T]) -> None:
        self._remove_edge_by_index(iterator.current_index)

    def _remove_edge_by_index(self, edge_index: int) -> None:
        self._validate_edge_index(edge_index)
        del self._edges[edge_index]
        for row in self._incidence:
            del row[edge_index]

    # Checks and metrics
    def has_edge(self, first: T, second: T) -> bool:
        try:
            first_idx, second_idx = self._vertex_index(first), self._vertex_index(second)
        except GraphError:
            return False
        return self._edge_index_by_vertices(first_idx, second_idx) is not None

    def degree_of_vertex(self, vertex: Union[T, int]) -> int:
        vertex_index = vertex if isinstance(vertex, int) else self._vertex_index(vertex)  # type: ignore[assignment]
        self._validate_vertex_index(vertex_index)  # type: ignore[arg-type]
        return sum(1 for incident in self._incidence[vertex_index] if incident)

    def vertex_degree(self, vertex: Union[T, int]) -> int:
        return self.degree_of_vertex(vertex)

    def degree_of_edge(self, edge: Union[int, Tuple[T, T]]) -> int:
        edge_index: int
        if isinstance(edge, int):
            edge_index = edge
        else:
            first_idx, second_idx = self._vertex_index(edge[0]), self._vertex_index(edge[1])
            maybe_index = self._edge_index_by_vertices(first_idx, second_idx)
            if maybe_index is None:
                raise GraphError("Edge not found")
            edge_index = maybe_index
        self._validate_edge_index(edge_index)
        return sum(1 for row in self._incidence if row[edge_index])

    def edge_degree(self, edge: Union[int, Tuple[T, T]]) -> int:
        return self.degree_of_edge(edge)

    # Iterators
    def vertices(self) -> VertexIterator[T]:
        return VertexIterator(self)

    def vertices_reverse(self) -> VertexIterator[T]:
        return VertexIterator(self, indices=reversed(range(self.vertex_count)))

    def edges(self) -> EdgeIterator[T]:
        return EdgeIterator(self)

    def edges_reverse(self) -> EdgeIterator[T]:
        return EdgeIterator(self, indices=reversed(range(self.edge_count)))

    def incident_edges(self, vertex: T) -> IncidentEdgeIterator[T]:
        vertex_index = self._vertex_index(vertex)
        return IncidentEdgeIterator(self, vertex_index)

    def incident_edges_reverse(self, vertex: T) -> IncidentEdgeIterator[T]:
        vertex_index = self._vertex_index(vertex)
        return IncidentEdgeIterator(self, vertex_index, indices=reversed(self.edge_indices_for_vertex(vertex_index)))

    def adjacent_vertices(self, vertex: T) -> AdjacentVertexIterator[T]:
        vertex_index = self._vertex_index(vertex)
        return AdjacentVertexIterator(self, vertex_index)

    def adjacent_vertices_reverse(self, vertex: T) -> AdjacentVertexIterator[T]:
        vertex_index = self._vertex_index(vertex)
        return AdjacentVertexIterator(
            self,
            vertex_index,
            indices=reversed(self.neighbor_indices(vertex_index)),
        )

    def __iter__(self) -> Iterator[T]:
        return iter(self.vertices())

    def __reversed__(self) -> Iterator[T]:
        return iter(self.vertices_reverse())

    # Comparison and representation
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph):
            return False
        return (
            self._vertices == other._vertices
            and self._normalized_edges(self._edges) == self._normalized_edges(other._edges)
        )

    def __lt__(self, other: "Graph[T]") -> bool:
        self_tuple = (self.vertex_count, self.edge_count, sorted(self._vertices), self._sorted_edge_values())
        other_tuple = (other.vertex_count, other.edge_count, sorted(other._vertices), other._sorted_edge_values())
        return self_tuple < other_tuple

    def __le__(self, other: "Graph[T]") -> bool:
        return self == other or self < other

    def __gt__(self, other: "Graph[T]") -> bool:
        return not self <= other

    def __ge__(self, other: "Graph[T]") -> bool:
        return not self < other

    def __contains__(self, vertex: object) -> bool:
        return bool(self.has_vertex(vertex))  # type: ignore[arg-type]

    def __str__(self) -> str:
        vertex_part = ", ".join(str(vertex) for vertex in self)
        edge_part = ", ".join(f"({first}, {second})" for first, second in self.edges())
        return f"Vertices: [{vertex_part}] | Edges: [{edge_part}]"

    def clear(self) -> None:
        self._vertices.clear()
        self._edges.clear()
        self._incidence.clear()

    def _normalized_edges(self, edges: Sequence[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [self._normalize_edge_indices(first, second) for first, second in edges]

    def _sorted_edge_values(self) -> List[Tuple[T, T]]:
        return sorted(tuple(sorted((self._vertices[first], self._vertices[second]))) for first, second in self._edges)

    def _rebuild_from_edges(self, edges: List[Tuple[int, int]]) -> None:
        self._edges = []
        self._incidence = [[False for _ in range(len(edges))] for _ in range(self.vertex_count)]
        for edge_index, (first_idx, second_idx) in enumerate(edges):
            self._edges.append(self._normalize_edge_indices(first_idx, second_idx))
            self._incidence[first_idx][edge_index] = True
            self._incidence[second_idx][edge_index] = True
