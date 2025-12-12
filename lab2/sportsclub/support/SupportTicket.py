from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SupportTicket:
    ticket_id: str
    member_id: str
    status: str

    def update_status(self, status: str) -> None:
        self.status = status

    def assign(self, agent: str) -> str:
        return f"Ticket {self.ticket_id} assigned to {agent}"
