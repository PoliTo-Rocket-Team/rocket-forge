from numpy import *
from matplotlib.pyplot import *
from scipy.optimize import brentq
from rocketprops.rocket_prop import get_prop


def main():
    ### INPUT ###
    n_s = 80 # number of stations to compute

    # Coolant
    P = get_prop('CH4') # coolant
    Tci = 115 # coolant inlet temperature
    mc = 0.4925 # coolant mass flow rate

    # Geometry
    Rcyl = 0.04712 * ones(30)
    Rco = linspace(0.04712, 0.01666, 30)
    Rd = linspace(0.01666+(0.02738-0.01666)/20, 0.02738, 20)
    R = concatenate((Rcyl, Rco, Rd)) # station radius
    Lc = 0.15589 # chamber length
    Le = 0.05344 # divergent length
    At = 0.000872 # throat section area
    Nc = 70 # number of channels (TODO)
    deco = linspace(0.0025, 0.0012, 60)
    ded = linspace(0.0012, 0.002, 20)
    de = concatenate((deco, ded)) # channel diameter
    Ac = de**2
    k = 285 # wall thermal conductivity
    dy = 0.0008 # wall thickness
    A = (2*pi*R)*(Lc+Le)/n_s # convective heat transfer surface

    # Thermodynamic properties
    p = linspace(45*10**5, 70*10**5, n_s) # coolant line pressure
    Prco = linspace(0.494049, 496142, 60)
    Prd = array([0.498062, 0.499387, 0.500754, 0.502214, 0.503783, 0.505462, 0.507248, 0.509135, 0.511115, 0.513179, 0.515319, 0.517527, 0.519792, 0.522108, 0.524466, 0.526858, 0.529276, 0.531716, 0.534169, 0.536634])
    Pr = concatenate((Prco, Prd)) # prandtl number
    gammaco = linspace(1.14, 1.14168, 60)
    gammad = array([1.14413, 1.14587, 1.14755, 1.14921, 1.15085, 1.15247, 1.15407, 1.15564, 1.15719, 1.1587, 1.16019, 1.16164, 1.16306, 1.16444, 1.16579, 1.1671, 1.16837, 1.16961, 1.17081, 1.17198])
    gamma = concatenate((gammaco, gammad)) # gamma
    Mcyl = zeros(30)
    Mco = linspace(0, 1, 30)
    Md = array([1.31303, 1.44362, 1.54177, 1.62242, 1.69165, 1.75262, 1.80726, 1.85687, 1.90236, 1.94441, 1.98353, 2.02012, 2.05451, 2.08696, 2.1177, 2.1469, 2.17472, 2.20129, 2.22673, 2.25115])
    M = concatenate((Mcyl, Mco, Md)) # mach number
    pc = 40 * 10**5 # chamber pressure
    Ts = 3369.19 # stagnation temperature
    cstar = 1817.04 # delivered characteristic velocity
    Pr0 = Pr[0] # upstream prandtl number
    cp0 = 5830.22 # upstream specific heat capacity
    mu0 = 1.06192 * 0.0001 # upstream dynamic viscosity
    ### END INPUT ###

    # Variables initialization
    i = 0
    Twg = zeros(n_s)
    Tc = zeros(n_s)
    lambdac = zeros(n_s)
    cpc = zeros(n_s)
    rhoc = zeros(n_s)
    muc = zeros(n_s)

    while True:
        # At each station, calculate the gas-side heat flux (convective and radiation) for given Twg
        Dt = sqrt(At/pi)
        Taw = Ts * (1+Pr**0.33 * (gamma-1)/2 * M**2)/(1+(gamma-1)/2*M**2)
        sigma = (0.5*Twg/Ts * (1+(gamma-1)/2*M**2)+0.5)**(-0.68) * (1+(gamma-1)/2*M**2)**(-0.12)
        h = 0.026 / (Dt**0.2) * mu0**0.2 *cp0 / (Pr0**0.6) * (pc/cstar)**0.8 * (Dt/R)*0.1 *(At/pi/R**2)**0.9 * sigma
        q = h * (Taw - Twg)

        # At each station, calculate the coolant heating and coolant exit temperature for known
        # input temperature (the direction of space-marching depends on the coolant flow direction).
        Tc[0] = Tci
        cpc[0] = P.CpAtTdegR(Tc[0] * 1.8) * 4186
        for n in range(n_s-1):
            Tc[n+1] = Tc[n] + q[n] * A[n] / cpc[n] / mc
            cpc[n+1] = P.CpAtTdegR(Tc[n+1] * 1.8) * 4186
        Tc = Tc[::-1]
        cpc = cpc[::-1]
        for n in range(n_s):
            # rhoc[n] = P.SGLiqAtTdegR(Tc[n] * 1.8) * 1000
            rhoc[n] = P.SG_compressed(Tc[n] * 1.8, p[n] * 6894.8) * 1000
            # muc[n] = P.ViscAtTdegR(Tc[n] * 1.8) / 10
            muc[n] = P.Visc_compressed(Tc[n] * 1.8, p[n] * 6894.8) / 10
            lambdac[n] = P.CondAtTdegR(Tc[n] * 1.8) * 1.72958

        # Calculate the coolant-side heat transfer coefficient hc
        u = mc / rhoc / Ac
        Rec = u * de * rhoc / muc
        Prc = muc * cpc / lambdac
        # Nu = 0.0185 * Rec**0.8 * Prc**0.4 * (Tc/Twc)**0.1 for methane
        hc = [lambda Twc, n=n: 0.0185*Rec[n]**0.8 * Prc[n]**0.4 * (Tc[n]/Twc)**0.1 * lambdac[n] / de[n] for n in range(n_s)]

        # From known heat flux and coolant-side heat transfer coefficient, calculate new values
        # of the coolant-side temperature Twc and the gas-side temperature Twg
        Twc = ones(n_s)
        for n in range(n_s):
            eq = lambda Twc: Tc[n] - Twc + q[n]/hc[n](Twc)
            Twc[n] = brentq(eq, 1, 10000)
        Twg_old = Twg
        Twg = Twc + q * dy / k
        i += 1

        # Calculate the convergence criteria
        if all(abs((Twg - Twg_old)/Twg) < 0.001):
            print(f"Executed in {i} iterations.")
            plot(Twg, label="Twg")
            plot(Twc, label="Twc")
            plot(Tc, label="Tc")
            break

    grid()
    legend()
    show()


if __name__ == "__main__":
    main()