from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PersonalGoal:
    goal_id: str
    member_id: str
    target: str

    def redefine(self, target: str) -> None:
        self.target = target

    def describe(self) -> str:
        return f"Goal {self.goal_id}: {self.target}"
