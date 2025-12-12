from __future__ import annotations

from datetime import date, datetime

from sportsclub.analytics import AttendanceStats, KPIReport, UsageReport
from sportsclub.equipment import EquipmentItem, EquipmentLoan, EquipmentMaintenance, GearBag
from sportsclub.events import Competition, EventRegistration, SponsorDeal, TrophyCase
from sportsclub.facility import CleaningSchedule, Court, Facility, Locker, PoolLane
from sportsclub.finance import Budget, DiscountCoupon, Invoice, Payment, SubscriptionPlan
from sportsclub.marketing import Campaign, Referral
from sportsclub.members import Coach, HealthProfile, Member, MembershipCard, PlayerContract, Team
from sportsclub.scheduling import Attendance, Booking, ClassSchedule, Session, Waitlist
from sportsclub.security import AccessPass, CameraMonitor, EmergencyDrill, IncidentReport
from sportsclub.support import CommunityProgram, Feedback, SupportTicket
from sportsclub.training import Exercise, InjuryReport, NutritionPlan, TrainingSession, WorkoutPlan
from sportsclub.wellness import Leaderboard, PersonalGoal, WellnessCheck


def run_demo() -> None:
    member = Member(member_id="M001", name="Lena")
    card = MembershipCard(card_number="CARD-1", member_id=member.member_id, status="active")
    health = HealthProfile(member_id=member.member_id, heart_rate=120, cleared=True)
    coach = Coach(coach_id="C01", name="Ilya", certified=True)
    team = Team(name="Falcons", sport="Basketball")
    team.add_member(member)
    contract = PlayerContract(member_id=member.member_id, coach_id=coach.coach_id, expires_on=date(2026, 5, 1))

    courts = Court(court_id="CT-1", sport="Basketball", capacity=10)
    courts.book_slot()
    locker = Locker(locker_id="L-10", assigned_to=None, pin="1234")
    locker.assign(member.member_id)
    cleaning = CleaningSchedule(schedule_id="CL-1")
    cleaning.add_area("Court A")
    cleaning.mark_completed("Court A")
    pool = PoolLane(lane_id="P1", length_m=25)
    pool.reserve(member.member_id)

    schedule = ClassSchedule(schedule_id="SC-1", start=datetime(2025, 5, 5, 18), end=datetime(2025, 5, 5, 19))
    schedule.add_participant(member.member_id)
    booking = Booking(booking_id="B-1", member_id=member.member_id, slot="SC-1")
    session = Session(session_id="SES-1", coach=coach)
    session.add_attendee(member.member_id)
    attendance = Attendance(session_id=session.session_id)
    attendance.mark_present(member.member_id)
    waitlist = Waitlist(session_id=session.session_id)

    plan = WorkoutPlan(plan_id="WP-1", focus="Strength")
    plan.add_exercise("Squat")
    exercise = Exercise(name="Squat", sets=3, reps=10)
    injury = InjuryReport(report_id="IR-1", member_id=member.member_id, severity="low")
    nutrition = NutritionPlan(plan_id="NP-1", calories=2200, protein=150)
    training = TrainingSession(session_id="TS-1", coach=coach, started_at=datetime(2025, 5, 5, 17))
    training.add_attendee(member.member_id)

    item = EquipmentItem(item_id="KB-16", name="Kettlebell", available=True)
    loan = EquipmentLoan(loan_id="EL-1", member_id=member.member_id, item=item)
    loan.checkout()
    maintenance = EquipmentMaintenance(record_id="EM-1", item_id=item.item_id, scheduled_on=date(2025, 6, 1))
    bag = GearBag(bag_id="GB-1", owner_id=member.member_id)
    bag.add_item("Shoes")

    invoice = Invoice(invoice_id="INV-1", member_id=member.member_id, amount=80.0)
    coupon = DiscountCoupon(code="SAVE10", percent=10, expires_on=date(2025, 12, 31))
    invoice.apply_discount(5.0)
    payment = Payment(payment_id="PAY-1", method="card", amount=invoice.amount)
    balance = 0.0
    balance = payment.process(balance)
    subscription = SubscriptionPlan(plan_id="P-MONTH", price=80.0, duration_days=30)
    budget = Budget(budget_id="BDG-1", allocated=5000.0, spent=1200.0)

    pass_card = AccessPass(pass_id="PASS-1", member_id=member.member_id, zones={"gym"})
    pass_card.grant_zone("pool")
    pass_card.validate("pool")
    incident = IncidentReport(report_id="INC-1", description="Slippery floor")
    incident.add_tag("safety")
    camera = CameraMonitor(camera_id="CAM-1", status="online")
    camera.record_alert("Wet floor detected")
    drill = EmergencyDrill(drill_id="DR-1")
    drill.add_participant(member.member_id)
    drill.complete()

    competition = Competition(name="Spring Cup", sport="Basketball")
    competition.add_participant(member.member_id)
    registration = EventRegistration(registration_id="REG-1", member_id=member.member_id, event_name=competition.name)
    sponsor = SponsorDeal(sponsor="LocalGym", amount=2000.0, active=True)
    trophies = TrophyCase(location="Lobby")
    trophies.add_trophy("MVP")

    support_ticket = SupportTicket(ticket_id="SUP-1", member_id=member.member_id, status="open")
    feedback = Feedback(feedback_id="FB-1", member_id=member.member_id, rating=5)
    community = CommunityProgram(program_id="CP-1", title="Youth Clinic")
    community.register(member.member_id)

    usage = UsageReport(report_id="UR-1", sessions=25, active_members=100)
    kpi = KPIReport(period="Q1", retention=0.92, revenue=15000.0)
    stats = AttendanceStats(session_id=session.session_id, attended=12, capacity=15)

    campaign = Campaign(name="Summer Promo")
    campaign.add_channel("email")
    referral = Referral(referral_id="REF-1", referrer_id=member.member_id, referred_id="M002")

    check = WellnessCheck(check_id="WC-1", member_id=member.member_id, resting_hr=65)
    goal = PersonalGoal(goal_id="G-1", member_id=member.member_id, target="5k PR")
    leaderboard = Leaderboard(name="Weekly Miles")
    leaderboard.submit_score(member.member_id, 30)

    print("=== Sports Club Demo ===")
    print(f"Member active: {member.active}, card status: {card.status}")
    print(f"Team size: {team.total_members()}, contract active: {contract.is_active()}")
    print(f"Court bookings: {courts.booked_slots}, Pool reserved by: {pool.reserved_by}")
    print(f"Schedule duration: {schedule.duration_hours()}h, Session coach: {session.coach_name()}")
    print(f"Workout exercises: {plan.exercises}, Nutrition calories: {nutrition.calories}")
    print(f"Equipment available: {item.available}, Bag contents: {bag.contents}")
    print(f"Invoice paid: {invoice.is_paid(balance)}, Budget remaining: {budget.remaining()}")
    print(f"Access zones: {pass_card.zones}, Camera alerts: {camera.alerts}")
    print(f"Competition participants: {competition.total()}, Trophy count: {len(trophies.trophies)}")
    print(f"Support status: {support_ticket.status}, Feedback tags: {feedback.tags}")
    print(f"Usage utilization: {usage.utilization()}, KPI revenue/member: {kpi.revenue_per_member(120)}")
    print(f"Campaign channels: {campaign.channels}, Referral: {referral.summary()}")
    print(f"Leaderboard top: {leaderboard.top_members()}, Wellness HR: {check.resting_hr}")


if __name__ == "__main__":
    run_demo()
