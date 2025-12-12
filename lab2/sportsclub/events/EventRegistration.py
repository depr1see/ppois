from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EventRegistration:
    registration_id: str
    member_id: str
    event_name: str

    def summary(self) -> str:
        return f"{self.member_id} registered for {self.event_name}"

    def update_member(self, member_id: str) -> None:
        self.member_id = member_id
