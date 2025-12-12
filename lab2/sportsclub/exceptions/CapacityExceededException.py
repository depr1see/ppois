class CapacityExceededException(Exception):
    """Raised when capacity limits are exceeded."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
