Sports Club Domain Model
==========================

Member 4 2 1 -> ClassSchedule  
MembershipCard 3 2 1 -> Member  
HealthProfile 3 2 1 -> Member  
Coach 3 2 1 -> Team  
Team 3 2 1 -> Member  
PlayerContract 3 2 1 -> Coach  
Facility 3 2 1 -> -  
Court 4 2 1 -> Member  
GymRoom 3 2 1 -> -  
PoolLane 3 2 1 -> Member  
Locker 3 2 1 -> Member  
CleaningSchedule 3 2 1 -> Facility  
ClassSchedule 4 2 1 -> Member  
Booking 3 2 1 -> Member  
Session 3 2 1 -> Coach  
Attendance 3 2 1 -> Member  
Waitlist 3 2 1 -> Member  
Invoice 3 2 1 -> Member  
Payment 3 2 1 -> Invoice  
SubscriptionPlan 3 2 1 -> Member  
DiscountCoupon 3 2 1 -> Invoice  
Budget 3 2 1 -> Campaign  
WorkoutPlan 3 2 1 -> Exercise  
Exercise 3 2 1 -> WorkoutPlan  
NutritionPlan 3 2 1 -> Member  
InjuryReport 3 2 1 -> Member  
TrainingSession 4 2 1 -> Coach  
EquipmentItem 3 2 1 -> -  
EquipmentLoan 3 2 1 -> EquipmentItem  
EquipmentMaintenance 3 2 1 -> EquipmentItem  
GearBag 3 2 1 -> Member  
AccessPass 3 2 1 -> Member  
IncidentReport 3 2 1 -> -  
CameraMonitor 3 2 1 -> IncidentReport  
EmergencyDrill 3 2 1 -> Member  
Competition 3 2 1 -> Member  
EventRegistration 3 2 1 -> Member  
SponsorDeal 3 2 1 -> -  
TrophyCase 3 2 1 -> SponsorDeal  
SupportTicket 3 2 1 -> Member  
Feedback 4 2 1 -> Member  
CommunityProgram 3 2 1 -> Member  
UsageReport 4 2 1 -> Member  
KPIReport 3 2 1 -> Budget  
AttendanceStats 3 2 1 -> Session  
Campaign 3 2 1 -> Budget  
Referral 3 2 1 -> Member  
WellnessCheck 3 2 1 -> HealthProfile  
PersonalGoal 3 2 1 -> Member  
Leaderboard 3 2 1 -> Member  

Exceptions (12)
---------------
AccessDeniedException, PaymentFailedException, CapacityExceededException, ScheduleConflictException, InvalidMembershipException, EquipmentUnavailableException, HealthRiskException, CouponExpiredException, OverdueBalanceException, DoubleBookingException, UnauthorizedCoachException, SafetyIncidentException.

Summary
-------
Classes: 50  
Fields: 150  
Behaviors: 100  
Associations: 50  
Exceptions: 12  
Modules: 13  
Tests: tests/test_sportsclub.py