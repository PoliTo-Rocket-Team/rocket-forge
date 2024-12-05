def pressure_uom(uom: str) -> float:
    """
    Converts pressure unit of measure to Pascal
    """
    uoms = {"Pa": 1, "MPa": 1000000, "bar": 100000, "atm": 101325, "psia": 6894.8}
    return uoms[uom]


def thrust_uom(uom: str) -> float:
    """
    Converts force unit of measure to Newtons
    """
    uoms = {"N": 1, "kN": 1000, "MN": 1000000, "kgf": 9.80655, "lbf": 4.44822162}
    return uoms[uom]


def mass_uom(uom: str) -> float:
    """
    Converts mass unit of measure to kilograms
    """
    uoms = {"kg": 1, "g": 0.001, "lb": 0.4535924}
    return uoms[uom]


def temperature_uom(value: float, uom : str) -> float:
    """
    Converts temperature unit of measure to Kelvins
    """
    uoms = {"K": (0.0, 1.0), "C": (273.15, 1.0), "F": (255.3722, 1.0/1.8), "R": (0.0, 1.0/1.8)}
    return uoms[uom][0] + value * uoms[uom][1]


def mdot_uom(uom: str) -> float:
    """
    Converts mass flow rate unit of measure to kg/s
    """
    uoms = {"kg/s": 1, "g/s": 0.001, "lb/s": 0.4535924}
    return uoms[uom]


def density_uom(uom: str) -> float:
    """
    Converts density unit of measure to kg/m3
    """
    uoms = {"kg/m3": 1, "g/ml": 1000, "g/cm3": 1000, "lb/in3": 27677.83, "lb/ft3": 16.02, "lb/gal": 119.83}
    return uoms[uom]


def length_uom(uom: str) -> float:
    """
    Converts length unit of measure to meters
    """
    uoms = {
        "m": 1,
        "cm": 0.01,
        "mm": 0.001,
        "in": 0.0254,
        "ft": 0.3048,
    }
    return uoms[uom]


def area_uom(uom: str) -> float:
    """
    Converts surface unit of measure to square meters
    """
    uoms = {
        "m2": 1,
        "cm2": 10 ** (-4),
        "mm2": 10 ** (-6),
        "sq in": 0.00064516,
        "sq ft": 0.09290304,
    }
    return uoms[uom]


def angle_uom(uom: str) -> float:
    """
    Converts angle unit of measure to radians
    """
    uoms = {
        "deg": 0.017453292519943295,
        "rad": 1,
    }
    return uoms[uom]
