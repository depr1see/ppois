"""Facade for metro operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from metro.models import (
    MetroStation,
    Passenger,
    Platform,
    ScheduleEntry,
    Ticket,
    Train,
    Turnstile,
)
from metro.repository import MetroRepository
from metro.services import (
    PassengerFlowService,
    SafetyService,
    ScheduleService,
    TicketService,
    TrainService,
)


@dataclass(slots=True)
class MetroSystem:
    """High-level API for metro application and CLI."""

    repository: MetroRepository
    ticket_service: TicketService
    safety_service: SafetyService
    passenger_flow_service: PassengerFlowService
    train_service: TrainService
    schedule_service: ScheduleService

    @classmethod
    def create_with_demo_data(cls) -> "MetroSystem":
        repository = MetroRepository()
        system = cls(
            repository=repository,
            ticket_service=TicketService(repository),
            safety_service=SafetyService(repository),
            passenger_flow_service=PassengerFlowService(repository),
            train_service=TrainService(repository),
            schedule_service=ScheduleService(repository),
        )
        system._load_demo_data()
        return system

    def register_passenger(self, full_name: str) -> Passenger:
        return self.repository.create_passenger(full_name)

    def sell_ticket(
        self,
        passenger_id: str,
        origin_station_id: str,
        destination_station_id: str,
    ) -> Ticket:
        return self.ticket_service.sell_ticket(
            passenger_id=passenger_id,
            origin_station_id=origin_station_id,
            destination_station_id=destination_station_id,
        )

    def pass_turnstile(self, passenger_id: str, turnstile_id: str) -> None:
        self.safety_service.pass_turnstile(passenger_id, turnstile_id)

    def set_turnstile_state(self, turnstile_id: str, is_operational: bool) -> None:
        self.safety_service.set_turnstile_state(turnstile_id, is_operational)

    def run_turnstile_check(self, turnstile_id: str) -> datetime:
        return self.safety_service.run_security_check(turnstile_id)

    def board_passenger(self, passenger_id: str, train_id: str) -> None:
        self.passenger_flow_service.board_passenger(passenger_id, train_id)

    def disembark_passenger(self, passenger_id: str, station_id: str) -> Ticket:
        return self.passenger_flow_service.disembark_passenger(passenger_id, station_id)

    def move_train(self, train_id: str, station_id: str, platform_id: str) -> None:
        self.train_service.move_train(train_id, station_id, platform_id)

    def send_train_to_maintenance(self, train_id: str) -> None:
        self.train_service.send_to_maintenance(train_id)

    def return_train_to_service(
        self,
        train_id: str,
        station_id: str,
        platform_id: str,
    ) -> None:
        self.train_service.return_from_maintenance(train_id, station_id, platform_id)

    def add_schedule_entry(
        self,
        train_id: str,
        station_id: str,
        time_label: str,
    ) -> ScheduleEntry:
        return self.schedule_service.add_entry(train_id, station_id, time_label)

    def shift_train_schedule(self, train_id: str, delta_minutes: int) -> None:
        self.schedule_service.shift_train_schedule(train_id, delta_minutes)

    def get_train_schedule(self, train_id: str) -> list[ScheduleEntry]:
        return self.schedule_service.get_train_entries(train_id)

    def list_stations(self) -> list[MetroStation]:
        return sorted(self.repository.stations.values(), key=lambda item: item.station_id)

    def list_platforms(self) -> list[Platform]:
        return sorted(self.repository.platforms.values(), key=lambda item: item.platform_id)

    def list_trains(self) -> list[Train]:
        return sorted(self.repository.trains.values(), key=lambda item: item.train_id)

    def list_passengers(self) -> list[Passenger]:
        return sorted(self.repository.passengers.values(), key=lambda item: item.passenger_id)

    def list_tickets(self) -> list[Ticket]:
        return sorted(self.repository.tickets.values(), key=lambda item: item.ticket_id)

    def list_turnstiles(self) -> list[Turnstile]:
        return sorted(self.repository.turnstiles.values(), key=lambda item: item.turnstile_id)

    def list_schedule(self) -> list[ScheduleEntry]:
        return sorted(
            self.repository.schedule.entries,
            key=lambda item: (item.train_id, item.time_minutes),
        )

    def _load_demo_data(self) -> None:
        for station in (
            MetroStation("ST01", "Центральная"),
            MetroStation("ST02", "Площадь Победы"),
            MetroStation("ST03", "Восточная"),
        ):
            self.repository.add_station(station)

        for platform in (
            Platform("PL01", "ST01"),
            Platform("PL02", "ST02"),
            Platform("PL03", "ST03"),
            Platform("PL04", "ST02"),
        ):
            self.repository.add_platform(platform)

        for train in (
            Train("TR01", capacity=3, station_id="ST01", platform_id="PL01"),
            Train("TR02", capacity=2, station_id="ST02", platform_id="PL04"),
        ):
            self.repository.add_train(train)

        for turnstile in (
            Turnstile("TU01", station_id="ST01"),
            Turnstile("TU02", station_id="ST02"),
            Turnstile("TU03", station_id="ST03"),
        ):
            self.repository.add_turnstile(turnstile)

        self.add_schedule_entry("TR01", "ST01", "08:00")
        self.add_schedule_entry("TR01", "ST02", "08:12")
        self.add_schedule_entry("TR01", "ST03", "08:25")
        self.add_schedule_entry("TR02", "ST02", "08:05")
        self.add_schedule_entry("TR02", "ST01", "08:20")
