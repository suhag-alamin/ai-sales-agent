class AppError(Exception):
    """Base class for all application-specific exceptions."""
    pass


class NotFoundError(AppError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource: str, key: str) -> None:
        super().__init__(f"'{resource}' not found with key '{key}'.")


class ConflictError(AppError):
    """Exception raised when there is a conflict, such as a duplicate entry."""

    def __init__(self, resource: str, key: str) -> None:
        super().__init__(
            f"Conflict: '{resource}' already exists with key '{key}'.")
