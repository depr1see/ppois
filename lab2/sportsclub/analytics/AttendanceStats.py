from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AttendanceStats:
    session_id: str
    attended: int
    capacity: int

    def fill_rate(self) -> float:
        return round(self.attended / max(self.capacity, 1), 2)

    def add_attendance(self, count: int) -> None:
        self.attended += count
