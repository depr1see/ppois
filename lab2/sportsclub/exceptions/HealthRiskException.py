class HealthRiskException(Exception):
    """Raised when health screening fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
