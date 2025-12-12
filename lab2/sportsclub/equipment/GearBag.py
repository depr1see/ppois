from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GearBag:
    bag_id: str
    owner_id: str
    contents: list[str] = field(default_factory=list)

    def add_item(self, item: str) -> None:
        if item not in self.contents:
            self.contents.append(item)

    def remove_item(self, item: str) -> None:
        if item in self.contents:
            self.contents.remove(item)
