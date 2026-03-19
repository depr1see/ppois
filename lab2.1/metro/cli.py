"""Russian CLI for metro system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from metro.exceptions import MetroError
from metro.models import Passenger, TicketStatus, TrainStatus
from metro.system import MetroSystem

Action = Callable[[], None]


@dataclass(slots=True)
class MenuItem:
    """Single menu item."""

    title: str
    handler: Action


class MetroCli:
    """Command line interface for metro domain."""

    def __init__(self, system: MetroSystem) -> None:
        self.system = system
        self.menu: dict[str, MenuItem] = {
            "1": MenuItem("Показать состояние системы", self.show_state),
            "2": MenuItem("Зарегистрировать пассажира", self.register_passenger),
            "3": MenuItem("Продать билет", self.sell_ticket),
            "4": MenuItem("Пропустить пассажира через турникет", self.pass_turnstile),
            "5": MenuItem("Посадить пассажира в поезд", self.board_passenger),
            "6": MenuItem("Высадить пассажира из поезда", self.disembark_passenger),
            "7": MenuItem("Переместить поезд на станцию", self.move_train),
            "8": MenuItem("Отправить поезд на обслуживание", self.send_train_to_maintenance),
            "9": MenuItem("Вернуть поезд с обслуживания", self.return_train_to_service),
            "10": MenuItem("Добавить запись в расписание", self.add_schedule_entry),
            "11": MenuItem("Сдвинуть расписание поезда", self.shift_schedule),
            "12": MenuItem("Операции безопасности турникета", self.turnstile_security_menu),
            "0": MenuItem("Выход", self.exit_program),
        }
        self._is_running = True

    def run(self) -> None:
        """Start CLI loop."""
        print("Система управления метро (CLI)")
        print("Все команды выполняются в интерактивном режиме.")

        while self._is_running:
            self.print_menu()
            try:
                choice = input("Выберите пункт меню: ").strip()
            except EOFError:
                print("\nПолучен конец ввода. Завершение программы.")
                return

            menu_item = self.menu.get(choice)
            if menu_item is None:
                print("Некорректный пункт меню. Введите номер из списка.")
                continue

            try:
                menu_item.handler()
            except MetroError as error:
                print(f"Ошибка домена: {error}")
            except KeyboardInterrupt:
                print("\nОперация прервана пользователем.")

    def print_menu(self) -> None:
        """Print main menu."""
        print("\nГлавное меню:")
        for key in sorted(self.menu.keys(), key=lambda value: int(value)):
            item = self.menu[key]
            print(f"{key}. {item.title}")

    def show_state(self) -> None:
        """Show current system state."""
        print("\nСтанции:")
        for station in self.system.list_stations():
            print(f"- {station.station_id}: {station.name}")

        print("\nПлатформы:")
        for platform in self.system.list_platforms():
            occupied = platform.current_train_id or "свободна"
            print(
                f"- {platform.platform_id}: станция={platform.station_id}, "
                f"поезд={occupied}"
            )

        print("\nПоезда:")
        for train in self.system.list_trains():
            status = self._train_status_label(train.status)
            print(
                f"- {train.train_id}: статус={status}, станция={train.station_id}, "
                f"платформа={train.platform_id or 'нет'}, пассажиры={len(train.passenger_ids)}/{train.capacity}"
            )

        print("\nПассажиры:")
        passengers = self.system.list_passengers()
        if not passengers:
            print("- нет зарегистрированных пассажиров")
        for passenger in passengers:
            print(f"- {passenger.passenger_id}: {passenger.full_name} ({self._passenger_state(passenger)})")

        print("\nБилеты:")
        tickets = self.system.list_tickets()
        if not tickets:
            print("- билеты еще не продавались")
        for ticket in tickets:
            status = "активен" if ticket.status is TicketStatus.ACTIVE else "использован"
            print(
                f"- {ticket.ticket_id}: пассажир={ticket.passenger_id}, "
                f"маршрут={ticket.origin_station_id}->{ticket.destination_station_id}, "
                f"статус={status}"
            )

        print("\nТурникеты:")
        for turnstile in self.system.list_turnstiles():
            mode = "включен" if turnstile.is_operational else "выключен"
            last_check = (
                turnstile.last_security_check.strftime("%Y-%m-%d %H:%M:%S")
                if turnstile.last_security_check
                else "проверка не проводилась"
            )
            print(
                f"- {turnstile.turnstile_id}: станция={turnstile.station_id}, "
                f"состояние={mode}, последняя проверка={last_check}"
            )

        print("\nРасписание:")
        schedule = self.system.list_schedule()
        if not schedule:
            print("- расписание пустое")
        for entry in schedule:
            print(
                f"- поезд={entry.train_id}, станция={entry.station_id}, время={entry.time_label}"
            )

    def register_passenger(self) -> None:
        """Register new passenger."""
        full_name = self.read_required("Введите ФИО пассажира: ")
        passenger = self.system.register_passenger(full_name)
        print(f"Пассажир создан: {passenger.passenger_id} ({passenger.full_name})")

    def sell_ticket(self) -> None:
        """Sell ticket."""
        passenger_id = self.read_required("Введите ID пассажира (например, P001): ")
        origin_station_id = self.read_required("Введите ID станции отправления: ")
        destination_station_id = self.read_required("Введите ID станции назначения: ")
        ticket = self.system.sell_ticket(
            passenger_id=passenger_id,
            origin_station_id=origin_station_id,
            destination_station_id=destination_station_id,
        )
        print(
            f"Билет {ticket.ticket_id} продан: "
            f"{ticket.origin_station_id} -> {ticket.destination_station_id}"
        )

    def pass_turnstile(self) -> None:
        """Pass passenger through turnstile."""
        passenger_id = self.read_required("Введите ID пассажира: ")
        turnstile_id = self.read_required("Введите ID турникета: ")
        self.system.pass_turnstile(passenger_id=passenger_id, turnstile_id=turnstile_id)
        print("Пассажир успешно прошел через турникет.")

    def board_passenger(self) -> None:
        """Board passenger to train."""
        passenger_id = self.read_required("Введите ID пассажира: ")
        train_id = self.read_required("Введите ID поезда: ")
        self.system.board_passenger(passenger_id=passenger_id, train_id=train_id)
        print("Пассажир посажен в поезд.")

    def disembark_passenger(self) -> None:
        """Disembark passenger from train."""
        passenger_id = self.read_required("Введите ID пассажира: ")
        station_id = self.read_required("Введите ID станции высадки: ")
        ticket = self.system.disembark_passenger(passenger_id=passenger_id, station_id=station_id)
        print(
            f"Пассажир высажен. Билет {ticket.ticket_id} помечен как использованный."
        )

    def move_train(self) -> None:
        """Move train to selected station/platform."""
        train_id = self.read_required("Введите ID поезда: ")
        station_id = self.read_required("Введите ID станции назначения: ")
        platform_id = self.read_required("Введите ID платформы назначения: ")
        self.system.move_train(train_id=train_id, station_id=station_id, platform_id=platform_id)
        print("Поезд перемещен.")

    def send_train_to_maintenance(self) -> None:
        """Send train to maintenance."""
        train_id = self.read_required("Введите ID поезда: ")
        self.system.send_train_to_maintenance(train_id)
        print("Поезд отправлен на обслуживание.")

    def return_train_to_service(self) -> None:
        """Return train from maintenance."""
        train_id = self.read_required("Введите ID поезда: ")
        station_id = self.read_required("Введите ID станции: ")
        platform_id = self.read_required("Введите ID платформы: ")
        self.system.return_train_to_service(
            train_id=train_id,
            station_id=station_id,
            platform_id=platform_id,
        )
        print("Поезд возвращен в эксплуатацию.")

    def add_schedule_entry(self) -> None:
        """Add schedule record."""
        train_id = self.read_required("Введите ID поезда: ")
        station_id = self.read_required("Введите ID станции: ")
        time_label = self.read_required("Введите время в формате HH:MM: ")
        entry = self.system.add_schedule_entry(
            train_id=train_id,
            station_id=station_id,
            time_label=time_label,
        )
        print(
            f"Запись добавлена: поезд={entry.train_id}, станция={entry.station_id}, время={entry.time_label}"
        )

    def shift_schedule(self) -> None:
        """Shift schedule for selected train."""
        train_id = self.read_required("Введите ID поезда: ")
        delta = self.read_int("Введите сдвиг в минутах (может быть отрицательным): ")
        self.system.shift_train_schedule(train_id=train_id, delta_minutes=delta)
        print("Расписание поезда обновлено.")

    def turnstile_security_menu(self) -> None:
        """Submenu with turnstile safety operations."""
        print("\nОперации безопасности турникета:")
        print("1. Провести проверку турникета")
        print("2. Включить турникет")
        print("3. Выключить турникет")
        choice = self.read_required("Выберите операцию (1-3): ")

        if choice == "1":
            turnstile_id = self.read_required("Введите ID турникета: ")
            checked_at = self.system.run_turnstile_check(turnstile_id)
            print(f"Проверка выполнена: {self.format_datetime(checked_at)}")
            return

        if choice in {"2", "3"}:
            turnstile_id = self.read_required("Введите ID турникета: ")
            self.system.set_turnstile_state(turnstile_id, is_operational=choice == "2")
            state = "включен" if choice == "2" else "выключен"
            print(f"Турникет {turnstile_id} теперь {state}.")
            return

        print("Некорректный выбор операции безопасности.")

    def exit_program(self) -> None:
        """Exit from CLI loop."""
        self._is_running = False
        print("Работа программы завершена.")

    @staticmethod
    def read_required(prompt: str) -> str:
        """Read non-empty input value."""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Пустое значение недопустимо. Повторите ввод.")

    @staticmethod
    def read_int(prompt: str) -> int:
        """Read integer from CLI input."""
        while True:
            raw_value = input(prompt).strip()
            try:
                return int(raw_value)
            except ValueError:
                print("Введите целое число.")

    @staticmethod
    def format_datetime(value: datetime) -> str:
        """Format datetime in local representation."""
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _train_status_label(status: TrainStatus) -> str:
        if status is TrainStatus.IN_SERVICE:
            return "в эксплуатации"
        return "на обслуживании"

    @staticmethod
    def _passenger_state(passenger: Passenger) -> str:
        if passenger.on_train_id:
            return f"в поезде {passenger.on_train_id}"
        if passenger.current_station_id:
            return f"на станции {passenger.current_station_id}"
        if passenger.active_ticket_id:
            return f"билет {passenger.active_ticket_id}, ожидает турникет"
        return "вне системы метро"
