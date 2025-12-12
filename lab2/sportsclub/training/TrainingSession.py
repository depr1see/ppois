from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

from sportsclub.members.Coach import Coach


@dataclass
class TrainingSession:
    session_id: str
    coach: Coach
    started_at: datetime
    attendees: list[str] = field(default_factory=list)

    def add_attendee(self, member_id: str) -> None:
        if member_id not in self.attendees:
            self.attendees.append(member_id)

    def duration_minutes(self, end: datetime) -> int:
        return int((end - self.started_at).total_seconds() // 60)
