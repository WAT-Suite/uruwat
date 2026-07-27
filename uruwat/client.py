"""
Main client class for the War Track Dashboard API.
"""

from datetime import date
from typing import Any, cast

import httpx

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
    DailyLossSeries,
    Equipment,
    EquipmentType,
    Status,
    System,
)


def _as_date_string(value: date | str | None) -> str:
    """Render a date bound for the API's two-element date range."""
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d") if isinstance(value, date) else value


class Client:
    """
    Client for interacting with the War Track Dashboard API.

    Example:
        ```python
        from uruwat import Client

        client = Client(base_url="http://localhost:8000")
        equipments = client.get_equipments(country=Country.UKRAINE)
        ```
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
        headers: dict[str, str] | None = None,
    ):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the API (default: http://localhost:8000)
            timeout: Request timeout in seconds (default: 30.0)
            headers: Additional headers to include in requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON body for POST requests

        Returns:
            Response data as dictionary or list

        Raises:
            WarTrackAPIError: Base exception for API errors
            WarTrackAuthenticationError: Authentication failed
            WarTrackForbiddenError: Access forbidden
            WarTrackNotFoundError: Resource not found
            WarTrackRateLimitError: Rate limit exceeded
            WarTrackServerError: Server error
        """
        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json,
            )
            response.raise_for_status()
            # response.json() returns Any, but we know it's either dict or list
            return cast(dict[str, Any] | list[Any], response.json())
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
                error_message = error_data.get("detail", str(e))
            except Exception:
                error_message = str(e)

            if status_code == 401:
                raise WarTrackAuthenticationError(
                    f"Authentication failed: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
            elif status_code == 403:
                raise WarTrackForbiddenError(
                    f"Access forbidden: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
            elif status_code == 404:
                raise WarTrackNotFoundError(
                    f"Resource not found: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
            elif status_code == 429:
                raise WarTrackRateLimitError(
                    f"Rate limit exceeded: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
            elif status_code >= 500:
                raise WarTrackServerError(
                    f"Server error: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
            else:
                raise WarTrackAPIError(
                    f"API error: {error_message}",
                    status_code=status_code,
                    response=error_data if "error_data" in locals() else None,
                )
        except httpx.RequestError as e:
            raise WarTrackAPIError(f"Request failed: {str(e)}")

    def get_equipments(
        self,
        country: Country,
        types: list[EquipmentType] | None = None,
        date_start: date | str | None = None,
        date_end: date | str | None = None,
    ) -> list[Equipment]:
        """
        Get equipment data filtered by country, types, and date range.

        Args:
            country: Country filter (UKRAINE or RUSSIA)
            types: Optional list of equipment types to filter
            date_start: Optional start date (YYYY-MM-DD format or date object)
            date_end: Optional end date (YYYY-MM-DD format or date object)

        Returns:
            List of Equipment objects

        Example:
            ```python
            from uruwat import Client, Country, EquipmentType

            client = Client()
            equipments = client.get_equipments(
                country=Country.UKRAINE,
                types=[EquipmentType.TANKS, EquipmentType.AIRCRAFT],
                date_start="2024-01-01",
                date_end="2024-12-31",
            )
            ```
        """
        if country not in [Country.UKRAINE, Country.RUSSIA]:
            raise ValueError("Country must be UKRAINE or RUSSIA")

        request_body: dict[str, Any] = {}
        if types:
            request_body["types"] = [t.value for t in types]
        if date_start or date_end:
            date_range = []
            if date_start:
                date_range.append(
                    date_start.strftime("%Y-%m-%d") if isinstance(date_start, date) else date_start
                )
            else:
                date_range.append("")
            if date_end:
                date_range.append(
                    date_end.strftime("%Y-%m-%d") if isinstance(date_end, date) else date_end
                )
            else:
                date_range.append("")
            request_body["date"] = date_range

        json_body = request_body if request_body else None
        data = self._request("POST", f"/api/stats/equipments/{country.value}", json=json_body)
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [Equipment(**item) for item in data if isinstance(item, dict)]

    def get_total_equipments(
        self,
        country: Country | None = None,
        types: list[EquipmentType] | None = None,
    ) -> list[AllEquipment]:
        """
        Get total equipment data with optional filters.

        Args:
            country: Optional country filter
            types: Optional list of equipment types to filter

        Returns:
            List of AllEquipment objects

        Example:
            ```python
            from uruwat import Client, Country, EquipmentType

            client = Client()
            totals = client.get_total_equipments(
                country=Country.UKRAINE,
                types=[EquipmentType.TANKS],
            )
            ```
        """
        request_body: dict[str, Any] = {}
        if country:
            request_body["country"] = country.value
        if types:
            request_body["types"] = [t.value for t in types]

        json_body = request_body if request_body else None
        data = self._request("POST", "/api/stats/equipments", json=json_body)
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [AllEquipment(**item) for item in data if isinstance(item, dict)]

    def get_equipment_types(self) -> list[dict[str, str]]:
        """
        Get distinct equipment types.

        Returns:
            List of dictionaries containing equipment type information

        Example:
            ```python
            from uruwat import Client

            client = Client()
            types = client.get_equipment_types()
            ```
        """
        data = self._request("GET", "/api/stats/equipment-types")
        return data if isinstance(data, list) else []

    def get_systems(
        self,
        country: Country,
        systems: list[str] | None = None,
        status: list[Status] | None = None,
        date_start: date | str | None = None,
        date_end: date | str | None = None,
    ) -> list[System]:
        """
        Get system data filtered by country, systems, status, and date range.

        Args:
            country: Country filter (UKRAINE or RUSSIA)
            systems: Optional list of system names to filter
            status: Optional list of statuses to filter
            date_start: Optional start date (YYYY-MM-DD format or date object)
            date_end: Optional end date (YYYY-MM-DD format or date object)

        Returns:
            List of System objects

        Example:
            ```python
            from uruwat import Client, Country, Status

            client = Client()
            systems = client.get_systems(
                country=Country.UKRAINE,
                status=[Status.DESTROYED, Status.CAPTURED],
                date_start="2024-01-01",
                date_end="2024-12-31",
            )
            ```
        """
        if country not in [Country.UKRAINE, Country.RUSSIA]:
            raise ValueError("Country must be UKRAINE or RUSSIA")

        request_body: dict[str, Any] = {}
        if systems:
            request_body["systems"] = systems
        if status:
            request_body["status"] = [s.value for s in status]
        if date_start or date_end:
            date_range = []
            if date_start:
                date_range.append(
                    date_start.strftime("%Y-%m-%d") if isinstance(date_start, date) else date_start
                )
            else:
                date_range.append("")
            if date_end:
                date_range.append(
                    date_end.strftime("%Y-%m-%d") if isinstance(date_end, date) else date_end
                )
            else:
                date_range.append("")
            request_body["date"] = date_range

        json_body = request_body if request_body else None
        data = self._request("POST", f"/api/stats/systems/{country.value}", json=json_body)
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [System(**item) for item in data if isinstance(item, dict)]

    def get_total_systems(
        self,
        country: Country | None = None,
        systems: list[str] | None = None,
    ) -> list[AllSystem]:
        """
        Get total system data with optional filters.

        Args:
            country: Optional country filter
            systems: Optional list of system names to filter

        Returns:
            List of AllSystem objects

        Example:
            ```python
            from uruwat import Client, Country

            client = Client()
            totals = client.get_total_systems(
                country=Country.UKRAINE,
                systems=["T-72"],
            )
            ```
        """
        request_body: dict[str, Any] = {}
        if country:
            request_body["country"] = country.value
        if systems:
            request_body["systems"] = systems

        json_body = request_body if request_body else None
        data = self._request("POST", "/api/stats/systems", json=json_body)
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [AllSystem(**item) for item in data if isinstance(item, dict)]

    def get_system_types(self) -> list[dict[str, str]]:
        """
        Get distinct system types.

        Returns:
            List of dictionaries containing system type information

        Example:
            ```python
            from uruwat import Client

            client = Client()
            types = client.get_system_types()
            ```
        """
        data = self._request("GET", "/api/stats/system-types")
        return data if isinstance(data, list) else []

    def import_equipments(self) -> dict[str, str]:
        """
        Trigger import of equipment data from scraper.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_equipments()
            ```
        """
        data = self._request("POST", "/api/import/equipments")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def import_all_equipments(self) -> dict[str, str]:
        """
        Trigger import of all equipment totals from scraper.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_all_equipments()
            ```
        """
        data = self._request("POST", "/api/import/all-equipments")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def import_systems(self) -> dict[str, str]:
        """
        Trigger import of system data from scraper.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_systems()
            ```
        """
        data = self._request("POST", "/api/import/systems")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def import_all_systems(self) -> dict[str, str]:
        """
        Trigger import of all system totals from scraper.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_all_systems()
            ```
        """
        data = self._request("POST", "/api/import/all-systems")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def import_all(self) -> dict[str, str]:
        """
        Trigger import of all data from scraper.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_all()
            ```
        """
        data = self._request("POST", "/api/import/all")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def import_historical(self) -> dict[str, str]:
        """
        Trigger a full re-import, ignoring dates already in the database.

        Unlike :meth:`import_all`, which only picks up dates the API does not
        yet have, this re-imports everything the scraper returns.

        Returns:
            Response message

        Example:
            ```python
            from uruwat import Client

            client = Client()
            result = client.import_historical()
            ```
        """
        data = self._request("POST", "/api/import/historical")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def _daily_loss_body(
        self,
        metrics: list[DailyLossMetric] | None = None,
        date_start: date | str | None = None,
        date_end: date | str | None = None,
    ) -> dict[str, Any]:
        """Build the request body shared by the daily loss endpoints."""
        body: dict[str, Any] = {}
        if metrics:
            body["metrics"] = [m.value for m in metrics]
        if date_start or date_end:
            body["date"] = [_as_date_string(date_start), _as_date_string(date_end)]
        return body

    def get_daily_losses(
        self,
        country: Country = Country.ALL,
        metrics: list[DailyLossMetric] | None = None,
        date_start: date | str | None = None,
        date_end: date | str | None = None,
    ) -> list[DailyLoss]:
        """
        Get raw rows of the daily historical loss series.

        This series runs back to 2022-02-24. The equipment and system endpoints
        are Oryx-derived and only accumulate dates going forward, so this is the
        one to chart history against.

        Args:
            country: Country filter; ``Country.ALL`` (default) returns every side
            metrics: Optional list of metrics to filter
            date_start: Optional start date (YYYY-MM-DD format or date object)
            date_end: Optional end date (YYYY-MM-DD format or date object)

        Returns:
            List of DailyLoss objects

        Example:
            ```python
            from uruwat import Client, Country, DailyLossMetric

            client = Client()
            rows = client.get_daily_losses(
                country=Country.RUSSIA,
                metrics=[DailyLossMetric.TANKS],
                date_start="2022-02-24",
            )
            ```
        """
        body = self._daily_loss_body(metrics, date_start, date_end)
        data = self._request("POST", f"/api/stats/daily-losses/{country.value}", json=body or None)
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [DailyLoss(**item) for item in data]

    def get_daily_loss_series(
        self,
        country: Country = Country.ALL,
        metrics: list[DailyLossMetric] | None = None,
        date_start: date | str | None = None,
        date_end: date | str | None = None,
    ) -> list[DailyLossSeries]:
        """
        Get the daily series already grouped into one entry per country/metric.

        The same data as :meth:`get_daily_losses`, shaped so it can be plotted
        without regrouping.

        Args:
            country: Country filter; ``Country.ALL`` (default) returns every side
            metrics: Optional list of metrics to filter
            date_start: Optional start date (YYYY-MM-DD format or date object)
            date_end: Optional end date (YYYY-MM-DD format or date object)

        Returns:
            List of DailyLossSeries objects, each with date-ordered points

        Example:
            ```python
            from uruwat import Client, Country, DailyLossMetric

            client = Client()
            for series in client.get_daily_loss_series(
                country=Country.RUSSIA, metrics=[DailyLossMetric.TANKS]
            ):
                print(series.metric, len(series.points))
            ```
        """
        body = self._daily_loss_body(metrics, date_start, date_end)
        data = self._request(
            "POST", f"/api/stats/daily-losses/{country.value}/series", json=body or None
        )
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return [DailyLossSeries(**item) for item in data]

    def get_daily_loss_metrics(self) -> list[dict[str, str]]:
        """
        Get the metrics present in the daily series.

        Returns:
            List of dictionaries with a ``metric`` key
        """
        data = self._request("GET", "/api/stats/daily-loss-metrics")
        if not isinstance(data, list):
            raise WarTrackAPIError(f"Expected list, got {type(data).__name__}")
        return data

    def import_daily_losses(self) -> dict[str, str]:
        """
        Trigger import of the daily series from the Google Sheet.

        Only imports dates the API does not already have; use
        :meth:`import_historical` to re-import everything.

        Returns:
            Response message
        """
        data = self._request("POST", "/api/import/daily-losses")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data

    def health_check(self) -> dict[str, str]:
        """
        Check API health status.

        Returns:
            Health status response

        Example:
            ```python
            from uruwat import Client

            client = Client()
            health = client.health_check()
            ```
        """
        data = self._request("GET", "/health")
        if not isinstance(data, dict):
            raise WarTrackAPIError(f"Expected dict, got {type(data).__name__}")
        return data
