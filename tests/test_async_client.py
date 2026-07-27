"""Unit tests for the AsyncClient class."""

from unittest.mock import AsyncMock, Mock

import pytest

from uruwat import AsyncClient, Country
from uruwat.exceptions import (
    WarTrackAPIError,
    WarTrackAuthenticationError,
)


@pytest.mark.asyncio
@pytest.mark.unit
class TestAsyncClientInitialization:
    """Test async client initialization."""

    async def test_default_initialization(self):
        """Test async client with default parameters."""
        async with AsyncClient() as client:
            assert client.base_url == "http://localhost:8000"
            assert client.timeout == 30.0

    async def test_custom_initialization(self):
        """Test async client with custom parameters."""
        async with AsyncClient(
            base_url="http://custom-api.example.com",
            timeout=60.0,
            headers={"Authorization": "Bearer token"},
        ) as client:
            assert client.base_url == "http://custom-api.example.com"
            assert client.timeout == 60.0
            assert client.headers == {"Authorization": "Bearer token"}

    async def test_base_url_trailing_slash_removed(self):
        """Test that trailing slashes are removed from base_url."""
        async with AsyncClient(base_url="http://example.com/") as client:
            assert client.base_url == "http://example.com"

    async def test_context_manager(self):
        """Test async client as context manager."""
        async with AsyncClient() as client:
            assert isinstance(client, AsyncClient)
            assert client._client is not None
        # Client should be closed after context exit
        assert client._client is None or client._client.is_closed


@pytest.mark.asyncio
@pytest.mark.unit
class TestAsyncClientRequests:
    """Test async client request methods."""

    async def test_get_equipments_success(self, mock_httpx_async_client):
        """Test successful get_equipments call."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "country": "ukraine",
                "type": "Tanks",
                "destroyed": 10,
                "abandoned": 2,
                "captured": 5,
                "damaged": 3,
                "total": 20,
                "date": "2024-01-15",
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_httpx_async_client.request = AsyncMock(return_value=mock_response)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            equipments = await client.get_equipments(country=Country.UKRAINE)

            assert len(equipments) == 1
            assert equipments[0].country == "ukraine"
            assert equipments[0].type == "Tanks"

    async def test_get_total_equipments_success(self, mock_httpx_async_client):
        """Test successful get_total_equipments call."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "country": "ukraine",
                "type": "Tanks",
                "destroyed": 100,
                "abandoned": 20,
                "captured": 50,
                "damaged": 30,
                "total": 200,
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_httpx_async_client.request = AsyncMock(return_value=mock_response)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            totals = await client.get_total_equipments(country=Country.UKRAINE)

            assert len(totals) == 1
            assert totals[0].country == "ukraine"

    async def test_get_systems_success(self, mock_httpx_async_client):
        """Test successful get_systems call."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "country": "ukraine",
                "origin": "Russia",
                "system": "T-72",
                "status": "destroyed",
                "url": "https://example.com",
                "date": "2024-01-15",
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_httpx_async_client.request = AsyncMock(return_value=mock_response)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            systems = await client.get_systems(country=Country.UKRAINE)

            assert len(systems) == 1
            assert systems[0].country == "ukraine"

    async def test_health_check_success(self, mock_httpx_async_client):
        """Test successful health_check call."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status = Mock()
        mock_httpx_async_client.request = AsyncMock(return_value=mock_response)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            health = await client.health_check()

            assert health["status"] == "healthy"

    async def test_request_error_handling(self, mock_httpx_async_client):
        """Test error handling for request failures."""
        import httpx

        mock_httpx_async_client.request = AsyncMock(side_effect=httpx.RequestError("Network error"))

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            with pytest.raises(WarTrackAPIError):
                await client.health_check()

    async def test_http_status_error_handling(self, mock_httpx_async_client):
        """Test error handling for HTTP status errors."""
        import httpx

        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Unauthorized"}
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=mock_response)
        mock_httpx_async_client.request = AsyncMock(side_effect=error)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            with pytest.raises(WarTrackAuthenticationError):
                await client.health_check()


@pytest.mark.asyncio
@pytest.mark.unit
class TestAsyncClientImports:
    """Test the import-trigger methods, which had no async coverage."""

    @pytest.mark.parametrize(
        ("method", "endpoint"),
        [
            ("import_equipments", "/api/import/equipments"),
            ("import_all_equipments", "/api/import/all-equipments"),
            ("import_systems", "/api/import/systems"),
            ("import_all_systems", "/api/import/all-systems"),
            ("import_all", "/api/import/all"),
            ("import_historical", "/api/import/historical"),
        ],
    )
    async def test_import_posts_to_expected_endpoint(
        self, mock_httpx_async_client, method, endpoint
    ):
        """Each import method POSTs to its own endpoint and returns the message."""
        mock_response = Mock()
        mock_response.json.return_value = {"message": "imported successfully"}
        mock_response.raise_for_status = Mock()
        mock_httpx_async_client.request = AsyncMock(return_value=mock_response)

        async with AsyncClient() as client:
            client._client = mock_httpx_async_client
            result = await getattr(client, method)()

        assert result["message"] == "imported successfully"
        assert mock_httpx_async_client.request.await_args.kwargs["method"] == "POST"
        assert mock_httpx_async_client.request.await_args.kwargs["url"] == endpoint
