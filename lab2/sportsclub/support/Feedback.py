from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Feedback:
    feedback_id: str
    member_id: str
    rating: int
    tags: set[str] = field(default_factory=set)

    def add_tag(self, tag: str) -> None:
        self.tags.add(tag)

    def is_positive(self) -> bool:
        return self.rating >= 4
