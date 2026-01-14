# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-12-19

### Added
- Async client support (`AsyncClient`) with async/await methods
- Async tests for all async client methods
- Support for async context managers

### Changed
- Improved type annotations and type safety

[Unreleased]: https://github.com/WAT-Suite/uruwat/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/WAT-Suite/uruwat/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/WAT-Suite/uruwat/releases/tag/v0.1.0

## [0.1.0] - 2024-01-XX

### Added
- Initial release of uruwat (formerly watpy)
- Python client wrapper for the War Track Dashboard API
- Type-safe API client with full type hints using Pydantic models
- Support for querying equipment and system data
- Error handling with custom exception classes
- Context manager support for proper resource cleanup
- Comprehensive test suite with high coverage
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks for code quality
- Documentation and examples

### Changed
- Renamed package from `watpy` to `uruwat`
- Updated all imports and references to use new package name

### Fixed
- Fixed CI workflow to use standard pip instead of uv run
- Fixed type checking issues with proper type narrowing
- Fixed linting issues (unused imports, ruff config)
- Fixed test failures with proper error handling
