from __future__ import annotations
from dataclasses import dataclass


@dataclass
class InjuryReport:
    report_id: str
    member_id: str
    severity: str

    def escalate(self) -> None:
        self.severity = "high"

    def close(self) -> None:
        self.severity = "resolved"
