from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.DoubleBookingException import DoubleBookingException


@dataclass
class Booking:
    booking_id: str
    member_id: str
    slot: str

    def reschedule(self, new_slot: str) -> None:
        self.slot = new_slot

    def prevent_duplicate(self, other_slot: str) -> None:
        if other_slot == self.slot:
            raise DoubleBookingException("Slot already booked.")
