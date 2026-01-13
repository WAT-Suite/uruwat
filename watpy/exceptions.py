"""
Custom exceptions for the War Track Dashboard API client.
"""


class WarTrackAPIError(Exception):
    """Base exception for all API errors."""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        """Initialize the exception."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response


class WarTrackAuthenticationError(WarTrackAPIError):
    """Raised when authentication fails (401 Unauthorized)."""

    pass


class WarTrackForbiddenError(WarTrackAPIError):
    """Raised when access is forbidden (403 Forbidden)."""

    pass


class WarTrackNotFoundError(WarTrackAPIError):
    """Raised when a resource is not found (404 Not Found)."""

    pass


class WarTrackRateLimitError(WarTrackAPIError):
    """Raised when rate limit is exceeded (429 Too Many Requests)."""

    pass


class WarTrackServerError(WarTrackAPIError):
    """Raised when server error occurs (500+)."""

    pass
