from typing import Generic, Iterable, Optional, Tuple, TypeVar, TYPE_CHECKING

from .BidirectionalIteratorBase import BidirectionalIteratorBase

T = TypeVar("T")

if TYPE_CHECKING:
    from .Graph import Graph


class IncidentEdgeIterator(BidirectionalIteratorBase[Tuple[T, T]], Generic[T]):
    """Iterates edges that are incident to a specific vertex."""

    def __init__(
        self,
        graph: "Graph[T]",
        vertex_index: int,
        indices: Optional[Iterable[int]] = None,
    ):
        self._graph = graph
        self._vertex_index = vertex_index
        prepared_indices = (
            list(graph.edge_indices_for_vertex(vertex_index))
            if indices is None
            else list(indices)
        )
        super().__init__(prepared_indices, self._graph.edge_vertices)

    def clone_reversed(self) -> "IncidentEdgeIterator[T]":
        return IncidentEdgeIterator(self._graph, self._vertex_index, reversed(self._indices))

    def __reversed__(self) -> "IncidentEdgeIterator[T]":
        return self.clone_reversed()
