from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from sportsclub.exceptions.CouponExpiredException import CouponExpiredException


@dataclass
class DiscountCoupon:
    code: str
    percent: float
    expires_on: date

    def apply(self, amount: float, today: date | None = None) -> float:
        today = today or date.today()
        if today > self.expires_on:
            raise CouponExpiredException("Coupon expired.")
        return round(amount * (1 - self.percent / 100), 2)

    def is_valid(self, today: date | None = None) -> bool:
        today = today or date.today()
        return today <= self.expires_on
