from typing import Generic, Iterable, Optional, TypeVar, TYPE_CHECKING

from .BidirectionalIteratorBase import BidirectionalIteratorBase

T = TypeVar("T")

if TYPE_CHECKING:
    from .Graph import Graph


class AdjacentVertexIterator(BidirectionalIteratorBase[T], Generic[T]):
    """Iterates vertices that are adjacent to a given vertex."""

    def __init__(
        self,
        graph: "Graph[T]",
        vertex_index: int,
        indices: Optional[Iterable[int]] = None,
    ):
        self._graph = graph
        self._vertex_index = vertex_index
        prepared_indices = (
            list(graph.neighbor_indices(vertex_index))
            if indices is None
            else list(indices)
        )
        super().__init__(prepared_indices, self._graph.vertex_value_at)

    def clone_reversed(self) -> "AdjacentVertexIterator[T]":
        return AdjacentVertexIterator(
            self._graph,
            self._vertex_index,
            reversed(self._indices),
        )

    def __reversed__(self) -> "AdjacentVertexIterator[T]":
        return self.clone_reversed()
