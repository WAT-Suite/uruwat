# uruwat

[![PyPI version](https://img.shields.io/pypi/v/uruwat.svg)](https://pypi.org/project/uruwat/)
[![PyPI downloads](https://img.shields.io/pypi/dm/uruwat.svg)](https://pypi.org/project/uruwat/)
[![Python versions](https://img.shields.io/pypi/pyversions/uruwat.svg)](https://pypi.org/project/uruwat/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/wat-suite/uruwat/workflows/CI/badge.svg)](https://github.com/wat-suite/uruwat/actions)
[![codecov](https://codecov.io/gh/wat-suite/uruwat/branch/main/graph/badge.svg)](https://codecov.io/gh/wat-suite/uruwat)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![GitHub stars](https://img.shields.io/github/stars/wat-suite/uruwat.svg?style=social&label=Star)](https://github.com/wat-suite/uruwat)

Python client wrapper for the War Track Dashboard API. This library provides a type-safe, async-compatible interface for interacting with the War Track Dashboard API, making it easy to query equipment and system data.

## Features

- ✅ **Type-safe**: Full type hints with Pydantic models
- ✅ **Async-compatible**: Built on httpx for async support
- ✅ **Error handling**: Custom exception classes for different error scenarios
- ✅ **Context manager**: Proper resource cleanup with context manager support
- ✅ **Well-tested**: Comprehensive test suite with high coverage
- ✅ **Modern Python**: Requires Python 3.10+

## Installation

```bash
pip install uruwat
```

Or using `uv`:

```bash
uv add uruwat
```

Or using `poetry`:

```bash
poetry add uruwat
```

## Quick Start

```python
from uruwat import Client, Country, EquipmentType

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
from uruwat import Status

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
from uruwat import Client

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
from uruwat import (
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
cd uruwat

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
uv run pytest --cov=uruwat --cov-report=html

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
uv run mypy uruwat
```

### Running CI Checks Locally

You can run the same checks that CI runs locally:

```bash
# Run all checks
uv run black --check .
uv run ruff check .
uv run mypy uruwat
uv run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and code is formatted (`uv run black . && uv run ruff check . && uv run pytest`)
6. Commit your changes (following [Conventional Commits](https://www.conventionalcommits.org/))
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/). Commit messages should be formatted as:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Code Style

- This project uses [Black](https://black.readthedocs.io/) for code formatting
- [Ruff](https://github.com/astral-sh/ruff) is used for linting
- [mypy](https://mypy.readthedocs.io/) is used for type checking
- All code must pass linting and type checking

## Releasing

This project uses GitHub Releases to trigger PyPI publishing. The workflow automatically publishes to PyPI when a final (non-pre-release) GitHub Release is created.

### Release Workflow

#### 1. Update Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update to your new version
```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

#### 2. Update Changelog

Update `CHANGELOG.md` with the changes for this version.

#### 3. Commit and Push Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

#### 4. Create a Git Tag

Create a tag matching the version (with or without 'v' prefix):

```bash
# Option 1: Tag with 'v' prefix
git tag v0.2.0

# Option 2: Tag without prefix
git tag 0.2.0

# Push the tag
git push origin v0.2.0
```

**Important:** The tag version must match the version in `pyproject.toml` exactly (excluding the 'v' prefix if used).

#### 5. Create GitHub Release

Go to the [GitHub Releases page](https://github.com/wat-suite/uruwat/releases) and click "Draft a new release":

**For Pre-Release (Testing):**
- **Tag:** Select the tag you just created (e.g., `v0.2.0`)
- **Release title:** `v0.2.0` (or your version)
- **Description:** Copy from `CHANGELOG.md` or write release notes
- **☑️ Set as a pre-release:** Check this box
- Click **"Publish release"**

Pre-releases are **not** published to PyPI. Use them for testing before the final release.

**For Final Release (Publishing to PyPI):**
- **Tag:** Select the tag you just created (e.g., `v0.2.0`)
- **Release title:** `v0.2.0` (or your version)
- **Description:** Copy from `CHANGELOG.md` or write release notes
- **☐ Set as a pre-release:** Leave this unchecked
- Click **"Publish release"**

The GitHub Actions workflow will:
1. Verify the tag version matches `pyproject.toml`
2. Build the package
3. Check the package with `twine`
4. Publish to PyPI (only for final releases, not pre-releases)

### Workflow Summary

```
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Commit and push changes
4. Create and push git tag
5. Create GitHub Release (pre-release or final)
   └─> Pre-release: Testing only, not published to PyPI
   └─> Final release: Automatically published to PyPI
```

### Troubleshooting

- **Version mismatch error:** Ensure the tag version (without 'v' prefix) exactly matches `pyproject.toml` version
- **Pre-release published:** Pre-releases are intentionally skipped. Create a final release to publish to PyPI
- **Workflow not triggered:** Ensure the release is "Published" (not "Draft") and the tag exists

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/wat-suite/uruwat/issues) on GitHub.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Acknowledgments

- War Track Dashboard API team
- All contributors who help improve this library
