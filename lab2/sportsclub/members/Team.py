from __future__ import annotations
from dataclasses import dataclass, field

from sportsclub.members.Member import Member


@dataclass
class Team:
    name: str
    sport: str
    roster: list[Member] = field(default_factory=list)

    def add_member(self, member: Member) -> None:
        if member not in self.roster:
            self.roster.append(member)

    def total_members(self) -> int:
        return len(self.roster)
