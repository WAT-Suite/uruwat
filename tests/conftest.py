"""Pytest configuration and fixtures."""

import pytest
import respx

from watpy import Client


@pytest.fixture
def client():
    """Create a test client instance."""
    return Client(base_url="http://test-api.example.com")


@pytest.fixture
def mock_api():
    """Create a mock API router for testing."""
    with respx.mock(base_url="http://test-api.example.com") as respx_mock:
        yield respx_mock


@pytest.fixture
def sample_equipment_data():
    """Sample equipment data for testing."""
    return [
        {
            "id": 1,
            "country": "ukraine",
            "type": "Tanks",
            "destroyed": 10,
            "abandoned": 2,
            "captured": 5,
            "damaged": 3,
            "total": 20,
            "date": "2024-01-01",
        }
    ]


@pytest.fixture
def sample_all_equipment_data():
    """Sample all equipment data for testing."""
    return [
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


@pytest.fixture
def sample_system_data():
    """Sample system data for testing."""
    return [
        {
            "id": 1,
            "country": "ukraine",
            "origin": "Russia",
            "system": "T-72",
            "status": "destroyed",
            "url": "https://example.com",
            "date": "2024-01-01",
        }
    ]


@pytest.fixture
def sample_all_system_data():
    """Sample all system data for testing."""
    return [
        {
            "id": 1,
            "country": "ukraine",
            "system": "T-72",
            "destroyed": 50,
            "abandoned": 10,
            "captured": 25,
            "damaged": 15,
            "total": 100,
        }
    ]
