from numpy import *


def get(At, R1OvRt, Lc, b, R2OvR2max, epsc):
    '''
    This function returns the x and y coordinates of the convergent section of the nozzle
    '''
    Rt = sqrt(At/pi)            # Throat radius
    R1 = R1OvRt * Rt            # Convex circular arc radius
    Rc = Rt * sqrt(epsc)        # Chamber radius
    R2max = (Rc - Rt)/(1-cos(b)) - R1  # Maximum allowed R2
    R2 = R2OvR2max * R2max      # Concave circular arc radius

    # Points coordinates
    m = - tan(b)
    q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
    xA = - Lc
    xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)
    xC = xB + R2 * sin(b)
    xD = - R1 * sin(b)

    # Convergent convex circular arc
    x1 = linspace(xD, 0, 1000)
    y1 = Rt + R1 - sqrt(R1**2 - x1**2)

    # Linear converging section
    x2 = linspace(xC, xD, 1000)
    y2 = m * x2 + q

    # Convergent concave circular arc
    x3 = linspace(xB, xC, 1000)
    y3 = Rc - R2 + sqrt(R2**2 - (x3 - xB)**2)

    # Chamber section
    x4 = linspace(xA, xB, 2)
    y4 = Rc + 0 * x4

    # Concatenate coordinates vectors
    x = concatenate((x4, x3, x2, x1))
    y = concatenate((y4, y3, y2, y1))

    return x, y