"""In-memory repository for metro entities."""

from __future__ import annotations

from dataclasses import dataclass, field

from metro.exceptions import NotFoundError, ValidationError
from metro.models import (
    MetroStation,
    Passenger,
    Platform,
    Schedule,
    Ticket,
    Train,
    Turnstile,
)


@dataclass(slots=True)
class MetroRepository:
    """Storage for domain entities."""

    stations: dict[str, MetroStation] = field(default_factory=dict)
    platforms: dict[str, Platform] = field(default_factory=dict)
    trains: dict[str, Train] = field(default_factory=dict)
    tickets: dict[str, Ticket] = field(default_factory=dict)
    turnstiles: dict[str, Turnstile] = field(default_factory=dict)
    passengers: dict[str, Passenger] = field(default_factory=dict)
    schedule: Schedule = field(default_factory=Schedule)
    _ticket_seq: int = 0
    _passenger_seq: int = 0

    def add_station(self, station: MetroStation) -> None:
        self._ensure_unique(station.station_id, self.stations, "станция")
        self.stations[station.station_id] = station

    def add_platform(self, platform: Platform) -> None:
        self._ensure_unique(platform.platform_id, self.platforms, "платформа")
        self.get_station(platform.station_id)
        self.platforms[platform.platform_id] = platform

    def add_train(self, train: Train) -> None:
        self._ensure_unique(train.train_id, self.trains, "поезд")
        self.get_station(train.station_id)
        if train.platform_id is not None:
            platform = self.get_platform(train.platform_id)
            if platform.station_id != train.station_id:
                raise ValidationError("Платформа не принадлежит указанной станции.")
            if platform.current_train_id is not None:
                raise ValidationError("Платформа уже занята другим поездом.")
            platform.current_train_id = train.train_id
        self.trains[train.train_id] = train

    def add_turnstile(self, turnstile: Turnstile) -> None:
        self._ensure_unique(turnstile.turnstile_id, self.turnstiles, "турникет")
        self.get_station(turnstile.station_id)
        self.turnstiles[turnstile.turnstile_id] = turnstile

    def create_passenger(self, full_name: str) -> Passenger:
        name = full_name.strip()
        if not name:
            raise ValidationError("Имя пассажира не может быть пустым.")
        self._passenger_seq += 1
        passenger = Passenger(
            passenger_id=f"P{self._passenger_seq:03d}",
            full_name=name,
        )
        self.passengers[passenger.passenger_id] = passenger
        return passenger

    def next_ticket_id(self) -> str:
        self._ticket_seq += 1
        return f"T{self._ticket_seq:04d}"

    def get_station(self, station_id: str) -> MetroStation:
        return self._get_or_raise(station_id, self.stations, "Станция")

    def get_platform(self, platform_id: str) -> Platform:
        return self._get_or_raise(platform_id, self.platforms, "Платформа")

    def get_train(self, train_id: str) -> Train:
        return self._get_or_raise(train_id, self.trains, "Поезд")

    def get_ticket(self, ticket_id: str) -> Ticket:
        return self._get_or_raise(ticket_id, self.tickets, "Билет")

    def get_turnstile(self, turnstile_id: str) -> Turnstile:
        return self._get_or_raise(turnstile_id, self.turnstiles, "Турникет")

    def get_passenger(self, passenger_id: str) -> Passenger:
        return self._get_or_raise(passenger_id, self.passengers, "Пассажир")

    @staticmethod
    def _ensure_unique(
        entity_id: str,
        storage: dict[str, object],
        entity_name: str,
    ) -> None:
        if entity_id in storage:
            raise ValidationError(
                f"Сущность '{entity_name}' с идентификатором '{entity_id}' уже существует."
            )

    @staticmethod
    def _get_or_raise(
        entity_id: str,
        storage: dict[str, object],
        entity_name: str,
    ) -> object:
        entity = storage.get(entity_id)
        if entity is None:
            raise NotFoundError(f"{entity_name} '{entity_id}' не найден(а).")
        return entity
