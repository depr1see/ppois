from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.DoubleBookingException import DoubleBookingException


@dataclass
class PoolLane:
    lane_id: str
    length_m: int
    reserved_by: str | None = None

    def reserve(self, member_id: str) -> None:
        if self.reserved_by and self.reserved_by != member_id:
            raise DoubleBookingException("Lane already reserved.")
        self.reserved_by = member_id

    def release(self) -> None:
        self.reserved_by = None
