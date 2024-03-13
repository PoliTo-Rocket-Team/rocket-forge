from math import *
from numpy import *
from scipy.optimize import fsolve


def get_geometry11(thetae, thetan, Le, At, RnOvRt):

    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt

    Nt = Rn * sin(thetan)

    a = (tan(thetan)-tan(thetae)) / (2 * Rn * sin(thetan) - 2 * Le)
    b = tan(thetae) - 2 * a * Le
    c = Rt + Rn * (1-cos(thetan)) - a * Rn**2 * (sin(thetan))**2 - b * Rn * sin(thetan)

    y1 = lambda x: - sqrt(Rn**2 - x**2) + Rt + Rn
    y2 = lambda x: a * x**2 + b * x + c
    
    x1 = linspace(0, Nt, 1000)
    x2 = linspace(Nt, Le, 1000)
    x = concatenate((x1, x2))
    y = concatenate((y1(x1), y2(x2)))

    Re = a * Le**2 + b * Le + c
    eps = (Re / Rt)**2

    return x, y, eps


def get_geometry111(thetae, thetan, eps, At, RnOvRt):

    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)

    def equations(vars):
        a, b, c, Le = vars
        e1 = a * Rn**2 * (sin(thetan))**2 + b * Rn * sin(thetan) + c - Rt - Rn*(1-cos(thetan))
        e2 = a * Le**2 + b * Le + c - Re
        e3 = 2 * a * Rn * sin(thetan) + b - tan(thetan)
        e4 = 2 * a * Le + b - tan(thetae)
        return [e1, e2, e3, e4]

    x0 = [1, 1, 1, 4 * Rt]
    sol = fsolve(equations, x0)
    Le = sol[3]

    x, y, thetae = get_geometry10(eps, thetan, Le, At, RnOvRt)

    return x, y, Le


def get_geometry10(eps, thetan, Le, At, RnOvRt):

    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)

    Nt = Rn * sin(thetan)

    a = (Re - tan(thetan)*Le - Rt - Rn*(1-cos(thetan)) + Rn*sin(thetan)*tan(thetan)) / (Rn*sin(thetan) - Le)**2
    b = tan(thetan) - 2 * a * Rn * sin(thetan)
    c = Rt + Rn * (1-cos(thetan)) - a * Rn**2 * (sin(thetan))**2 - b * Rn * sin(thetan)

    y1 = lambda x: - sqrt(Rn**2 - x**2) + Rt + Rn
    y2 = lambda x: a * x**2 + b * x + c
    
    x1 = linspace(0, Nt, 1000)
    x2 = linspace(Nt, Le, 1000)
    x = concatenate((x1, x2))
    y = concatenate((y1(x1), y2(x2)))

    thetae = atan(2 * a * Le + b)

    return x, y, thetae


def get_geometry01(eps, thetae, Le, At, RnOvRt):
    
    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)

    def equations(vars):
        a, b, c, thetan = vars
        e1 = a * Rn**2 * (sin(thetan))**2 + b * Rn * sin(thetan) + c - Rt - Rn*(1-cos(thetan))
        e2 = a * Le**2 + b * Le + c - Re
        e3 = 2 * a * Rn * sin(thetan) + b - tan(thetan)
        e4 = 2 * a * Le + b - tan(thetae)
        return [e1, e2, e3, e4]

    x0 = [1, 1, 1, pi/6]
    sol = fsolve(equations, x0)
    thetan = sol[3]

    x, y, thetae = get_geometry10(eps, thetan, Le, At, RnOvRt)

    return x, y, thetan


def lc15(At, RnOvRt, eps):
    Rt = sqrt(At/pi)
    Rn = RnOvRt * Rt
    Re = Rt * sqrt(eps)
    Lc15 = (Re - Rt - Rn * (1-cos(15/180*pi)))/tan(15/180*pi) + Rn*sin(15/180*pi)
    return Lc15