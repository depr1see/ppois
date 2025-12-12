from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

from sportsclub.exceptions.ScheduleConflictException import ScheduleConflictException


@dataclass
class ClassSchedule:
    schedule_id: str
    start: datetime
    end: datetime
    participants: list[str] = field(default_factory=list)

    def duration_hours(self) -> float:
        return round((self.end - self.start).total_seconds() / 3600, 2)

    def add_participant(self, member_id: str) -> None:
        if member_id in self.participants:
            raise ScheduleConflictException("Member already scheduled.")
        self.participants.append(member_id)
