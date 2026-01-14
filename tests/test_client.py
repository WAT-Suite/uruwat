"""Unit tests for the Client class."""

import pytest
from httpx import Response

from uruwat import Client, Country, EquipmentType, Status
from uruwat.exceptions import (
    WarTrackAPIError,
    WarTrackAuthenticationError,
    WarTrackForbiddenError,
    WarTrackNotFoundError,
    WarTrackRateLimitError,
    WarTrackServerError,
)


@pytest.mark.unit
class TestClientInitialization:
    """Test client initialization."""

    def test_default_initialization(self):
        """Test client with default parameters."""
        client = Client()
        assert client.base_url == "http://localhost:8000"
        assert client.timeout == 30.0

    def test_custom_initialization(self):
        """Test client with custom parameters."""
        client = Client(
            base_url="http://custom-api.example.com",
            timeout=60.0,
            headers={"Authorization": "Bearer token"},
        )
        assert client.base_url == "http://custom-api.example.com"
        assert client.timeout == 60.0
        assert client.headers == {"Authorization": "Bearer token"}

    def test_base_url_trailing_slash_removed(self):
        """Test that trailing slashes are removed from base_url."""
        client = Client(base_url="http://example.com/")
        assert client.base_url == "http://example.com"

    def test_context_manager(self):
        """Test client as context manager."""
        with Client() as client:
            assert isinstance(client, Client)
        # Client should be closed after context exit
        assert client._client.is_closed


@pytest.mark.unit
class TestClientEquipments:
    """Test equipment-related methods."""

    def test_get_equipments_success(self, mock_api, sample_equipment_data):
        """Test successful equipment retrieval."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(200, json=sample_equipment_data)
        )

        client = Client(base_url="http://test-api.example.com")
        equipments = client.get_equipments(country=Country.UKRAINE)

        assert len(equipments) == 1
        assert equipments[0].country == "ukraine"
        assert equipments[0].type == "Tanks"
        assert equipments[0].total == 20

    def test_get_equipments_with_filters(self, mock_api, sample_equipment_data):
        """Test equipment retrieval with filters."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(200, json=sample_equipment_data)
        )

        client = Client(base_url="http://test-api.example.com")
        equipments = client.get_equipments(
            country=Country.UKRAINE,
            types=[EquipmentType.TANKS],
            date_start="2024-01-01",
            date_end="2024-12-31",
        )

        assert len(equipments) == 1
        # Verify request was made with correct body
        request = mock_api.calls[0].request
        assert request.method == "POST"
        assert "types" in request.read().decode()

    def test_get_equipments_invalid_country(self):
        """Test equipment retrieval with invalid country."""
        client = Client()
        with pytest.raises(ValueError, match="Country must be UKRAINE or RUSSIA"):
            client.get_equipments(country=Country.ALL)

    def test_get_total_equipments_success(self, mock_api, sample_all_equipment_data):
        """Test successful total equipment retrieval."""
        mock_api.post("/api/stats/equipments").mock(
            return_value=Response(200, json=sample_all_equipment_data)
        )

        client = Client(base_url="http://test-api.example.com")
        totals = client.get_total_equipments(country=Country.UKRAINE)

        assert len(totals) == 1
        assert totals[0].country == "ukraine"
        assert totals[0].total == 200

    def test_get_equipment_types_success(self, mock_api):
        """Test successful equipment types retrieval."""
        mock_api.get("/api/stats/equipment-types").mock(
            return_value=Response(200, json=[{"type": "Tanks"}, {"type": "Aircraft"}])
        )

        client = Client(base_url="http://test-api.example.com")
        types = client.get_equipment_types()

        assert len(types) == 2
        assert types[0]["type"] == "Tanks"


@pytest.mark.unit
class TestClientSystems:
    """Test system-related methods."""

    def test_get_systems_success(self, mock_api, sample_system_data):
        """Test successful system retrieval."""
        mock_api.post("/api/stats/systems/ukraine").mock(
            return_value=Response(200, json=sample_system_data)
        )

        client = Client(base_url="http://test-api.example.com")
        systems = client.get_systems(country=Country.UKRAINE)

        assert len(systems) == 1
        assert systems[0].country == "ukraine"
        assert systems[0].system == "T-72"
        assert systems[0].status == "destroyed"

    def test_get_systems_with_filters(self, mock_api, sample_system_data):
        """Test system retrieval with filters."""
        mock_api.post("/api/stats/systems/ukraine").mock(
            return_value=Response(200, json=sample_system_data)
        )

        client = Client(base_url="http://test-api.example.com")
        systems = client.get_systems(
            country=Country.UKRAINE,
            status=[Status.DESTROYED],
            date_start="2024-01-01",
            date_end="2024-12-31",
        )

        assert len(systems) == 1

    def test_get_systems_invalid_country(self):
        """Test system retrieval with invalid country."""
        client = Client()
        with pytest.raises(ValueError, match="Country must be UKRAINE or RUSSIA"):
            client.get_systems(country=Country.ALL)

    def test_get_total_systems_success(self, mock_api, sample_all_system_data):
        """Test successful total system retrieval."""
        mock_api.post("/api/stats/systems").mock(
            return_value=Response(200, json=sample_all_system_data)
        )

        client = Client(base_url="http://test-api.example.com")
        totals = client.get_total_systems(country=Country.UKRAINE)

        assert len(totals) == 1
        assert totals[0].country == "ukraine"
        assert totals[0].total == 100

    def test_get_system_types_success(self, mock_api):
        """Test successful system types retrieval."""
        mock_api.get("/api/stats/system-types").mock(
            return_value=Response(200, json=[{"system": "T-72"}, {"system": "T-90"}])
        )

        client = Client(base_url="http://test-api.example.com")
        types = client.get_system_types()

        assert len(types) == 2
        assert types[0]["system"] == "T-72"


@pytest.mark.unit
class TestClientImport:
    """Test import-related methods."""

    def test_import_equipments(self, mock_api):
        """Test equipment import."""
        mock_api.post("/api/import/equipments").mock(
            return_value=Response(200, json={"message": "Equipment data imported successfully"})
        )

        client = Client(base_url="http://test-api.example.com")
        result = client.import_equipments()

        assert result["message"] == "Equipment data imported successfully"

    def test_import_all_equipments(self, mock_api):
        """Test all equipment import."""
        mock_api.post("/api/import/all-equipments").mock(
            return_value=Response(200, json={"message": "All equipment data imported successfully"})
        )

        client = Client(base_url="http://test-api.example.com")
        result = client.import_all_equipments()

        assert result["message"] == "All equipment data imported successfully"

    def test_import_systems(self, mock_api):
        """Test system import."""
        mock_api.post("/api/import/systems").mock(
            return_value=Response(200, json={"message": "System data imported successfully"})
        )

        client = Client(base_url="http://test-api.example.com")
        result = client.import_systems()

        assert result["message"] == "System data imported successfully"

    def test_import_all_systems(self, mock_api):
        """Test all system import."""
        mock_api.post("/api/import/all-systems").mock(
            return_value=Response(200, json={"message": "All system data imported successfully"})
        )

        client = Client(base_url="http://test-api.example.com")
        result = client.import_all_systems()

        assert result["message"] == "All system data imported successfully"

    def test_import_all(self, mock_api):
        """Test import all data."""
        mock_api.post("/api/import/all").mock(
            return_value=Response(200, json={"message": "All data imported successfully"})
        )

        client = Client(base_url="http://test-api.example.com")
        result = client.import_all()

        assert result["message"] == "All data imported successfully"


@pytest.mark.unit
class TestClientHealth:
    """Test health check method."""

    def test_health_check(self, mock_api):
        """Test health check."""
        mock_api.get("/health").mock(return_value=Response(200, json={"status": "healthy"}))

        client = Client(base_url="http://test-api.example.com")
        result = client.health_check()

        assert result["status"] == "healthy"


@pytest.mark.unit
class TestClientErrorHandling:
    """Test error handling."""

    def test_authentication_error(self, mock_api):
        """Test authentication error handling."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(401, json={"detail": "Unauthorized"})
        )

        client = Client(base_url="http://test-api.example.com")
        with pytest.raises(WarTrackAuthenticationError) as exc_info:
            client.get_equipments(country=Country.UKRAINE)

        assert exc_info.value.status_code == 401

    def test_forbidden_error(self, mock_api):
        """Test forbidden error handling."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(403, json={"detail": "Forbidden"})
        )

        client = Client(base_url="http://test-api.example.com")
        with pytest.raises(WarTrackForbiddenError) as exc_info:
            client.get_equipments(country=Country.UKRAINE)

        assert exc_info.value.status_code == 403

    def test_not_found_error(self, mock_api):
        """Test not found error handling."""
        mock_api.get("/health").mock(return_value=Response(404, json={"detail": "Not Found"}))

        client = Client(base_url="http://test-api.example.com")
        with pytest.raises(WarTrackNotFoundError) as exc_info:
            client.health_check()

        assert exc_info.value.status_code == 404

    def test_rate_limit_error(self, mock_api):
        """Test rate limit error handling."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(429, json={"detail": "Rate limit exceeded"})
        )

        client = Client(base_url="http://test-api.example.com")
        with pytest.raises(WarTrackRateLimitError) as exc_info:
            client.get_equipments(country=Country.UKRAINE)

        assert exc_info.value.status_code == 429

    def test_server_error(self, mock_api):
        """Test server error handling."""
        mock_api.post("/api/stats/equipments/ukraine").mock(
            return_value=Response(500, json={"detail": "Internal Server Error"})
        )

        client = Client(base_url="http://test-api.example.com")
        with pytest.raises(WarTrackServerError) as exc_info:
            client.get_equipments(country=Country.UKRAINE)

        assert exc_info.value.status_code == 500

    def test_request_error(self):
        """Test request error handling."""
        # Use a non-existent URL to trigger a RequestError
        client = Client(base_url="http://nonexistent-domain-12345.example.com", timeout=1.0)
        with pytest.raises(WarTrackAPIError) as exc_info:
            client.get_equipments(country=Country.UKRAINE)

        assert "Request failed" in str(exc_info.value)
