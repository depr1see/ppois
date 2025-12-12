class UnauthorizedCoachException(Exception):
    """Raised when coach permissions are missing."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
