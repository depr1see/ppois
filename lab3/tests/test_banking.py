import pytest

from banking.accounts.AccountBundle import AccountBundle
from banking.accounts.BankAccount import BankAccount
from banking.accounts.SavingsAccount import SavingsAccount
from banking.accounts.CheckingAccount import CheckingAccount
from banking.accounts.BusinessAccount import BusinessAccount
from banking.cards.DebitCard import DebitCard
from banking.cards.CreditCard import CreditCard
from banking.cards.CardControl import CardControl
from banking.cards.CardPIN import CardPIN
from banking.cards.CardReward import CardReward
from banking.customers.Customer import Customer
from banking.customers.CustomerProfile import CustomerProfile
from banking.customers.Address import Address
from banking.customers.EmployerInfo import EmployerInfo
from banking.customers.Beneficiary import Beneficiary
from banking.transactions.Transaction import Transaction
from banking.transactions.TransferOrder import TransferOrder
from banking.transactions.PaymentRequest import PaymentRequest
from banking.transactions.StandingInstruction import StandingInstruction
from banking.transactions.FXExchange import FXExchange
from banking.loans.LoanApplication import LoanApplication
from banking.loans.LoanAgreement import LoanAgreement
from banking.loans.MortgageAccount import MortgageAccount
from banking.loans.CollateralItem import CollateralItem
from banking.loans.RepaymentSchedule import RepaymentSchedule
from banking.security.AuthSession import AuthSession
from banking.security.TwoFactorDevice import TwoFactorDevice
from banking.security.AccessLog import AccessLog
from banking.security.FraudAlert import FraudAlert
from banking.security.SecurityPolicy import SecurityPolicy
from banking.compliance.KYCCheck import KYCCheck
from banking.compliance.AMLReport import AMLReport
from banking.compliance.SanctionsScreening import SanctionsScreening
from banking.compliance.AuditTrail import AuditTrail
from banking.compliance.ConsentRecord import ConsentRecord
from banking.support.SupportTicket import SupportTicket
from banking.support.ChatMessage import ChatMessage
from banking.support.BranchAppointment import BranchAppointment
from banking.support.ServiceRequest import ServiceRequest
from banking.support.IncidentReport import IncidentReport
from banking.analytics.RiskScore import RiskScore
from banking.analytics.SpendingReport import SpendingReport
from banking.analytics.InterestProjection import InterestProjection
from banking.analytics.BalanceForecast import BalanceForecast
from banking.analytics.CustomerSegment import CustomerSegment
from banking.operations.Branch import Branch
from banking.operations.ATM import ATM
from banking.operations.TellerCashDrawer import TellerCashDrawer
from banking.operations.MaintenanceTask import MaintenanceTask
from banking.operations.CourierShipment import CourierShipment
from banking.exceptions import (
    AccountFrozenException,
    AMLFlaggedException,
    CardExpiredException,
    CurrencyMismatchException,
    FraudDetectedException,
    InvalidScheduleException,
    KYCFailedException,
    LimitExceededException,
    LoanDefaultException,
    OverdraftException,
    PaymentRejectedException,
    UnauthorizedAccessException,
)


def to_snake(name: str) -> str:
    out = ""
    for i, ch in enumerate(name):
        if ch.isupper() and i and (name[i - 1].islower() or (i + 1 < len(name) and name[i + 1].islower())):
            out += "_" + ch.lower()
        else:
            out += ch.lower()
    return out


def sample_account(balance: float = 1000.0) -> BankAccount:
    return BankAccount(account_number="SAFE", balance=balance, owner=Customer(customer_id="C", name="Demo"))


CLASS_LIST = [
    BankAccount,
    SavingsAccount,
    CheckingAccount,
    BusinessAccount,
    AccountBundle,
    Customer,
    CustomerProfile,
    Address,
    EmployerInfo,
    Beneficiary,
    DebitCard,
    CreditCard,
    CardControl,
    CardPIN,
    CardReward,
    Transaction,
    TransferOrder,
    PaymentRequest,
    StandingInstruction,
    FXExchange,
    LoanApplication,
    LoanAgreement,
    MortgageAccount,
    CollateralItem,
    RepaymentSchedule,
    AuthSession,
    TwoFactorDevice,
    AccessLog,
    FraudAlert,
    SecurityPolicy,
    KYCCheck,
    AMLReport,
    SanctionsScreening,
    AuditTrail,
    ConsentRecord,
    SupportTicket,
    ChatMessage,
    BranchAppointment,
    ServiceRequest,
    IncidentReport,
    RiskScore,
    SpendingReport,
    InterestProjection,
    BalanceForecast,
    CustomerSegment,
    Branch,
    ATM,
    TellerCashDrawer,
    MaintenanceTask,
    CourierShipment,
]


SAFE_KWARGS = {
    "BankAccount": {"owner": Customer(customer_id="C1", name="Alice"), "balance": 200.0},
    "AccountBundle": {"accounts": [sample_account()], "advisor": Customer(customer_id="C2", name="Bob")},
    "DebitCard": {"account": sample_account()},
    "CreditCard": {"account": sample_account(), "credit_limit": 3000.0},
    "CardControl": {"card": DebitCard(card_number="4000", account=sample_account())},
    "CardPIN": {"card": DebitCard(card_number="4001", account=sample_account())},
    "CardReward": {"card": CreditCard(card_number="5000", account=sample_account())},
    "Transaction": {"amount": 50.0, "source_account": sample_account()},
    "TransferOrder": {"amount": 75.0, "destination_account": sample_account()},
    "PaymentRequest": {"merchant": "Shop", "account": sample_account()},
    "StandingInstruction": {"account": sample_account(), "frequency": "weekly"},
    "FXExchange": {"account": sample_account()},
    "LoanApplication": {"amount": 1000.0, "customer": Customer(customer_id="LC1", name="Lender")},
    "LoanAgreement": {
        "principal": 5000.0,
        "collateral": CollateralItem(collateral_id="COL-1", value=10000.0, owner=Customer(customer_id="X", name="Owner")),
    },
    "MortgageAccount": {"borrower": Customer(customer_id="B1", name="Borrower"), "property_value": 120000.0},
    "RepaymentSchedule": {"due_dates": ["2025-01-01"], "agreement": None},
    "AuthSession": {"user": Customer(customer_id="AUTH", name="User")},
    "FraudAlert": {"account": sample_account(), "severity": "low"},
    "AMLReport": {"account": sample_account(), "flagged": False},
    "SanctionsScreening": {"customer": Customer(customer_id="SEC", name="Name")},
    "KYCCheck": {"customer": Customer(customer_id="KYC", name="Know"), "status": "pending"},
    "IncidentReport": {"details": "network issue", "account": sample_account()},
    "ServiceRequest": {"account": sample_account(), "category": "cards"},
    "SpendingReport": {"account": sample_account(), "total": 10.0},
    "InterestProjection": {"account": sample_account(), "estimated": 1.0},
    "BalanceForecast": {"account": sample_account(), "trajectory": [1.0, 2.0]},
    "CustomerSegment": {"customers": [Customer(customer_id="SEG", name="Segment")], "label": "retail"},
    "Branch": {"manager": Customer(customer_id="MGR", name="Manager")},
    "ATM": {"managed_by": Branch(branch_id="BR", city="City", manager=Customer(customer_id="M", name="Mgr"))},
    "TellerCashDrawer": {"branch": Branch(branch_id="BR2", city="Town", manager=Customer(customer_id="M2", name="Mgr2")), "cash_level": 100.0},
    "MaintenanceTask": {"target_atm": ATM(atm_id="ATM1", location="Lobby", managed_by=None)},
    "CourierShipment": {"destination_branch": Branch(branch_id="BR3", city="Village", manager=Customer(customer_id="M3", name="Mgr3"))},
}


def test_update_and_describe_all_classes():
    note_map = {
        "TransferOrder": "usd/eur",
        "BankAccount": "active",
        "AccountBundle": "rebalance",
        "LoanAgreement": "sign",
        "RepaymentSchedule": "review",
        "LoanApplication": "submit",
        "MortgageAccount": "review",
        "StandingInstruction": "run",
        "PaymentRequest": "pay",
    }
    delta_map = {
        "BankAccount": 10.0,
        "CheckingAccount": 5.0,
        "SavingsAccount": 0.1,
        "DebitCard": 1.0,
        "CreditCard": 1.0,
        "Transaction": 1.0,
        "TransferOrder": 1.0,
        "LoanApplication": 1.0,
        "LoanAgreement": 1.0,
        "CollateralItem": 5.0,
        "RiskScore": 0.5,
        "SpendingReport": 2.0,
        "InterestProjection": 0.5,
        "BalanceForecast": 0.0,
        "TellerCashDrawer": 10.0,
        "FXExchange": 0.01,
    }
    for cls in CLASS_LIST:
        kwargs = SAFE_KWARGS.get(cls.__name__, {})
        instance = cls(**kwargs)
        update_method = getattr(instance, f"update_{to_snake(cls.__name__)}")
        describe_method = getattr(instance, f"describe_{to_snake(cls.__name__)}")
        result = update_method(note_map.get(cls.__name__, ""), delta_map.get(cls.__name__, None))
        assert isinstance(result, str)
        description = describe_method()
        assert cls.__name__ in description


def test_exception_branches():
    with pytest.raises(UnauthorizedAccessException):
        BankAccount().update_bank_account(note="open")

    with pytest.raises(CardExpiredException):
        DebitCard(account=sample_account()).update_debit_card(note="expired")

    with pytest.raises(PaymentRejectedException):
        Transaction(amount=0, source_account=None).update_transaction(note="process")

    with pytest.raises(PaymentRejectedException):
        TransferOrder(amount=-1.0, destination_account=sample_account()).update_transfer_order(delta=-1.0)

    with pytest.raises(CurrencyMismatchException):
        TransferOrder(amount=10.0, destination_account=sample_account()).update_transfer_order(note="BAD")

    with pytest.raises(CurrencyMismatchException):
        FXExchange(pair="USDEUR", account=sample_account()).update_fx_exchange()

    with pytest.raises(InvalidScheduleException):
        RepaymentSchedule(schedule_id="S1", due_dates=[], agreement=None).update_repayment_schedule(note="check")

    with pytest.raises(LoanDefaultException):
        LoanAgreement(principal=0, collateral=None).update_loan_agreement(note="sign")

    with pytest.raises(KYCFailedException):
        KYCCheck(status="failed", customer=Customer(customer_id="K2", name="K")).update_kyc_check()

    with pytest.raises(AMLFlaggedException):
        AMLReport(flagged=True, account=sample_account()).update_aml_report()

    with pytest.raises(FraudDetectedException):
        FraudAlert(severity="high", account=sample_account()).update_fraud_alert()

    with pytest.raises(UnauthorizedAccessException):
        CardPIN(attempts=3, card=DebitCard(account=sample_account())).update_card_pin()

    with pytest.raises(LimitExceededException):
        CreditCard(account=sample_account(), credit_limit=1000.0).update_credit_card(delta=2000.0)

    with pytest.raises(OverdraftException):
        BankAccount(owner=Customer(customer_id="Z", name="Zed"), balance=10.0).update_bank_account(delta=-50.0)
