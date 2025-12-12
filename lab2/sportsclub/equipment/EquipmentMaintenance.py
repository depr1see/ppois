from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class EquipmentMaintenance:
    record_id: str
    item_id: str
    scheduled_on: date

    def reschedule(self, new_date: date) -> None:
        self.scheduled_on = new_date

    def is_due(self, today: date | None = None) -> bool:
        today = today or date.today()
        return today >= self.scheduled_on
