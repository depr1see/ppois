class AccessDeniedException(Exception):
    """Raised when access control denies entry."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
