from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CleaningSchedule:
    schedule_id: str
    areas: list[str] = field(default_factory=list)
    completed: list[str] = field(default_factory=list)

    def add_area(self, area: str) -> None:
        if area not in self.areas:
            self.areas.append(area)

    def mark_completed(self, area: str) -> None:
        if area in self.areas and area not in self.completed:
            self.completed.append(area)
