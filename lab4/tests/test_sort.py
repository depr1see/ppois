import pytest

from sort import SortableItem, comb_sort, tournament_sort


def test_comb_sort_sorts_integers():
    numbers = [5, 1, 4, 2, 8]
    result = comb_sort(numbers)
    assert result == [1, 2, 4, 5, 8]
    assert numbers == [5, 1, 4, 2, 8]


def test_comb_sort_reverse_with_key():
    words = ["apple", "fig", "banana", "kiwi"]
    result = comb_sort(words, key=len, reverse=True)
    assert result == ["banana", "apple", "kiwi", "fig"]


def test_tournament_sort_with_custom_objects():
    items = [SortableItem(3, "c"), SortableItem(1, "a"), SortableItem(2, "b")]
    sorted_items = tournament_sort(items, key=lambda i: i.priority)
    assert [item.priority for item in sorted_items] == [1, 2, 3]
    assert items[0].describe() == "Item c with priority 3"


def test_tournament_sort_reverse_and_empty():
    items = [5, 2, 9]
    assert tournament_sort(items, reverse=True) == [9, 5, 2]
    assert tournament_sort([]) == []
    assert comb_sort([]) == []


def test_sortable_item_validation():
    with pytest.raises(TypeError):
        SortableItem("high", "oops")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        SortableItem(1, 123)  # type: ignore[arg-type]
