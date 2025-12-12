from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EquipmentItem:
    item_id: str
    name: str
    available: bool

    def mark_unavailable(self) -> None:
        self.available = False

    def mark_available(self) -> None:
        self.available = True
