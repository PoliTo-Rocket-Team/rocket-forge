import numpy as np
from scipy.integrate import quad
from typing import Tuple


def get(
    At: float,
    R1OvRt: float,
    Lc: float,
    b: float,
    R2OvR2max: float,
    epsc: float,
    ptscirc: int = 360
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the x and y coordinates of the convergent section of the nozzle.

    Parameters:
        At (float): Throat area.
        R1OvRt (float): Ratio of convex circular arc radius to throat radius.
        Lc (float): Chamber length.
        b (float): Contraction angle in radians.
        R2OvR2max (float): Ratio of concave arc radius to maximum allowed value.
        epsc (float): Contraction area ratio.
        ptscirc (int, optional): Points per circle for the circular arcs.
            Default is 360.

    Returns:
        Tuple[np.ndarray, np.ndarray]: x and y coordinates of the convergent
            section.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    R1 = R1OvRt * Rt          # Convex circular arc radius
    Rc = Rt * np.sqrt(epsc)   # Chamber radius
    R2max = (Rc - Rt) / (1 - np.cos(b)) - R1  # Maximum allowed R2
    R2 = R2OvR2max * R2max    # Concave circular arc radius

    # Points coordinates
    m = -np.tan(b)
    q = Rt + R1 * (1 - np.cos(b) - np.tan(b) * np.sin(b))
    xA = -Lc
    xB = (Rc - R2 * (1 - np.cos(b)) - q) / m - R2 * np.sin(b)
    xC = xB + R2 * np.sin(b)
    xD = -R1 * np.sin(b)

    # Convergent convex circular arc
    pts = int(ptscirc * b / (2 * np.pi))
    x1 = np.linspace(xD, 0, pts)
    y1 = Rt + R1 - np.sqrt(R1**2 - x1**2)

    # Linear converging section
    x2 = np.linspace(xC, xD, 2)
    y2 = m * x2 + q

    # Convergent concave circular arc
    x3 = np.linspace(xB, xC, pts)
    y3 = Rc - R2 + np.sqrt(R2**2 - (x3 - xB) ** 2)

    # Chamber section
    x4 = np.linspace(xA, xB, 2)
    y4 = Rc + 0 * x4

    # Concatenate coordinates vectors
    x = np.concatenate((x4, x3, x2, x1))
    y = np.concatenate((y4, y3, y2, y1))

    return x, y


def get_Lc(
    At: float,
    R1OvRt: float,
    Lstar: float,
    b: float,
    R2OvR2max: float,
    epsc: float
) -> float:
    """
    Computes the chamber length for a given characteristic length.

    Parameters:
        At (float): Throat area.
        R1OvRt (float): Ratio of convex circular arc radius to throat radius.
        Lstar (float): Characteristic length.
        b (float): Contraction angle in radians.
        R2OvR2max (float): Ratio of concave arc radius to maximum allowed value.
        epsc (float): Contraction area ratio.

    Returns:
        float: Chamber length.
    """
    Rt = np.sqrt(At / np.pi)
    R1 = R1OvRt * Rt
    Rc = Rt * np.sqrt(epsc)
    R2max = (Rc - Rt) / (1 - np.cos(b)) - R1
    R2 = R2OvR2max * R2max

    m = -np.tan(b)
    q = Rt + R1 * (1 - np.cos(b) - np.tan(b) * np.sin(b))
    xB = (Rc - R2 * (1 - np.cos(b)) - q) / m - R2 * np.sin(b)

    I = get_I(At, R1OvRt, b, R2OvR2max, epsc)
    Lc = (Rt**2 * Lstar - I) / Rc**2 - xB

    return Lc


def get_Lstar(
    At: float,
    R1OvRt: float,
    Lc: float,
    b: float,
    R2OvR2max: float,
    epsc: float
) -> float:
    """
    Computes the characteristic length for a given chamber length.

    Parameters:
        At (float): Throat area.
        R1OvRt (float): Ratio of convex circular arc radius to throat radius.
        Lc (float): Chamber length.
        b (float): Contraction angle in radians.
        R2OvR2max (float): Ratio of concave arc radius to maximum allowed value.
        epsc (float): Contraction area ratio.

    Returns:
        float: Characteristic length.
    """
    Rt = np.sqrt(At / np.pi)
    R1 = R1OvRt * Rt
    Rc = Rt * np.sqrt(epsc)
    R2max = (Rc - Rt) / (1 - np.cos(b)) - R1
    R2 = R2OvR2max * R2max

    m = -np.tan(b)
    q = Rt + R1 * (1 - np.cos(b) - np.tan(b) * np.sin(b))
    xB = (Rc - R2 * (1 - np.cos(b)) - q) / m - R2 * np.sin(b)

    I = get_I(At, R1OvRt, b, R2OvR2max, epsc)
    Lstar = I / Rt**2 + epsc * (xB + Lc)

    return Lstar


def get_I(
    At: float,
    R1OvRt: float,
    b: float,
    R2OvR2max: float,
    epsc: float
) -> float:
    """
    Computes the integral I for characteristic length calculations.

    Parameters:
        At (float): Throat area.
        R1OvRt (float): Ratio of convex circular arc radius to throat radius.
        b (float): Contraction angle in radians.
        R2OvR2max (float): Ratio of concave arc radius to maximum allowed value.
        epsc (float): Contraction area ratio.

    Returns:
        float: Computed integral value.
    """
    Rt = np.sqrt(At / np.pi)
    R1 = R1OvRt * Rt
    Rc = Rt * np.sqrt(epsc)
    R2max = (Rc - Rt) / (1 - np.cos(b)) - R1
    R2 = R2OvR2max * R2max

    m = -np.tan(b)
    q = Rt + R1 * (1 - np.cos(b) - np.tan(b) * np.sin(b))
    xB = (Rc - R2 * (1 - np.cos(b)) - q) / m - R2 * np.sin(b)
    xC = xB + R2 * np.sin(b)
    xD = -R1 * np.sin(b)

    y1 = lambda x: (Rt + R1 - np.sqrt(R1**2 - x**2)) ** 2
    y2 = lambda x: (m * x + q) ** 2
    y3 = lambda x: (Rc - R2 + np.sqrt(R2**2 - (x - xB) ** 2)) ** 2

    I1 = quad(y1, xD, 0)[0]
    I2 = quad(y2, xC, xD)[0]
    I3 = quad(y3, xB, xC)[0]
    I = I1 + I2 + I3

    return I
