from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class WorkoutPlan:
    plan_id: str
    focus: str
    exercises: list[str] = field(default_factory=list)

    def add_exercise(self, name: str) -> None:
        if name not in self.exercises:
            self.exercises.append(name)

    def remove_exercise(self, name: str) -> None:
        if name in self.exercises:
            self.exercises.remove(name)
