from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TrophyCase:
    location: str
    trophies: list[str] = field(default_factory=list)
    curator: str | None = None

    def add_trophy(self, name: str) -> None:
        if name not in self.trophies:
            self.trophies.append(name)

    def assign_curator(self, name: str) -> None:
        self.curator = name
