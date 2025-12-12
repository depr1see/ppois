from __future__ import annotations
from dataclasses import dataclass, field

from sportsclub.exceptions.SafetyIncidentException import SafetyIncidentException


@dataclass
class IncidentReport:
    report_id: str
    description: str
    tags: set[str] = field(default_factory=set)

    def add_tag(self, tag: str) -> None:
        self.tags.add(tag)

    def escalate(self) -> None:
        if not self.tags:
            raise SafetyIncidentException("Incident lacks detail.")
