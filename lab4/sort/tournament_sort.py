from typing import Callable, Iterable, List, Optional, TypeVar

T = TypeVar("T")


def tournament_sort(
    data: Iterable[T],
    *,
    key: Optional[Callable[[T], object]] = None,
    reverse: bool = False,
) -> List[T]:
    """
    Tournament sort implementation using a knock-out bracket.

    The algorithm repeatedly builds a tournament tree to pick the winner
    (min or max depending on `reverse`) and removes it until the input is
    exhausted. The function returns a new sorted list without mutating the input.
    """

    items: List[T] = list(data)
    if len(items) < 2:
        return items

    key_fn = key if key is not None else lambda x: x

    def _better(first_index: int, second_index: int) -> int:
        if first_index is None:
            return second_index
        if second_index is None:
            return first_index
        first_key, second_key = key_fn(items[first_index]), key_fn(items[second_index])
        if reverse:
            return first_index if first_key >= second_key else second_index
        return first_index if first_key <= second_key else second_index

    def _build_tournament(indices: List[int]) -> List[List[int]]:
        levels: List[List[int]] = [indices]
        current = indices
        while len(current) > 1:
            next_round: List[int] = []
            for i in range(0, len(current), 2):
                if i + 1 < len(current):
                    next_round.append(_better(current[i], current[i + 1]))
                else:
                    next_round.append(current[i])
            levels.append(next_round)
            current = next_round
        return levels

    active_indices = list(range(len(items)))
    sorted_result: List[T] = []

    while active_indices:
        tournament = _build_tournament(active_indices)
        winner_index = tournament[-1][0]
        sorted_result.append(items[winner_index])
        active_indices.remove(winner_index)

    return sorted_result
