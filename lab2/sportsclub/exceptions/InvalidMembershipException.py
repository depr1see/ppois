class InvalidMembershipException(Exception):
    """Raised when membership is inactive or invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
