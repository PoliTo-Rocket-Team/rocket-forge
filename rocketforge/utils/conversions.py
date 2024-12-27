from typing import Dict, Tuple


def pressure_uom(uom: str) -> float:
    """
    Converts a pressure unit of measure to Pascals.

    Parameters:
        uom (str): The pressure unit (e.g., "Pa", "MPa", "bar", "atm", "psia").

    Returns:
        float: Conversion factor to Pascals.
    """
    uoms: Dict[str, float] = {
        "Pa": 1.0,
        "MPa": 1.0e6,
        "bar": 1.0e5,
        "atm": 1.01325e5,
        "psia": 6894.8,
    }
    return uoms[uom]


def thrust_uom(uom: str) -> float:
    """
    Converts a force unit of measure to Newtons.

    Parameters:
        uom (str): The force unit (e.g., "N", "kN", "MN", "kgf", "lbf").

    Returns:
        float: Conversion factor to Newtons.
    """
    uoms: Dict[str, float] = {
        "N": 1.0,
        "kN": 1.0e3,
        "MN": 1.0e6,
        "kgf": 9.80655,
        "lbf": 4.44822162,
    }
    return uoms[uom]


def mass_uom(uom: str) -> float:
    """
    Converts a mass unit of measure to kilograms.

    Parameters:
        uom (str): The mass unit (e.g., "kg", "g", "lb").

    Returns:
        float: Conversion factor to kilograms.
    """
    uoms: Dict[str, float] = {
        "kg": 1.0,
        "g": 1.0e-3,
        "lb": 0.4535924,
    }
    return uoms[uom]


def temperature_uom(value: float, uom: str) -> float:
    """
    Converts a temperature value to Kelvins.

    Parameters:
        value (float): The temperature value to be converted.
        uom (str): The temperature unit (e.g., "K", "C", "F", "R").

    Returns:
        float: The temperature in Kelvins.
    """
    uoms: Dict[str, Tuple[float, float]] = {
        "K": (0.0, 1.0),
        "C": (273.15, 1.0),
        "F": (255.3722, 1.0 / 1.8),
        "R": (0.0, 1.0 / 1.8),
    }
    offset, scale = uoms[uom]
    return offset + value * scale


def mdot_uom(uom: str) -> float:
    """
    Converts a mass flow rate unit of measure to kg/s.

    Parameters:
        uom (str): The mass flow rate unit (e.g., "kg/s", "g/s", "lb/s").

    Returns:
        float: Conversion factor to kg/s.
    """
    uoms: Dict[str, float] = {
        "kg/s": 1.0,
        "g/s": 1.0e-3,
        "lb/s": 0.4535924,
    }
    return uoms[uom]


def density_uom(uom: str) -> float:
    """
    Converts a density unit of measure to kg/m³.

    Parameters:
        uom (str): The density unit (e.g., "kg/m3", "g/ml", "g/cm3",
                   "lb/in3", "lb/ft3", "lb/gal").

    Returns:
        float: Conversion factor to kg/m³.
    """
    uoms: Dict[str, float] = {
        "kg/m3": 1.0,
        "g/ml": 1.0e3,
        "g/cm3": 1.0e3,
        "lb/in3": 27677.83,
        "lb/ft3": 16.02,
        "lb/gal": 119.83,
    }
    return uoms[uom]


def length_uom(uom: str) -> float:
    """
    Converts a length unit of measure to meters.

    Parameters:
        uom (str): The length unit (e.g., "m", "cm", "mm", "in", "ft").

    Returns:
        float: Conversion factor to meters.
    """
    uoms: Dict[str, float] = {
        "m": 1.0,
        "cm": 1.0e-2,
        "mm": 1.0e-3,
        "in": 0.0254,
        "ft": 0.3048,
    }
    return uoms[uom]


def area_uom(uom: str) -> float:
    """
    Converts a surface area unit of measure to square meters.

    Parameters:
        uom (str): The area unit (e.g., "m2", "cm2", "mm2", "sq in", "sq ft").

    Returns:
        float: Conversion factor to square meters.
    """
    uoms: Dict[str, float] = {
        "m2": 1.0,
        "cm2": 1.0e-4,
        "mm2": 1.0e-6,
        "sq in": 0.00064516,
        "sq ft": 0.09290304,
    }
    return uoms[uom]


def angle_uom(uom: str) -> float:
    """
    Converts an angle unit of measure to radians.

    Parameters:
        uom (str): The angle unit (e.g., "deg", "rad").

    Returns:
        float: Conversion factor to radians.
    """
    uoms: Dict[str, float] = {
        "deg": 0.017453292519943295,
        "rad": 1.0,
    }
    return uoms[uom]
