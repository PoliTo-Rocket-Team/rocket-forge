import numpy as np
from scipy.optimize import brentq
from typing import Tuple


def get(
    At: float,
    RnOvRt: float,
    eps: float,
    Le: float,
    theta: float,
    ptscirc: int = 360
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the x and y coordinates of the divergent section of a conical nozzle.

    Parameters:
        At (float): Throat area.
        RnOvRt (float): Ratio of divergent circular arc radius to throat radius.
        eps (float): Expansion area ratio.
        Le (float): Divergent nozzle length.
        theta (float): Divergence angle in radians.
        ptscirc (int, optional): Points per circle for the circular arc.
            Default is 360.

    Returns:
        Tuple[np.ndarray, np.ndarray]: x and y coordinates of the divergent
            section.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    Rn = RnOvRt * Rt          # Divergent circular arc radius
    Re = Rt * np.sqrt(eps)    # Exit radius

    # Points coordinates
    xN = Rn * np.sin(theta)
    yN = Rt + Rn * (1 - np.cos(theta))
    xE = Le
    yE = Re

    # Divergent circular arc coordinates
    pts = int(ptscirc * theta / (2 * np.pi))
    x1 = np.linspace(0, xN, pts)
    y1 = -np.sqrt(Rn**2 - x1**2) + Rt + Rn

    # Conical section
    x2 = np.array([xN, xE])
    y2 = np.array([yN, yE])

    # Concatenate coordinate arrays
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))

    return x, y


def get_theta(
    At: float,
    RnOvRt: float,
    eps: float,
    Le: float
) -> float:
    """
    Returns the divergence angle of a conical nozzle for a given length.

    Parameters:
        At (float): Throat area.
        RnOvRt (float): Ratio of divergent circular arc radius to throat radius.
        eps (float): Expansion area ratio.
        Le (float): Divergent nozzle length.

    Returns:
        float: Divergence angle in radians.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    Rn = RnOvRt * Rt          # Divergent circular arc radius
    Re = Rt * np.sqrt(eps)    # Exit radius

    # Equation to solve for theta
    def equation(theta: float) -> float:
        return (
            (Re - Rt - Rn * (1 - np.cos(theta))) / np.tan(theta)
            + Rn * np.sin(theta)
            - Le
        )

    theta_solution = brentq(
        equation,
        np.radians(0.0001),
        np.radians(89.9999)
    )

    return theta_solution


def le(
    At: float,
    RnOvRt: float,
    eps: float,
    theta: float
) -> float:
    """
    Returns the length of a conical nozzle for a specified divergence angle.

    Parameters:
        At (float): Throat area.
        RnOvRt (float): Ratio of divergent circular arc radius to throat radius.
        eps (float): Expansion area ratio.
        theta (float): Divergence angle in radians.

    Returns:
        float: Divergent nozzle length.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    Rn = RnOvRt * Rt          # Divergent circular arc radius
    Re = Rt * np.sqrt(eps)    # Exit radius

    # Calculate nozzle length
    Le = (
        (Re - Rt - Rn * (1 - np.cos(theta))) / np.tan(theta)
        + Rn * np.sin(theta)
    )

    return Le


def lc15(
    At: float,
    RnOvRt: float,
    eps: float
) -> float:
    """
    Returns the length of a conical nozzle with a 15-degree divergence angle.

    Parameters:
        At (float): Throat area.
        RnOvRt (float): Ratio of divergent circular arc radius to throat radius.
        eps (float): Expansion area ratio.

    Returns:
        float: Nozzle length with 15-degree divergence.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    Rn = RnOvRt * Rt          # Divergent circular arc radius
    Re = Rt * np.sqrt(eps)    # Exit radius

    theta = np.radians(15)  # 15-degree divergence angle
    Lc15 = (
        (Re - Rt - Rn * (1 - np.cos(theta))) / np.tan(theta)
        + Rn * np.sin(theta)
    )

    return Lc15
