Banking Domain Model
===================

BankAccount 3 2 -> Customer
SavingsAccount 3 2 -> Beneficiary
CheckingAccount 3 2 -> Customer
BusinessAccount 3 2 -> EmployerInfo
AccountBundle 3 2 -> BankAccount, Customer
Customer 3 2 -> BankAccount
CustomerProfile 3 2 -> Customer
Address 3 2 -> Customer
EmployerInfo 3 2 -> Customer
Beneficiary 3 2 -> BankAccount
DebitCard 3 2 -> BankAccount
CreditCard 3 2 -> BankAccount
CardControl 3 2 -> DebitCard
CardPIN 3 2 -> DebitCard
CardReward 3 2 -> CreditCard
Transaction 3 2 -> BankAccount
TransferOrder 3 2 -> BankAccount
PaymentRequest 3 2 -> BankAccount
StandingInstruction 3 2 -> BankAccount
FXExchange 3 2 -> BankAccount
LoanApplication 3 2 -> Customer
LoanAgreement 3 2 -> CollateralItem
MortgageAccount 3 2 -> Customer
CollateralItem 3 2 -> Customer
RepaymentSchedule 3 2 -> LoanAgreement
AuthSession 3 2 -> Customer
TwoFactorDevice 3 2 -> Customer
AccessLog 3 2 -> Customer
FraudAlert 3 2 -> BankAccount
SecurityPolicy 3 2 -> BankAccount
KYCCheck 3 2 -> Customer
AMLReport 3 2 -> BankAccount
SanctionsScreening 3 2 -> Customer
AuditTrail 3 2 -> Customer
ConsentRecord 3 2 -> Customer
SupportTicket 3 2 -> Customer
ChatMessage 3 2 -> Customer
BranchAppointment 3 2 -> Customer
ServiceRequest 3 2 -> BankAccount
IncidentReport 3 2 -> BankAccount
RiskScore 3 2 -> Customer
SpendingReport 3 2 -> BankAccount
InterestProjection 3 2 -> BankAccount
BalanceForecast 3 2 -> BankAccount
CustomerSegment 3 2 -> Customer
Branch 3 2 -> Customer
ATM 3 2 -> Branch
TellerCashDrawer 3 2 -> Branch
MaintenanceTask 3 2 -> ATM
CourierShipment 3 2 -> Branch

Exceptions (12):
----------------
UnauthorizedAccessException 0 1 -> -
PaymentRejectedException 0 1 -> -
OverdraftException 0 1 -> -
FraudDetectedException 0 1 -> -
CardExpiredException 0 1 -> -
LimitExceededException 0 1 -> -
KYCFailedException 0 1 -> -
AMLFlaggedException 0 1 -> -
LoanDefaultException 0 1 -> -
InvalidScheduleException 0 1 -> -
CurrencyMismatchException 0 1 -> -
AccountFrozenException 0 1 -> -

Totals:
- Classes: 50
- Fields: 150
- Behaviors: 100
- Associations: 51

Tests: run `./.venv/bin/python -m pytest` from the repo root (coverage configured for exceptions and tests >85%).
Demo: `python -m main` runs a short banking scenario.
