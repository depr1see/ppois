from __future__ import annotations
from dataclasses import dataclass


@dataclass
class NutritionPlan:
    plan_id: str
    calories: int
    protein: int

    def adjust_calories(self, amount: int) -> None:
        self.calories += amount

    def protein_ratio(self) -> float:
        return round(self.protein / max(self.calories, 1), 3)
