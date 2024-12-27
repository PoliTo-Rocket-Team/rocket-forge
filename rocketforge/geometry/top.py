import numpy as np
from typing import Tuple


def get(
    At: float,
    RnOvRt: float,
    Le: float,
    thetan: float,
    thetae: float,
    eps: float,
    ptscirc: int = 360,
    ptspar: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns the x and y coordinates of the divergent section for a thrust-
    optimized parabolic (TOP) nozzle.

    Parameters:
        At (float): Throat area.
        RnOvRt (float): Ratio of divergent circular arc radius to throat radius.
        Le (float): Divergent nozzle length.
        thetan (float): Starting parabola angle in radians.
        thetae (float): Parabola angle at the exit in radians.
        eps (float): Expansion area ratio.
        ptscirc (int, optional): Points per circle for the circular arc.
            Default is 360.
        ptspar (int, optional): Number of points for the parabolic contour.
            Default is 100.

    Returns:
        Tuple[np.ndarray, np.ndarray]: x and y coordinates of the divergent
            section.
    """
    Rt = np.sqrt(At / np.pi)  # Throat radius
    Rn = RnOvRt * Rt          # Divergent circular arc radius
    Re = Rt * np.sqrt(eps)    # Exit radius

    # Points coordinates
    xN = Rn * np.sin(thetan)
    yN = Rt + Rn * (1 - np.cos(thetan))
    xE = Le
    yE = Re

    # Divergent circular arc coordinates
    pts = int(ptscirc * thetan / (2 * np.pi))
    x1 = np.linspace(0, xN, pts)
    y1 = -np.sqrt(Rn**2 - x1**2) + Rt + Rn

    # Canted parabola contour
    theta = np.linspace(thetan, thetae, ptspar)
    xA = (
        (yE - xE * np.tan(thetae) - yN + xN * np.tan(thetan))
        / (np.tan(thetan) - np.tan(thetae))
    )
    DN = (xA - xN) * (np.tan(thetan) - np.tan(theta))
    DE = (xE - xA) * (np.tan(thetae) - np.tan(theta))
    alpha = DN / (DN - DE)
    x2 = (
        xN + alpha * (2 - alpha) * (xA - xN)
        + alpha**2 * (xE - xA)
    )
    y2 = yN + np.tan(theta) * (x2 - xN) + alpha * DN

    # Concatenate coordinate arrays
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))

    return x, y
