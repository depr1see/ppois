from __future__ import annotations
from dataclasses import dataclass

from sportsclub.exceptions.AccessDeniedException import AccessDeniedException


@dataclass
class AccessPass:
    pass_id: str
    member_id: str
    zones: set[str]

    def grant_zone(self, zone: str) -> None:
        self.zones.add(zone)

    def validate(self, zone: str) -> bool:
        if zone not in self.zones:
            raise AccessDeniedException("Zone not permitted.")
        return True
