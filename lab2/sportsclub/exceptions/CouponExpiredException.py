class CouponExpiredException(Exception):
    """Raised when a discount is expired."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
