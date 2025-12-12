from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SponsorDeal:
    sponsor: str
    amount: float
    active: bool

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False
