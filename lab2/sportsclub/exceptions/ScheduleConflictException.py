class ScheduleConflictException(Exception):
    """Raised when sessions overlap."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
