from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.AccessDeniedException import AccessDeniedException


@dataclass
class Locker:
    locker_id: str
    assigned_to: str | None
    pin: str

    def assign(self, member_id: str) -> None:
        self.assigned_to = member_id

    def open(self, pin: str) -> bool:
        if pin != self.pin:
            raise AccessDeniedException("Invalid PIN.")
        return True
