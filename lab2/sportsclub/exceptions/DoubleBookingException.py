class DoubleBookingException(Exception):
    """Raised when a member books the same slot twice."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
