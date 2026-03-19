"""Domain exceptions for the metro system."""


class MetroError(Exception):
    """Base metro domain error."""


class ValidationError(MetroError):
    """Invalid input or invalid state transition."""


class NotFoundError(MetroError):
    """Entity not found."""


class SequenceError(MetroError):
    """Operation was called in a wrong order."""


class CapacityError(MetroError):
    """Train capacity exceeded."""


class SafetyError(MetroError):
    """Safety constraints are violated."""
