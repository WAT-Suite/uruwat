"""
Data models for the War Track Dashboard API.
"""

from enum import Enum

from pydantic import BaseModel


class Country(str, Enum):
    """Country enumeration."""

    ALL = "all"
    UKRAINE = "ukraine"
    RUSSIA = "russia"


class EquipmentType(str, Enum):
    """Equipment type enumeration."""

    ALL_TYPES = "All Types"
    AIRCRAFT = "Aircraft"
    ANTI_AIRCRAFT_GUNS = "Anti-Aircraft Guns"
    ARMOURED_FIGHTING_VEHICLES = "Armoured Fighting Vehicles"
    ARMOURED_PERSONNEL_CARRIERS = "Armoured Personnel Carriers"
    ARTILLERY_SUPPORT_VEHICLES_AND_EQUIPMENT = "Artillery Support Vehicles And Equipment"
    COMMAND_POSTS_AND_COMMUNICATIONS_STATIONS = "Command Posts And Communications Stations"
    ENGINEERING_VEHICLES_AND_EQUIPMENT = "Engineering Vehicles And Equipment"
    HELICOPTERS = "Helicopters"
    INFANTRY_FIGHTING_VEHICLES = "Infantry Fighting Vehicles"
    INFANTRY_MOBILITY_VEHICLES = "Infantry Mobility Vehicles"
    JAMMERS_AND_DECEPTION_SYSTEMS = "Jammers And Deception Systems"
    MINE_RESISTANT_AMBUSH_PROTECTED = "Mine-Resistant Ambush Protected"
    MULTIPLE_ROCKET_LAUNCHERS = "Multiple Rocket Launchers"
    NAVAL_SHIPS_AND_SUBMARINES = "Naval Ships and Submarines"
    RADARS = "Radars"
    RECONNAISSANCE_UNMANNED_AERIAL_VEHICLES = "Reconnaissance Unmanned Aerial Vehicles"
    SELF_PROPELLED_ANTI_AIRCRAFT_GUNS = "Self-Propelled Anti-Aircraft Guns"
    SELF_PROPELLED_ANTI_TANK_MISSILE_SYSTEMS = "Self-Propelled Anti-Tank Missile Systems"
    SELF_PROPELLED_ARTILLERY = "Self-Propelled Artillery"
    SURFACE_TO_AIR_MISSILE_SYSTEMS = "Surface-To-Air Missile Systems"
    TANKS = "Tanks"
    TOWED_ARTILLERY = "Towed Artillery"
    TRUCKS_VEHICLES_AND_JEEPS = "Trucks, Vehicles, and Jeeps"
    UNMANNED_COMBAT_AERIAL_VEHICLES = "Unmanned Combat Aerial Vehicles"


class Status(str, Enum):
    """Status enumeration."""

    ABANDONED = "abandoned"
    DAMAGED = "damaged"
    DESTROYED = "destroyed"
    CAPTURED = "captured"


class Equipment(BaseModel):
    """Equipment data model."""

    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int
    date: str

    class Config:
        """Pydantic config."""

        frozen = True


class AllEquipment(BaseModel):
    """All equipment totals data model."""

    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int

    class Config:
        """Pydantic config."""

        frozen = True


class System(BaseModel):
    """System data model."""

    id: int
    country: str
    origin: str
    system: str
    status: str
    url: str
    date: str

    class Config:
        """Pydantic config."""

        frozen = True


class AllSystem(BaseModel):
    """All system totals data model."""

    id: int
    country: str
    system: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int

    class Config:
        """Pydantic config."""

        frozen = True


class EquipmentTypesResponse(BaseModel):
    """Equipment types response model."""

    types: list[dict[str, str]]

    class Config:
        """Pydantic config."""

        frozen = True


class SystemTypesResponse(BaseModel):
    """System types response model."""

    types: list[dict[str, str]]

    class Config:
        """Pydantic config."""

        frozen = True
