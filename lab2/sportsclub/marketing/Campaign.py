from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Campaign:
    name: str
    channels: list[str] = field(default_factory=list)
    budget: float = 0.0

    def add_channel(self, channel: str) -> None:
        if channel not in self.channels:
            self.channels.append(channel)

    def spend(self, amount: float) -> None:
        self.budget += amount
