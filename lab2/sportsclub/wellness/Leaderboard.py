from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Leaderboard:
    name: str
    scores: dict[str, int] = field(default_factory=dict)
    season: str = "2025"

    def submit_score(self, member_id: str, score: int) -> None:
        self.scores[member_id] = max(self.scores.get(member_id, 0), score)

    def top_members(self, n: int = 3) -> list[str]:
        return [mid for mid, _ in sorted(self.scores.items(), key=lambda x: x[1], reverse=True)[:n]]
