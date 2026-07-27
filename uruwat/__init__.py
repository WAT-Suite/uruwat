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
    DailyLoss,
    DailyLossMetric,
    DailyLossPoint,
    DailyLossSeries,
    Equipment,
    EquipmentType,
    Status,
    System,
)

__version__ = "0.4.0"

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
    "DailyLoss",
    "DailyLossMetric",
    "DailyLossPoint",
    "DailyLossSeries",
]
