from typing import Generic, Iterable, Optional, TypeVar, TYPE_CHECKING

from .BidirectionalIteratorBase import BidirectionalIteratorBase

T = TypeVar("T")

if TYPE_CHECKING:
    from .Graph import Graph


class VertexIterator(BidirectionalIteratorBase[T], Generic[T]):
    """Bidirectional iterator over graph vertices."""

    def __init__(
        self,
        graph: "Graph[T]",
        indices: Optional[Iterable[int]] = None,
    ):
        self._graph = graph
        prepared_indices = (
            list(range(graph.vertex_count)) if indices is None else list(indices)
        )
        super().__init__(prepared_indices, self._graph.vertex_value_at)

    def clone_reversed(self) -> "VertexIterator[T]":
        return VertexIterator(self._graph, reversed(self._indices))

    def __reversed__(self) -> "VertexIterator[T]":
        return self.clone_reversed()
