# watpy

Python client wrapper for the War Track Dashboard API.

## Installation

```bash
pip install watpy
```

Or using `uv`:

```bash
uv add watpy
```

## Quick Start

```python
from watpy import Client, Country, EquipmentType

# Initialize the client
client = Client(base_url="http://localhost:8000")

# Get equipment data for Ukraine
equipments = client.get_equipments(country=Country.UKRAINE)

# Get equipment with filters
equipments = client.get_equipments(
    country=Country.UKRAINE,
    types=[EquipmentType.TANKS, EquipmentType.AIRCRAFT],
    date_start="2024-01-01",
    date_end="2024-12-31",
)

# Get total equipment data
totals = client.get_total_equipments(country=Country.UKRAINE)

# Get system data
from watpy import Status

systems = client.get_systems(
    country=Country.UKRAINE,
    status=[Status.DESTROYED, Status.CAPTURED],
)

# Health check
health = client.health_check()
```

## API Reference

### Client

The main client class for interacting with the API.

```python
from watpy import Client

client = Client(
    base_url="http://localhost:8000",  # Optional, defaults to http://localhost:8000
    timeout=30.0,  # Optional, defaults to 30.0 seconds
    headers={"Authorization": "Bearer token"},  # Optional custom headers
)
```

#### Methods

##### `get_equipments()`

Get equipment data filtered by country, types, and date range.

**Parameters:**
- `country` (Country): Country filter (UKRAINE or RUSSIA)
- `types` (list[EquipmentType], optional): List of equipment types to filter
- `date_start` (date | str, optional): Start date (YYYY-MM-DD format or date object)
- `date_end` (date | str, optional): End date (YYYY-MM-DD format or date object)

**Returns:** `list[Equipment]`

**Example:**
```python
equipments = client.get_equipments(
    country=Country.UKRAINE,
    types=[EquipmentType.TANKS],
    date_start="2024-01-01",
    date_end="2024-12-31",
)
```

##### `get_total_equipments()`

Get total equipment data with optional filters.

**Parameters:**
- `country` (Country, optional): Country filter
- `types` (list[EquipmentType], optional): List of equipment types to filter

**Returns:** `list[AllEquipment]`

**Example:**
```python
totals = client.get_total_equipments(
    country=Country.UKRAINE,
    types=[EquipmentType.TANKS],
)
```

##### `get_equipment_types()`

Get distinct equipment types.

**Returns:** `list[dict[str, str]]`

**Example:**
```python
types = client.get_equipment_types()
```

##### `get_systems()`

Get system data filtered by country, systems, status, and date range.

**Parameters:**
- `country` (Country): Country filter (UKRAINE or RUSSIA)
- `systems` (list[str], optional): List of system names to filter
- `status` (list[Status], optional): List of statuses to filter
- `date_start` (date | str, optional): Start date (YYYY-MM-DD format or date object)
- `date_end` (date | str, optional): End date (YYYY-MM-DD format or date object)

**Returns:** `list[System]`

**Example:**
```python
systems = client.get_systems(
    country=Country.UKRAINE,
    status=[Status.DESTROYED],
    date_start="2024-01-01",
    date_end="2024-12-31",
)
```

##### `get_total_systems()`

Get total system data with optional filters.

**Parameters:**
- `country` (Country, optional): Country filter
- `systems` (list[str], optional): List of system names to filter

**Returns:** `list[AllSystem]`

**Example:**
```python
totals = client.get_total_systems(
    country=Country.UKRAINE,
    systems=["T-72"],
)
```

##### `get_system_types()`

Get distinct system types.

**Returns:** `list[dict[str, str]]`

**Example:**
```python
types = client.get_system_types()
```

##### `import_equipments()`

Trigger import of equipment data from scraper.

**Returns:** `dict[str, str]`

##### `import_all_equipments()`

Trigger import of all equipment totals from scraper.

**Returns:** `dict[str, str]`

##### `import_systems()`

Trigger import of system data from scraper.

**Returns:** `dict[str, str]`

##### `import_all_systems()`

Trigger import of all system totals from scraper.

**Returns:** `dict[str, str]`

##### `import_all()`

Trigger import of all data from scraper.

**Returns:** `dict[str, str]`

##### `health_check()`

Check API health status.

**Returns:** `dict[str, str]`

## Data Models

### Equipment

```python
class Equipment:
    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int
    date: str
```

### AllEquipment

```python
class AllEquipment:
    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int
```

### System

```python
class System:
    id: int
    country: str
    origin: str
    system: str
    status: str
    url: str
    date: str
```

### AllSystem

```python
class AllSystem:
    id: int
    country: str
    system: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int
```

## Enumerations

### Country

- `Country.ALL`
- `Country.UKRAINE`
- `Country.RUSSIA`

### EquipmentType

- `EquipmentType.TANKS`
- `EquipmentType.AIRCRAFT`
- `EquipmentType.HELICOPTERS`
- ... (see full list in code)

### Status

- `Status.DESTROYED`
- `Status.CAPTURED`
- `Status.ABANDONED`
- `Status.DAMAGED`

## Error Handling

The library provides specific exception classes for different error scenarios:

```python
from watpy import (
    Client,
    WarTrackAPIError,
    WarTrackAuthenticationError,
    WarTrackForbiddenError,
    WarTrackNotFoundError,
    WarTrackRateLimitError,
    WarTrackServerError,
)

client = Client()

try:
    equipments = client.get_equipments(country=Country.UKRAINE)
except WarTrackAuthenticationError:
    print("Authentication failed")
except WarTrackRateLimitError:
    print("Rate limit exceeded")
except WarTrackServerError:
    print("Server error")
except WarTrackAPIError as e:
    print(f"API error: {e}")
```

### Exception Classes

- `WarTrackAPIError`: Base exception for all API errors
- `WarTrackAuthenticationError`: Raised on 401 Unauthorized
- `WarTrackForbiddenError`: Raised on 403 Forbidden
- `WarTrackNotFoundError`: Raised on 404 Not Found
- `WarTrackRateLimitError`: Raised on 429 Too Many Requests
- `WarTrackServerError`: Raised on 500+ Server Error

## Context Manager

The client can be used as a context manager to ensure proper cleanup:

```python
with Client() as client:
    equipments = client.get_equipments(country=Country.UKRAINE)
    # Client is automatically closed when exiting the context
```

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd watpy

# Install in development mode
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests (unit tests only, uses mocked requests)
uv run pytest

# Run with coverage
uv run pytest --cov=watpy --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py

# Run integration tests (requires running API server)
uv run pytest -m integration
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy watpy
```

### Running CI Checks Locally

You can run the same checks that CI runs locally:

```bash
# Run all checks
uv run black --check .
uv run ruff check .
uv run mypy watpy
uv run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code is formatted
6. Commit your changes (following the commit message guidelines)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- War Track Dashboard API team
- All contributors who help improve this library
