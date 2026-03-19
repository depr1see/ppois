"""Unit tests for metro system."""

from __future__ import annotations

import unittest

from metro.exceptions import SafetyError, SequenceError, ValidationError
from metro.models import TicketStatus
from metro.system import MetroSystem


class MetroSystemTestCase(unittest.TestCase):
    """Tests for key operations and invalid sequences."""

    def setUp(self) -> None:
        self.system = MetroSystem.create_with_demo_data()
        self.passenger = self.system.register_passenger("Иван Петров")

    def test_ticket_sale_success(self) -> None:
        ticket = self.system.sell_ticket(
            passenger_id=self.passenger.passenger_id,
            origin_station_id="ST01",
            destination_station_id="ST03",
        )

        self.assertEqual(ticket.status, TicketStatus.ACTIVE)
        self.assertEqual(ticket.origin_station_id, "ST01")
        self.assertEqual(ticket.destination_station_id, "ST03")

    def test_boarding_without_ticket_fails(self) -> None:
        with self.assertRaises(SequenceError):
            self.system.board_passenger(self.passenger.passenger_id, "TR01")

    def test_full_flow_with_boarding_and_disembark(self) -> None:
        self.system.sell_ticket(self.passenger.passenger_id, "ST01", "ST03")
        self.system.pass_turnstile(self.passenger.passenger_id, "TU01")
        self.system.board_passenger(self.passenger.passenger_id, "TR01")
        self.system.move_train("TR01", "ST03", "PL03")
        ticket = self.system.disembark_passenger(self.passenger.passenger_id, "ST03")

        self.assertEqual(ticket.status, TicketStatus.USED)
        passenger = self.system.repository.get_passenger(self.passenger.passenger_id)
        self.assertIsNone(passenger.active_ticket_id)
        self.assertIsNone(passenger.on_train_id)
        self.assertEqual(passenger.current_station_id, "ST03")

    def test_maintenance_with_passengers_fails(self) -> None:
        self.system.sell_ticket(self.passenger.passenger_id, "ST01", "ST03")
        self.system.pass_turnstile(self.passenger.passenger_id, "TU01")
        self.system.board_passenger(self.passenger.passenger_id, "TR01")

        with self.assertRaises(SequenceError):
            self.system.send_train_to_maintenance("TR01")

    def test_turnstile_disabled_blocks_passage(self) -> None:
        self.system.sell_ticket(self.passenger.passenger_id, "ST01", "ST03")
        self.system.set_turnstile_state("TU01", is_operational=False)

        with self.assertRaises(SafetyError):
            self.system.pass_turnstile(self.passenger.passenger_id, "TU01")

    def test_schedule_shift_changes_all_train_entries(self) -> None:
        before = [entry.time_minutes for entry in self.system.get_train_schedule("TR01")]
        self.system.shift_train_schedule("TR01", 15)
        after = [entry.time_minutes for entry in self.system.get_train_schedule("TR01")]

        expected = [(value + 15) % (24 * 60) for value in before]
        self.assertEqual(after, expected)

    def test_invalid_schedule_time_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.system.add_schedule_entry("TR01", "ST01", "25:99")


if __name__ == "__main__":
    unittest.main()
