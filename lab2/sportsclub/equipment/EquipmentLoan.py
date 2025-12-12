from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.EquipmentUnavailableException import EquipmentUnavailableException
from sportsclub.equipment.EquipmentItem import EquipmentItem


@dataclass
class EquipmentLoan:
    loan_id: str
    member_id: str
    item: EquipmentItem

    def checkout(self) -> None:
        if not self.item.available:
            raise EquipmentUnavailableException("Item unavailable.")
        self.item.mark_unavailable()

    def checkin(self) -> None:
        self.item.mark_available()
