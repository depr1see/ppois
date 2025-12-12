from __future__ import annotations
from dataclasses import dataclass


@dataclass
class KPIReport:
    period: str
    retention: float
    revenue: float

    def retention_delta(self, previous: float) -> float:
        return round(self.retention - previous, 2)

    def revenue_per_member(self, members: int) -> float:
        return round(self.revenue / max(members, 1), 2)
