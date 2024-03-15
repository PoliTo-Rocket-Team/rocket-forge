from numpy import *


def get_divergent(At, RnOvRt, Le, thetan, thetae, eps):
    '''
    This function returns the x and y coordinates of the divergent for a thrust-optimized parabolic (TOP) nozzle
    '''
    Rt = sqrt(At/pi)        # Throat radius
    Rn = RnOvRt * Rt        # Divergent circular arc radius
    Re = Rt * sqrt(eps)     # Exit radius

    # Points coordinates
    xN = Rn * sin(thetan)
    yN = Rt + Rn*(1-cos(thetan))
    xE = Le
    yE = Re

    # Divergent circular arc coordinates
    x1 = linspace(0, xN, 1000)
    y1 = - sqrt(Rn**2 - x1**2) + Rt + Rn

    # Canted parabola contour
    xA = (yE-xE*tan(thetae)-yN+xN*tan(thetan))/(tan(thetan)-tan(thetae))
    DN = lambda theta: (xA-xN)*(tan(thetan)-tan(theta))
    DE = lambda theta: (xE-xA)*(tan(thetae)-tan(theta))
    alpha = lambda theta: DN(theta)/(DN(theta)-DE(theta))
    xp = lambda theta: xN+alpha(theta)*(2-alpha(theta))*(xA-xN)+alpha(theta)**2 *(xE-xA)
    yp = lambda theta: yN+tan(theta)*(xp(theta)-xN)+alpha(theta)*DN(theta)
    theta = linspace(thetan, thetae, 1000)
    x2 = xp(theta)
    y2 = yp(theta)

    # Concatenate coordinates vectors
    x = concatenate((x1, x2))
    y = concatenate((y1, y2))

    return x, y


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