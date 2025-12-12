from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MembershipCard:
    card_number: str
    member_id: str
    status: str

    def deactivate(self) -> None:
        self.status = "inactive"

    def assign_member(self, member_id: str) -> None:
        self.member_id = member_id
