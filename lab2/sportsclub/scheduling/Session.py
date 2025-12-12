from __future__ import annotations
from dataclasses import dataclass, field

from sportsclub.members.Coach import Coach


@dataclass
class Session:
    session_id: str
    coach: Coach
    attendees: list[str] = field(default_factory=list)

    def add_attendee(self, member_id: str) -> None:
        if member_id not in self.attendees:
            self.attendees.append(member_id)

    def coach_name(self) -> str:
        return self.coach.name
