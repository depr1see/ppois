from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SubscriptionPlan:
    plan_id: str
    price: float
    duration_days: int

    def monthly_rate(self) -> float:
        return round(self.price / max(self.duration_days / 30, 1), 2)

    def extend(self, days: int) -> None:
        self.duration_days += days
