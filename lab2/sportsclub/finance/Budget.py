from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.OverdueBalanceException import OverdueBalanceException


@dataclass
class Budget:
    budget_id: str
    allocated: float
    spent: float

    def spend(self, amount: float) -> None:
        self.spent += amount
        if self.spent > self.allocated:
            raise OverdueBalanceException("Budget exceeded.")

    def remaining(self) -> float:
        return round(self.allocated - self.spent, 2)
