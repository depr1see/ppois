from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Invoice:
    invoice_id: str
    member_id: str
    amount: float

    def apply_discount(self, amount: float) -> None:
        self.amount = max(self.amount - amount, 0.0)

    def is_paid(self, payments: float) -> bool:
        return payments >= self.amount
