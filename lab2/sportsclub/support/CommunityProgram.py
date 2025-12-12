from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CommunityProgram:
    program_id: str
    title: str
    attendees: list[str] = field(default_factory=list)

    def register(self, member_id: str) -> None:
        if member_id not in self.attendees:
            self.attendees.append(member_id)

    def total_attendees(self) -> int:
        return len(self.attendees)
