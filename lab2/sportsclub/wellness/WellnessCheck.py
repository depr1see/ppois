from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.HealthRiskException import HealthRiskException


@dataclass
class WellnessCheck:
    check_id: str
    member_id: str
    resting_hr: int

    def validate(self) -> None:
        if self.resting_hr > 120:
            raise HealthRiskException("Resting HR too high.")

    def adjust(self, bpm: int) -> None:
        self.resting_hr = bpm
