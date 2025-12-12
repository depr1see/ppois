from __future__ import annotations
from dataclasses import dataclass
from sportsclub.exceptions.HealthRiskException import HealthRiskException


@dataclass
class HealthProfile:
    member_id: str
    heart_rate: int
    cleared: bool

    def update_heart_rate(self, bpm: int) -> None:
        self.heart_rate = bpm
        if bpm > 190:
            raise HealthRiskException("Heart rate too high for participation.")

    def mark_cleared(self) -> None:
        self.cleared = True
