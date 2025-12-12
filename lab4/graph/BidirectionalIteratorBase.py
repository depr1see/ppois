from typing import Callable, Generic, Iterable, List, Optional, TypeVar

T_co = TypeVar("T_co", covariant=True)


class BidirectionalIteratorBase(Generic[T_co]):
    """
    Simple bidirectional iterator that works over a prepared list of indices.

    Access to the underlying element is delegated to the `accessor` callback.
    """

    def __init__(self, indices: Iterable[int], accessor: Callable[[int], T_co]):
        self._indices: List[int] = list(indices)
        self._accessor = accessor
        self._position = 0
        self._current_index: Optional[int] = None

    def __iter__(self) -> "BidirectionalIteratorBase[T_co]":
        return self

    def __next__(self) -> T_co:
        if self._position >= len(self._indices):
            raise StopIteration
        self._current_index = self._indices[self._position]
        self._position += 1
        return self._accessor(self._current_index)

    def previous(self) -> T_co:
        if self._position <= 0:
            raise StopIteration
        self._position -= 1
        self._current_index = self._indices[self._position]
        return self._accessor(self._current_index)

    def clone_reversed(self) -> "BidirectionalIteratorBase[T_co]":
        return BidirectionalIteratorBase(reversed(self._indices), self._accessor)

    @property
    def current_index(self) -> int:
        if self._current_index is None:
            raise RuntimeError("Iterator has not yielded any element yet")
        return self._current_index

    def __reversed__(self) -> "BidirectionalIteratorBase[T_co]":
        return self.clone_reversed()

    def __len__(self) -> int:
        return len(self._indices)
