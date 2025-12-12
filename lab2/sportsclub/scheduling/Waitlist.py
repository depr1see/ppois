from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Waitlist:
    session_id: str
    members: list[str] = field(default_factory=list)
    promoted: list[str] = field(default_factory=list)

    def add(self, member_id: str) -> None:
        if member_id not in self.members:
            self.members.append(member_id)

    def promote(self, member_id: str) -> None:
        if member_id in self.members and member_id not in self.promoted:
            self.promoted.append(member_id)
