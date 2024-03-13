from math import *
from numpy import *
from scipy.optimize import fsolve


def get_divergent(At, RnOvRt, Le, thetan, thetae, eps):

    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)
    Nt = Rn * sin(thetan)

    x1 = linspace(0, Nt, 1000)
    y1 = lambda x: - sqrt(Rn**2 - x**2) + Rt + Rn

    xN = Nt
    yN = Rt + Rn*(1-cos(thetan))
    xE = Le
    yE = Re
    xA=(yE-xE*tan(thetae)-yN+xN*tan(thetan))/(tan(thetan)-tan(thetae))
    DN=lambda theta: (xA-xN)*(tan(thetan)-tan(theta))
    DE=lambda theta: (xE-xA)*(tan(thetae)-tan(theta))
    alpha=lambda theta: DN(theta)/(DN(theta)-DE(theta))
    xp= lambda theta: xN+alpha(theta)*(2-alpha(theta))*(xA-xN)+alpha(theta)**2 *(xE-xA)
    yp= lambda theta: yN+tan(theta)*(xp(theta)-xN)+alpha(theta)*DN(theta)

    theta = linspace(thetan, thetae, 1000)
    x2 = xp(theta)

    x = concatenate((x1, x2))
    y = concatenate((y1(x1), yp(theta)))

    return x, y


def lc15(At, RnOvRt, eps):
    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)
    Lc15 = (Re - Rt - Rn * (1-cos(radians(15))))/tan(radians(15)) + Rn*sin(radians(15))
    return Lc15