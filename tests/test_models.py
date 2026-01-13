"""Unit tests for data models."""

import pytest

from watpy.models import (
    AllEquipment,
    AllSystem,
    Country,
    Equipment,
    EquipmentType,
    Status,
    System,
)


@pytest.mark.unit
class TestModels:
    """Test data models."""

    def test_equipment_model(self):
        """Test Equipment model."""
        equipment = Equipment(
            id=1,
            country="ukraine",
            type="Tanks",
            destroyed=10,
            abandoned=2,
            captured=5,
            damaged=3,
            total=20,
            date="2024-01-01",
        )

        assert equipment.id == 1
        assert equipment.country == "ukraine"
        assert equipment.type == "Tanks"
        assert equipment.total == 20
        assert equipment.date == "2024-01-01"

    def test_all_equipment_model(self):
        """Test AllEquipment model."""
        all_equipment = AllEquipment(
            id=1,
            country="ukraine",
            type="Tanks",
            destroyed=100,
            abandoned=20,
            captured=50,
            damaged=30,
            total=200,
        )

        assert all_equipment.id == 1
        assert all_equipment.country == "ukraine"
        assert all_equipment.total == 200

    def test_system_model(self):
        """Test System model."""
        system = System(
            id=1,
            country="ukraine",
            origin="Russia",
            system="T-72",
            status="destroyed",
            url="https://example.com",
            date="2024-01-01",
        )

        assert system.id == 1
        assert system.country == "ukraine"
        assert system.system == "T-72"
        assert system.status == "destroyed"

    def test_all_system_model(self):
        """Test AllSystem model."""
        all_system = AllSystem(
            id=1,
            country="ukraine",
            system="T-72",
            destroyed=50,
            abandoned=10,
            captured=25,
            damaged=15,
            total=100,
        )

        assert all_system.id == 1
        assert all_system.country == "ukraine"
        assert all_system.total == 100


@pytest.mark.unit
class TestEnums:
    """Test enumeration types."""

    def test_country_enum(self):
        """Test Country enum."""
        assert Country.UKRAINE.value == "ukraine"
        assert Country.RUSSIA.value == "russia"
        assert Country.ALL.value == "all"

    def test_equipment_type_enum(self):
        """Test EquipmentType enum."""
        assert EquipmentType.TANKS.value == "Tanks"
        assert EquipmentType.AIRCRAFT.value == "Aircraft"

    def test_status_enum(self):
        """Test Status enum."""
        assert Status.DESTROYED.value == "destroyed"
        assert Status.CAPTURED.value == "captured"
        assert Status.ABANDONED.value == "abandoned"
        assert Status.DAMAGED.value == "damaged"
