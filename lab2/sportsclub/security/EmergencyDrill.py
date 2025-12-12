from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class EmergencyDrill:
    drill_id: str
    participants: list[str] = field(default_factory=list)
    completed: bool = False

    def add_participant(self, member_id: str) -> None:
        if member_id not in self.participants:
            self.participants.append(member_id)

    def complete(self) -> None:
        self.completed = True
