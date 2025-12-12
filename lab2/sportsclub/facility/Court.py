from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.CapacityExceededException import CapacityExceededException


@dataclass
class Court:
    court_id: str
    sport: str
    capacity: int
    booked_slots: int = 0

    def book_slot(self) -> None:
        if self.booked_slots >= self.capacity:
            raise CapacityExceededException("Court capacity reached.")
        self.booked_slots += 1

    def release_slot(self) -> None:
        self.booked_slots = max(self.booked_slots - 1, 0)
