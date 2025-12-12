from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class PlayerContract:
    member_id: str
    coach_id: str
    expires_on: date

    def extend(self, days: int) -> None:
        self.expires_on = self.expires_on.fromordinal(self.expires_on.toordinal() + days)

    def is_active(self, today: date | None = None) -> bool:
        today = today or date.today()
        return today <= self.expires_on
