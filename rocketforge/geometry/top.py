from numpy import *


def get(At, RnOvRt, Le, thetan, thetae, eps):
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
    theta = linspace(thetan, thetae, 1000)
    xA = (yE-xE*tan(thetae)-yN+xN*tan(thetan))/(tan(thetan)-tan(thetae))
    DN = (xA-xN)*(tan(thetan)-tan(theta))
    DE = (xE-xA)*(tan(thetae)-tan(theta))
    alpha = DN/(DN-DE)
    x2 = xN+alpha*(2-alpha)*(xA-xN)+alpha**2 *(xE-xA)
    y2 = yN+tan(theta)*(x2-xN)+alpha*DN

    # Concatenate coordinates vectors
    x = concatenate((x1, x2))
    y = concatenate((y1, y2))

    return x, y