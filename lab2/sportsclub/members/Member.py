from __future__ import annotations
from dataclasses import dataclass, field
from sportsclub.exceptions.InvalidMembershipException import InvalidMembershipException


@dataclass
class Member:
    member_id: str
    name: str
    active: bool = True
    classes_attended: list[str] = field(default_factory=list)

    def suspend(self) -> None:
        self.active = False

    def enroll_class(self, session_id: str) -> None:
        if not self.active:
            raise InvalidMembershipException("Member is not active.")
        self.classes_attended.append(session_id)
