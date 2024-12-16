from numpy import *
from scipy.integrate import quad


def get(At, R1OvRt, Lc, b, R2OvR2max, epsc, ptscirc=360):
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
    pts = int(ptscirc * b / (2 * pi))
    x1 = linspace(xD, 0, pts)
    y1 = Rt + R1 - sqrt(R1**2 - x1**2)

    # Linear converging section
    x2 = linspace(xC, xD, 2)
    y2 = m * x2 + q

    # Convergent concave circular arc
    x3 = linspace(xB, xC, pts)
    y3 = Rc - R2 + sqrt(R2**2 - (x3 - xB)**2)

    # Chamber section
    x4 = linspace(xA, xB, 2)
    y4 = Rc + 0 * x4

    # Concatenate coordinates vectors
    x = concatenate((x4, x3, x2, x1))
    y = concatenate((y4, y3, y2, y1))

    return x, y


def get_Lc(At, R1OvRt, Lstar, b, R2OvR2max, epsc):
    Rt = sqrt(At/pi)            # Throat radius
    R1 = R1OvRt * Rt            # Convex circular arc radius
    Rc = Rt * sqrt(epsc)        # Chamber radius
    R2max = (Rc - Rt)/(1-cos(b)) - R1  # Maximum allowed R2
    R2 = R2OvR2max * R2max      # Concave circular arc radius

    # Points coordinates
    m = - tan(b)
    q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
    xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)

    # Compute I
    I = get_I(At, R1OvRt, b, R2OvR2max, epsc)

    # Chamber length
    Lc = (Rt**2 * Lstar - I)/Rc**2 - xB

    return Lc


def get_Lstar(At, R1OvRt, Lc, b, R2OvR2max, epsc):
    Rt = sqrt(At/pi)            # Throat radius
    R1 = R1OvRt * Rt            # Convex circular arc radius
    Rc = Rt * sqrt(epsc)        # Chamber radius
    R2max = (Rc - Rt)/(1-cos(b)) - R1  # Maximum allowed R2
    R2 = R2OvR2max * R2max      # Concave circular arc radius

    # Points coordinates
    m = - tan(b)
    q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
    xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)

    # Compute I
    I = get_I(At, R1OvRt, b, R2OvR2max, epsc)

    # Characteristic length
    Lstar = I/Rt**2 + epsc * (xB + Lc)

    return Lstar


def get_I(At, R1OvRt, b, R2OvR2max, epsc):
    Rt = sqrt(At/pi)            # Throat radius
    R1 = R1OvRt * Rt            # Convex circular arc radius
    Rc = Rt * sqrt(epsc)        # Chamber radius
    R2max = (Rc - Rt)/(1-cos(b)) - R1  # Maximum allowed R2
    R2 = R2OvR2max * R2max      # Concave circular arc radius

    # Points coordinates
    m = - tan(b)
    q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
    xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)
    xC = xB + R2 * sin(b)
    xD = - R1 * sin(b)

    # Functions
    y1 = lambda x: (Rt + R1 - sqrt(R1**2 - x**2))**2
    y2 = lambda x: (m * x + q)**2
    y3 = lambda x: (Rc - R2 + sqrt(R2**2 - (x-xB)**2))**2

    # Compute integrals
    I1 = quad(y1, xD, 0)[0]
    I2 = quad(y2, xC, xD)[0]
    I3 = quad(y3, xB, xC)[0]
    I = I1 + I2 + I3

    return I