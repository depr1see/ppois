class SafetyIncidentException(Exception):
    """Raised for safety incidents."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
