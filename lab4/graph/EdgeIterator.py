from typing import Generic, Iterable, Optional, Tuple, TypeVar, TYPE_CHECKING

from .BidirectionalIteratorBase import BidirectionalIteratorBase

T = TypeVar("T")

if TYPE_CHECKING:
    from .Graph import Graph


class EdgeIterator(BidirectionalIteratorBase[Tuple[T, T]], Generic[T]):
    """Bidirectional iterator over graph edges (as unordered vertex pairs)."""

    def __init__(
        self,
        graph: "Graph[T]",
        indices: Optional[Iterable[int]] = None,
    ):
        self._graph = graph
        prepared_indices = (
            list(range(graph.edge_count)) if indices is None else list(indices)
        )
        super().__init__(prepared_indices, self._graph.edge_vertices)

    def clone_reversed(self) -> "EdgeIterator[T]":
        return EdgeIterator(self._graph, reversed(self._indices))

    def __reversed__(self) -> "EdgeIterator[T]":
        return self.clone_reversed()
