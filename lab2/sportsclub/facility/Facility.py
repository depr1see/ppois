from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Facility:
    name: str
    address: str
    amenities: list[str] = field(default_factory=list)

    def add_amenity(self, amenity: str) -> None:
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def has_amenity(self, amenity: str) -> bool:
        return amenity in self.amenities
