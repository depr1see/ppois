from typing import Callable, Iterable, List, Optional, TypeVar

T = TypeVar("T")


def comb_sort(
    data: Iterable[T],
    *,
    key: Optional[Callable[[T], object]] = None,
    reverse: bool = False,
) -> List[T]:
    """
    Comb sort implementation that works with any iterable.

    The function does not mutate the incoming iterable; it returns a new list.
    A key function can be provided to mirror `sorted` semantics.
    """

    items: List[T] = list(data)
    if len(items) < 2:
        return items

    gap = len(items)
    shrink_factor = 1.3
    swapped = True
    key_fn = key if key is not None else lambda x: x

    while gap > 1 or swapped:
        gap = max(1, int(gap / shrink_factor))
        swapped = False
        for i in range(len(items) - gap):
            first, second = items[i], items[i + gap]
            first_key, second_key = key_fn(first), key_fn(second)
            should_swap = first_key < second_key if reverse else first_key > second_key
            if should_swap:
                items[i], items[i + gap] = second, first
                swapped = True

    return items
