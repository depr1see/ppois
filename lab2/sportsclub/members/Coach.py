from __future__ import annotations
from dataclasses import dataclass
from sportsclub.exceptions.UnauthorizedCoachException import UnauthorizedCoachException


@dataclass
class Coach:
    coach_id: str
    name: str
    certified: bool

    def verify_certification(self) -> None:
        if not self.certified:
            raise UnauthorizedCoachException("Coach certification missing.")

    def assign_team(self, team: "Team") -> str:
        return f"Coach {self.name} assigned to team {team.name}"
