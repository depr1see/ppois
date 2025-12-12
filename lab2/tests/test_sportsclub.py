from datetime import date, datetime
import pytest

from sportsclub.equipment import EquipmentItem, EquipmentLoan, EquipmentMaintenance, GearBag
from sportsclub.exceptions import (
    AccessDeniedException,
    CapacityExceededException,
    CouponExpiredException,
    DoubleBookingException,
    EquipmentUnavailableException,
    InvalidMembershipException,
    PaymentFailedException,
)
from sportsclub.facility import CleaningSchedule, Court, Facility, Locker, PoolLane
from sportsclub.finance import Budget, DiscountCoupon, Invoice, Payment, SubscriptionPlan
from sportsclub.members import Coach, Member, MembershipCard, Team
from sportsclub.scheduling import ClassSchedule, Session
from sportsclub.security import AccessPass, CameraMonitor, EmergencyDrill, IncidentReport


def test_membership_and_access() -> None:
    member = Member(member_id="M1", name="Alex")
    schedule = ClassSchedule(schedule_id="SC1", start=datetime(2025, 1, 1, 9), end=datetime(2025, 1, 1, 10))
    schedule.add_participant(member.member_id)
    member.enroll_class("SC1")
    member.suspend()
    with pytest.raises(InvalidMembershipException):
        member.enroll_class("SC1")

    access = AccessPass(pass_id="P1", member_id=member.member_id, zones={"gym"})
    access.grant_zone("pool")
    assert access.validate("pool")


def test_facility_capacity_and_booking() -> None:
    facility = Facility(name="Main Club", address="123 Street")
    facility.add_amenity("sauna")
    assert facility.has_amenity("sauna")

    court = Court(court_id="C1", sport="tennis", capacity=1)
    court.book_slot()
    court.release_slot()
    with pytest.raises(CapacityExceededException):
        court.book_slot(); court.book_slot()

    lane = PoolLane(lane_id="L1", length_m=25)
    lane.reserve("M1")
    with pytest.raises(DoubleBookingException):
        lane.reserve("M2")
    lane.release()

    locker = Locker(locker_id="L1", assigned_to=None, pin="1234")
    locker.assign("M1")
    assert locker.open("1234")
    with pytest.raises(AccessDeniedException):
        locker.open("0000")

    cleaning = CleaningSchedule(schedule_id="CL1")
    cleaning.add_area("Court")
    cleaning.mark_completed("Court")


def test_finance_payments_and_coupons() -> None:
    invoice = Invoice(invoice_id="I1", member_id="M1", amount=100.0)
    coupon = DiscountCoupon(code="OFF10", percent=10, expires_on=date(2025, 12, 31))
    invoice.apply_discount(5.0)
    assert coupon.apply(invoice.amount) < invoice.amount
    assert coupon.is_valid()

    plan = SubscriptionPlan(plan_id="P1", price=90.0, duration_days=30)
    plan.extend(15)
    assert plan.monthly_rate() > 0

    budget = Budget(budget_id="B1", allocated=500.0, spent=100.0)
    budget.spend(200.0)
    assert budget.remaining() == 200.0

    with pytest.raises(CouponExpiredException):
        coupon.apply(invoice.amount, today=date(2026, 1, 1))

    payment = Payment(payment_id="P1", method="card", amount=-10.0)
    with pytest.raises(PaymentFailedException):
        payment.process(0.0)
    assert Payment(payment_id="P2", method="cash", amount=10.0).refund() == -10.0


def test_equipment_loans_and_security() -> None:
    item = EquipmentItem(item_id="E1", name="Ball", available=False)
    with pytest.raises(EquipmentUnavailableException):
        EquipmentLoan(loan_id="L1", member_id="M1", item=item).checkout()
    item.mark_available()
    loan = EquipmentLoan(loan_id="L2", member_id="M1", item=item)
    loan.checkout()
    loan.checkin()

    maintenance = EquipmentMaintenance(record_id="EM1", item_id=item.item_id, scheduled_on=date.today())
    maintenance.reschedule(date.today())
    assert maintenance.is_due()

    bag = GearBag(bag_id="G1", owner_id="M1")
    bag.add_item("Water")
    bag.remove_item("Water")

    camera = CameraMonitor(camera_id="CAM1", status="online")
    camera.record_alert("Test")
    camera.clear_alerts()

    incident = IncidentReport(report_id="INC1", description="Minor")
    incident.add_tag("notice")
    incident.escalate()

    drill = EmergencyDrill(drill_id="DR1")
    drill.add_participant("M1")
    drill.complete()

    card = MembershipCard(card_number="CARD1", member_id="M1", status="active")
    card.deactivate()
    card.assign_member("M2")


def test_team_and_coach_session() -> None:
    coach = Coach(coach_id="C1", name="Ilya", certified=True)
    session = Session(session_id="S1", coach=coach)
    session.add_attendee("M1")
    assert session.coach_name() == "Ilya"

    team = Team(name="Wolves", sport="Swim")
    team.add_member(Member(member_id="M2", name="Nina"))
    assert team.total_members() == 1
