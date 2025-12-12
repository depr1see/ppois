from banking.accounts.BankAccount import BankAccount
from banking.accounts.AccountBundle import AccountBundle
from banking.cards.DebitCard import DebitCard
from banking.cards.CreditCard import CreditCard
from banking.customers.Customer import Customer
from banking.customers.CustomerProfile import CustomerProfile
from banking.transactions.TransferOrder import TransferOrder
from banking.transactions.Transaction import Transaction
from banking.transactions.PaymentRequest import PaymentRequest
from banking.transactions.FXExchange import FXExchange
from banking.security.AuthSession import AuthSession
from banking.compliance.KYCCheck import KYCCheck
from banking.security.FraudAlert import FraudAlert
from banking.exceptions import (
    UnauthorizedAccessException,
    PaymentRejectedException,
    OverdraftException,
    CurrencyMismatchException,
    AccountFrozenException,
    FraudDetectedException,
)


def run_demo() -> None:
    """Small end-to-end walkthrough of the banking domain."""
    customer = Customer(customer_id="C001", name="Alice Doe")
    profile = CustomerProfile(profile_id="P001", risk_level="low", customer=customer)

    account = BankAccount(account_number="ACC-001", balance=1500.0, owner=customer)
    bundle = AccountBundle(bundle_id="BUNDLE-01", accounts=[account], advisor=customer)
    debit_card = DebitCard(card_number="4000123412341234", account=account)
    credit_card = CreditCard(card_number="5444333322221111", credit_limit=8000.0, account=account)

    print("Customer profile:", profile.describe_customer_profile())
    print("Opening balance:", account.describe_bank_account())
    account.update_bank_account(delta=500.0)
    debit_card.update_debit_card(delta=200.0)
    print("Post-deposit balance:", account.describe_bank_account())

    payment = PaymentRequest(request_id="PAY-1", merchant="Bookstore", account=account)
    payment.update_payment_request(note="approve")
    transfer = TransferOrder(order_id="TR-1", amount=250.0, destination_account=account)
    transfer.update_transfer_order(delta=transfer.amount)

    fx = FXExchange(pair="USD/EUR", rate=0.9, account=account)
    fx.update_fx_exchange(note="hedge", delta=0.1)

    session = AuthSession(session_id="S001", user=customer, active=True)
    session.update_auth_session(note="validate")
    compliance = KYCCheck(check_id="KYC-1", customer=customer)
    compliance.update_kyc_check(note="pass")

    alert = FraudAlert(alert_id="F-1", severity="low", account=account)
    alert.update_fraud_alert(note="monitor")

    bundle.update_account_bundle(note="rebalance")
    print("Bundle view:", bundle.describe_account_bundle())
    print("Debit card:", debit_card.describe_debit_card())
    print("Credit card:", credit_card.describe_credit_card())
    print("Transfer:", transfer.describe_transfer_order())
    print("FX rate:", fx.describe_fx_exchange())
    print("Session:", session.describe_auth_session())
    print("Compliance:", compliance.describe_kyc_check())
    print("Fraud monitoring:", alert.describe_fraud_alert())


def run_error_showcase() -> None:
    """Show a few guarded behaviors with exception handling."""
    temp_account = BankAccount(account_number="ACC-ERR", balance=10.0, owner=Customer(customer_id="ERR", name="Temp"))
    try:
        temp_account.update_bank_account(note="frozen")
    except AccountFrozenException as exc:
        print("Freeze guard:", exc)
    except UnauthorizedAccessException as exc:
        print("Ownership guard:", exc)

    try:
        temp_account.update_bank_account(delta=-50.0)
    except OverdraftException as exc:
        print("Overdraft guard:", exc)

    temp_transfer = TransferOrder(order_id="BAD", amount=-10.0, destination_account=temp_account)
    try:
        temp_transfer.update_transfer_order(delta=temp_transfer.amount)
    except PaymentRejectedException as exc:
        print("Transfer validation:", exc)

    fx = FXExchange(pair="USDEUR", account=temp_account)
    try:
        fx.update_fx_exchange(note="bad-pair")
    except CurrencyMismatchException as exc:
        print("FX guard:", exc)

    fraud = FraudAlert(alert_id="F-HIGH", severity="high", account=temp_account)
    try:
        fraud.update_fraud_alert()
    except FraudDetectedException as exc:
        print("Fraud escalation:", exc)


if __name__ == "__main__":
    try:
        run_demo()
    except (UnauthorizedAccessException, PaymentRejectedException) as demo_error:
        print("Demo interrupted:", demo_error)
    run_error_showcase()
