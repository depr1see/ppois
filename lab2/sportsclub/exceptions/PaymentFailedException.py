class PaymentFailedException(Exception):
    """Raised when a payment cannot be processed."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
