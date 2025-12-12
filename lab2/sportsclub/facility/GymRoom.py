from __future__ import annotations
from dataclasses import dataclass


@dataclass
class GymRoom:
    room_id: str
    area_m2: float
    equipment_count: int

    def add_equipment(self, amount: int) -> None:
        self.equipment_count += amount

    def utilization(self, people: int) -> float:
        return round(people / max(self.area_m2, 1), 2)
