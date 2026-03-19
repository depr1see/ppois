"""Application services for metro operations."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from metro.exceptions import (
    CapacityError,
    SequenceError,
    SafetyError,
    ValidationError,
)
from metro.models import (
    Passenger,
    ScheduleEntry,
    Ticket,
    TicketStatus,
    TrainStatus,
)
from metro.repository import MetroRepository

TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def parse_time_label(time_label: str) -> int:
    """Parse HH:MM to minutes from midnight."""
    text = time_label.strip()
    if not TIME_PATTERN.match(text):
        raise ValidationError("Некорректный формат времени. Используйте HH:MM.")
    hours, minutes = text.split(":")
    return int(hours) * 60 + int(minutes)


@dataclass(slots=True)
class TicketService:
    """Ticket sales."""

    repository: MetroRepository

    def sell_ticket(
        self,
        passenger_id: str,
        origin_station_id: str,
        destination_station_id: str,
    ) -> Ticket:
        passenger = self.repository.get_passenger(passenger_id)
        self.repository.get_station(origin_station_id)
        self.repository.get_station(destination_station_id)

        if origin_station_id == destination_station_id:
            raise ValidationError("Станции отправления и прибытия должны отличаться.")
        if passenger.on_train_id is not None:
            raise SequenceError("Нельзя купить билет во время поездки.")
        if passenger.active_ticket_id is not None:
            ticket = self.repository.get_ticket(passenger.active_ticket_id)
            if ticket.status is TicketStatus.ACTIVE:
                raise SequenceError("У пассажира уже есть активный билет.")

        ticket = Ticket(
            ticket_id=self.repository.next_ticket_id(),
            passenger_id=passenger_id,
            origin_station_id=origin_station_id,
            destination_station_id=destination_station_id,
        )
        self.repository.tickets[ticket.ticket_id] = ticket
        passenger.active_ticket_id = ticket.ticket_id
        passenger.current_station_id = None
        passenger.passed_turnstile = False
        return ticket


@dataclass(slots=True)
class SafetyService:
    """Safety and turnstile operations."""

    repository: MetroRepository

    def pass_turnstile(self, passenger_id: str, turnstile_id: str) -> None:
        passenger = self.repository.get_passenger(passenger_id)
        turnstile = self.repository.get_turnstile(turnstile_id)

        if not turnstile.is_operational:
            raise SafetyError("Турникет отключен. Доступ временно запрещен.")
        if passenger.on_train_id is not None:
            raise SequenceError("Пассажир уже находится в поезде.")
        ticket = self._require_active_ticket(passenger)
        if ticket.origin_station_id != turnstile.station_id:
            raise SequenceError("Турникет не соответствует станции отправления билета.")
        if passenger.passed_turnstile and passenger.current_station_id == turnstile.station_id:
            raise SequenceError("Пассажир уже прошел через турникет этой станции.")

        passenger.current_station_id = turnstile.station_id
        passenger.passed_turnstile = True
        turnstile.last_security_check = datetime.now()

    def set_turnstile_state(self, turnstile_id: str, is_operational: bool) -> None:
        turnstile = self.repository.get_turnstile(turnstile_id)
        turnstile.is_operational = is_operational

    def run_security_check(self, turnstile_id: str) -> datetime:
        turnstile = self.repository.get_turnstile(turnstile_id)
        turnstile.last_security_check = datetime.now()
        return turnstile.last_security_check

    def _require_active_ticket(self, passenger: Passenger) -> Ticket:
        if passenger.active_ticket_id is None:
            raise SequenceError("У пассажира нет активного билета.")
        ticket = self.repository.get_ticket(passenger.active_ticket_id)
        if ticket.status is not TicketStatus.ACTIVE:
            raise SequenceError("Активный билет отсутствует.")
        return ticket


@dataclass(slots=True)
class PassengerFlowService:
    """Boarding and disembark operations."""

    repository: MetroRepository

    def board_passenger(self, passenger_id: str, train_id: str) -> None:
        passenger = self.repository.get_passenger(passenger_id)
        train = self.repository.get_train(train_id)

        if train.status is not TrainStatus.IN_SERVICE:
            raise SequenceError("Посадка невозможна: поезд находится на обслуживании.")
        if passenger.on_train_id is not None:
            raise SequenceError("Пассажир уже в поезде.")
        if not passenger.passed_turnstile:
            raise SequenceError("Сначала нужно пройти через турникет.")
        if passenger.current_station_id != train.station_id:
            raise SequenceError(
                "Посадка невозможна: пассажир и поезд находятся на разных станциях."
            )
        if train.free_seats <= 0:
            raise CapacityError("Посадка невозможна: в поезде нет свободных мест.")

        ticket = self._require_active_ticket(passenger)
        if ticket.origin_station_id != train.station_id:
            raise SequenceError("Нельзя сесть в поезд не на станции отправления билета.")

        train.passenger_ids.add(passenger.passenger_id)
        passenger.on_train_id = train.train_id
        passenger.current_station_id = None
        passenger.passed_turnstile = False

    def disembark_passenger(self, passenger_id: str, station_id: str) -> Ticket:
        passenger = self.repository.get_passenger(passenger_id)
        if passenger.on_train_id is None:
            raise SequenceError("Пассажир не находится в поезде.")

        train = self.repository.get_train(passenger.on_train_id)
        if train.station_id != station_id:
            raise SequenceError("Высадка невозможна: поезд находится на другой станции.")

        ticket = self._require_active_ticket(passenger)
        if ticket.destination_station_id != station_id:
            raise SequenceError("Высадка разрешена только на станции назначения по билету.")
        if passenger.passenger_id not in train.passenger_ids:
            raise SequenceError("Системная ошибка: пассажир не найден в составе поезда.")

        train.passenger_ids.remove(passenger.passenger_id)
        passenger.on_train_id = None
        passenger.current_station_id = station_id
        passenger.active_ticket_id = None
        passenger.passed_turnstile = False
        ticket.status = TicketStatus.USED
        return ticket

    def _require_active_ticket(self, passenger: Passenger) -> Ticket:
        if passenger.active_ticket_id is None:
            raise SequenceError("Для операции требуется активный билет.")
        ticket = self.repository.get_ticket(passenger.active_ticket_id)
        if ticket.status is not TicketStatus.ACTIVE:
            raise SequenceError("Активный билет отсутствует.")
        return ticket


@dataclass(slots=True)
class TrainService:
    """Train movement and maintenance operations."""

    repository: MetroRepository

    def move_train(self, train_id: str, station_id: str, platform_id: str) -> None:
        train = self.repository.get_train(train_id)
        self.repository.get_station(station_id)
        platform = self.repository.get_platform(platform_id)

        if train.status is not TrainStatus.IN_SERVICE:
            raise SequenceError("Поезд на обслуживании. Перемещение недоступно.")
        if platform.station_id != station_id:
            raise ValidationError("Платформа не относится к выбранной станции.")
        if platform.current_train_id not in (None, train.train_id):
            raise SequenceError("Платформа занята другим поездом.")

        self._release_train_platform(train)
        train.station_id = station_id
        train.platform_id = platform_id
        platform.current_train_id = train.train_id

    def send_to_maintenance(self, train_id: str) -> None:
        train = self.repository.get_train(train_id)
        if train.passenger_ids:
            raise SequenceError("Нельзя отправить поезд на обслуживание с пассажирами.")
        if train.status is TrainStatus.MAINTENANCE:
            raise SequenceError("Поезд уже находится на обслуживании.")

        self._release_train_platform(train)
        train.status = TrainStatus.MAINTENANCE
        train.platform_id = None

    def return_from_maintenance(
        self,
        train_id: str,
        station_id: str,
        platform_id: str,
    ) -> None:
        train = self.repository.get_train(train_id)
        self.repository.get_station(station_id)
        platform = self.repository.get_platform(platform_id)

        if train.status is not TrainStatus.MAINTENANCE:
            raise SequenceError("Поезд не находится на обслуживании.")
        if platform.station_id != station_id:
            raise ValidationError("Платформа не относится к указанной станции.")
        if platform.current_train_id not in (None, train.train_id):
            raise SequenceError("Платформа занята другим поездом.")

        train.status = TrainStatus.IN_SERVICE
        train.station_id = station_id
        train.platform_id = platform_id
        platform.current_train_id = train.train_id

    def _release_train_platform(self, train) -> None:
        if train.platform_id is None:
            return
        platform = self.repository.get_platform(train.platform_id)
        if platform.current_train_id == train.train_id:
            platform.current_train_id = None


@dataclass(slots=True)
class ScheduleService:
    """Operations for schedule maintenance."""

    repository: MetroRepository

    def add_entry(self, train_id: str, station_id: str, time_label: str) -> ScheduleEntry:
        self.repository.get_train(train_id)
        self.repository.get_station(station_id)
        time_minutes = parse_time_label(time_label)

        for entry in self.repository.schedule.entries:
            if entry.train_id == train_id and entry.time_minutes == time_minutes:
                raise ValidationError(
                    "Для этого поезда уже существует запись расписания на это время."
                )

        new_entry = ScheduleEntry(
            time_minutes=time_minutes,
            train_id=train_id,
            station_id=station_id,
        )
        self.repository.schedule.entries.append(new_entry)
        self.repository.schedule.entries.sort(key=lambda item: (item.train_id, item.time_minutes))
        return new_entry

    def shift_train_schedule(self, train_id: str, delta_minutes: int) -> None:
        self.repository.get_train(train_id)
        updated_entries: list[ScheduleEntry] = []
        has_train_entries = False

        for entry in self.repository.schedule.entries:
            if entry.train_id != train_id:
                updated_entries.append(entry)
                continue

            has_train_entries = True
            shifted_time = (entry.time_minutes + delta_minutes) % (24 * 60)
            updated_entries.append(
                ScheduleEntry(
                    time_minutes=shifted_time,
                    train_id=entry.train_id,
                    station_id=entry.station_id,
                )
            )

        if not has_train_entries:
            raise SequenceError("Для выбранного поезда нет записей в расписании.")

        updated_entries.sort(key=lambda item: (item.train_id, item.time_minutes))
        self.repository.schedule.entries = updated_entries

    def get_train_entries(self, train_id: str) -> list[ScheduleEntry]:
        self.repository.get_train(train_id)
        return sorted(
            (entry for entry in self.repository.schedule.entries if entry.train_id == train_id),
            key=lambda item: item.time_minutes,
        )
