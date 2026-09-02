class AppException(Exception):
    """Base exception for application-level errors."""

    def __init__(
        self,
        message: str,
        code: str = "APPLICATION_ERROR",
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code

        super().__init__(message)


class ValidationError(AppException):
    """Raised when application input is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
        )


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
        )


class UnauthorizedError(AppException):
    """Raised when authentication is required or invalid."""

    def __init__(self, message: str = "Authentication required.") -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenError(AppException):
    """Raised when access to a resource is not allowed."""

    def __init__(self, message: str = "Access denied.") -> None:
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )