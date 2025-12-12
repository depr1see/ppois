class OverdueBalanceException(Exception):
    """Raised when outstanding balance is overdue."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
