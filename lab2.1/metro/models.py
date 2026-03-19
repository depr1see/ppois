"""Domain models for metro transport."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TrainStatus(str, Enum):
    """Operational status of a train."""

    IN_SERVICE = "IN_SERVICE"
    MAINTENANCE = "MAINTENANCE"


class TicketStatus(str, Enum):
    """Status of a ticket."""

    ACTIVE = "ACTIVE"
    USED = "USED"


@dataclass(frozen=True, slots=True)
class MetroStation:
    """Metro station."""

    station_id: str
    name: str


@dataclass(slots=True)
class Platform:
    """Platform located at a station."""

    platform_id: str
    station_id: str
    current_train_id: str | None = None


@dataclass(slots=True)
class Train:
    """Metro train."""

    train_id: str
    capacity: int
    station_id: str
    platform_id: str | None
    status: TrainStatus = TrainStatus.IN_SERVICE
    passenger_ids: set[str] = field(default_factory=set)

    @property
    def free_seats(self) -> int:
        """Return count of free seats."""
        return self.capacity - len(self.passenger_ids)


@dataclass(slots=True)
class Ticket:
    """Passenger ticket."""

    ticket_id: str
    passenger_id: str
    origin_station_id: str
    destination_station_id: str
    status: TicketStatus = TicketStatus.ACTIVE


@dataclass(slots=True)
class Turnstile:
    """Station turnstile."""

    turnstile_id: str
    station_id: str
    is_operational: bool = True
    last_security_check: datetime | None = None


@dataclass(slots=True)
class Passenger:
    """Passenger."""

    passenger_id: str
    full_name: str
    current_station_id: str | None = None
    on_train_id: str | None = None
    active_ticket_id: str | None = None
    passed_turnstile: bool = False


@dataclass(order=True, frozen=True, slots=True)
class ScheduleEntry:
    """Single schedule record."""

    time_minutes: int
    train_id: str
    station_id: str

    @property
    def time_label(self) -> str:
        """Format minutes from midnight to HH:MM."""
        hours = self.time_minutes // 60
        minutes = self.time_minutes % 60
        return f"{hours:02d}:{minutes:02d}"


@dataclass(slots=True)
class Schedule:
    """Schedule aggregate."""

    entries: list[ScheduleEntry] = field(default_factory=list)
