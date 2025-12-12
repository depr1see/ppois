class EquipmentUnavailableException(Exception):
    """Raised when equipment is not available."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
