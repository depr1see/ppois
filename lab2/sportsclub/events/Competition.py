from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Competition:
    name: str
    sport: str
    participants: list[str] = field(default_factory=list)

    def add_participant(self, member_id: str) -> None:
        if member_id not in self.participants:
            self.participants.append(member_id)

    def total(self) -> int:
        return len(self.participants)
