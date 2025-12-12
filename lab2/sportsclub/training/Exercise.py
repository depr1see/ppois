from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Exercise:
    name: str
    sets: int
    reps: int

    def volume(self) -> int:
        return self.sets * self.reps

    def adjust_sets(self, sets: int) -> None:
        self.sets = sets
