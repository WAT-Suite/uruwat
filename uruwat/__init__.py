"""
Python client wrapper for the War Track Dashboard API.
"""

from uruwat.async_client import AsyncClient
from uruwat.client import Client
from uruwat.exceptions import (
    WarTrackAPIError,
    WarTrackAuthenticationError,
    WarTrackForbiddenError,
    WarTrackNotFoundError,
    WarTrackRateLimitError,
    WarTrackServerError,
)
from uruwat.models import (
    AllEquipment,
    AllSystem,
    Country,
    Equipment,
    EquipmentType,
    Status,
    System,
)

__version__ = "0.2.0"

__all__ = [
    "Client",
    "AsyncClient",
    "WarTrackAPIError",
    "WarTrackAuthenticationError",
    "WarTrackForbiddenError",
    "WarTrackNotFoundError",
    "WarTrackRateLimitError",
    "WarTrackServerError",
    "Country",
    "EquipmentType",
    "Status",
    "Equipment",
    "AllEquipment",
    "System",
    "AllSystem",
]
