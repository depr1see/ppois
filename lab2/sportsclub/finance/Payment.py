from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.PaymentFailedException import PaymentFailedException


@dataclass
class Payment:
    payment_id: str
    method: str
    amount: float

    def process(self, balance: float) -> float:
        if self.amount <= 0:
            raise PaymentFailedException("Payment must be positive.")
        return balance + self.amount

    def refund(self) -> float:
        return -self.amount
