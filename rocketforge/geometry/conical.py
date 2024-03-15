from numpy import *


def get(At, RnOvRt, eps, Le, theta):
    '''
    This function returns the x and y coordinates of the divergent section of a conical nozzle
    '''
    Rt = sqrt(At/pi)        # Throat radius
    Rn = RnOvRt * Rt        # Divergent circular arc radius
    Re = Rt * sqrt(eps)     # Exit radius

    # Points coordinates
    xN = Rn * sin(theta)
    yN = Rt + Rn * (1 - cos(theta))
    xE = Le
    yE = Re

    # Divergent circular arc coordinates
    x1 = linspace(0, xN, 1000)
    y1 = - sqrt(Rn**2 - x1**2) + Rt + Rn

    # Conical section
    x2 = [xN, xE]
    y2 = [yN, yE]

    # Concatenate coordinates vectors
    x = concatenate((x1, x2))
    y = concatenate((y1, y2))

    return x, y


def get_theta(At, RnOvRt, eps, Le):
    '''
    This function returns the angle of a conical nozzle with a user defined length
    '''
    # Throat radius
    Rt = sqrt(At/pi)

    # Divergent circular arc radius
    Rn = RnOvRt * Rt

    # Exit radius
    Re = Rt * sqrt(eps)

    # Divergence angle
    theta = 0

    return theta


def le(At, RnOvRt, eps, theta):
    '''
    This function returns the length of a conical nozzle with a user defined divergence angle
    '''
    # Throat radius
    Rt = sqrt(At/pi)

    # Divergent circular arc radius
    Rn = RnOvRt * Rt

    # Exit radius
    Re = Rt * sqrt(eps)

    # Conical nozzle length
    Le = (Re - Rt - Rn * (1-cos(theta)))/tan(theta) + Rn*sin(theta)

    return Le


def lc15(At, RnOvRt, eps):
    '''
    This function returns the length of a conical nozzle with a 15 degrees divergence angle
    '''
    # Throat radius
    Rt = sqrt(At/pi)

    # Divergent circular arc radius
    Rn = RnOvRt * Rt

    # Exit radius
    Re = Rt * sqrt(eps)

    # Conical nozzle length
    Lc15 = (Re - Rt - Rn * (1-cos(radians(15))))/tan(radians(15)) + Rn*sin(radians(15))

    return Lc15