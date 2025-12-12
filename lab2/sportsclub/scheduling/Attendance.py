from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Attendance:
    session_id: str
    present: set[str] = field(default_factory=set)
    late: set[str] = field(default_factory=set)

    def mark_present(self, member_id: str) -> None:
        self.present.add(member_id)

    def mark_late(self, member_id: str) -> None:
        self.late.add(member_id)
