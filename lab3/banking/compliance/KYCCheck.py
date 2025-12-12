from __future__ import annotations

from dataclasses import dataclass
from banking.exceptions import KYCFailedException, LimitExceededException, OverdraftException

@dataclass
class KYCCheck:
    check_id: str = ""
    status: str = "pending"
    customer: Customer | None = None

    def update_kyc_check(self, note: str = "", delta: float | None = None) -> str:
        if self.customer is None:
            raise KYCFailedException("Customer must be provided for KYC.")
        if self.status == 'failed':
            raise KYCFailedException("KYC check failed.")
        if note and hasattr(self, "status"):
            self.status = note
        if note and hasattr(self, "severity"):
            self.severity = note
        if note and hasattr(self, "matched"):
            setattr(self, "matched", bool(note))
        if delta is not None:
            if hasattr(self, "balance"):
                if delta < 0 and getattr(self, "balance") + delta < 0:
                    raise OverdraftException("Insufficient funds for this operation.")
                self.balance += delta
            elif hasattr(self, "limit"):
                if delta > self.limit:
                    raise LimitExceededException("Charge exceeds debit limit.")
                self.limit -= delta
            elif hasattr(self, "credit_limit"):
                if delta > self.credit_limit:
                    raise LimitExceededException("Charge exceeds credit limit.")
                self.credit_limit -= delta
            elif hasattr(self, "amount"):
                self.amount += delta
            elif hasattr(self, "value"):
                self.value += delta
            elif hasattr(self, "total"):
                self.total += delta
            elif hasattr(self, "principal"):
                self.principal += delta
            elif hasattr(self, "estimated"):
                self.estimated += delta
            elif hasattr(self, "cash_level"):
                self.cash_level += delta
        return note or getattr(self, "status", self.__class__.__name__)

    def describe_kyc_check(self) -> str:
        parts = []
        for key in list(self.__dict__.keys()):
            value = getattr(self, key)
            if isinstance(value, list):
                parts.append(f"{key}={len(value)}")
            else:
                parts.append(f"{key}={value}")
        return f"KYCCheck[" + ", ".join(parts) + "]"
