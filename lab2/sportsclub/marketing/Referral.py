from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Referral:
    referral_id: str
    referrer_id: str
    referred_id: str

    def swap_referrer(self, new_referrer: str) -> None:
        self.referrer_id = new_referrer

    def summary(self) -> str:
        return f"{self.referrer_id}->{self.referred_id}"
