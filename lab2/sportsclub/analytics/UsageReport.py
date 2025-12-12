from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class UsageReport:
    report_id: str
    sessions: int
    active_members: int
    notes: list[str] = field(default_factory=list)

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def utilization(self) -> float:
        return round(self.sessions / max(self.active_members, 1), 2)
