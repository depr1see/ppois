from dataclasses import dataclass
from typing import Any


@dataclass(order=True, frozen=True)
class SortableItem:
    """Example comparable object for demonstrating template-like sorting."""

    priority: int
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.priority, int):
            raise TypeError("priority must be int")
        if not isinstance(self.name, str):
            raise TypeError("name must be str")

    def __str__(self) -> str:
        return f"{self.name}({self.priority})"

    def describe(self) -> str:
        return f"Item {self.name} with priority {self.priority}"
