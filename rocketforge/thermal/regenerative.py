from numpy import *
from matplotlib.pyplot import *
from scipy.optimize import brentq

# Regenerative cooling draft

### INPUT ###
n_s = 7 # number of stations
Twg_guess = 300 # initial wall temperature guess
Tci = 115 # coolant inlet temperature

# Geometry
R = array([0.04712, 0.01666, 0.018, 0.0212, 0.0235, 0.026, 0.02738]) # station radius
A = 2*pi*R*0.2/n_s # convective heat transfer surface
Nc = 70 # number of channels (TO DO)
Ac = 3.14 * 10**(-6) # channel section area
de = 0.002 # channel diameter
k = 15 # wall thermal conductivity
dy = 0.001 # wall thickness

# Coolant properties
mc = 0.4925 # mass flow rate
rhoc = 352.16 # density
muc = 53.431 # dynamic viscosity
cpc = 3925.2 # specific heat capacity
lambdac = 126300 # thermal conductivity
### END INPUT ###

# Known data
pc = 40 * 10**5 # chamber pressure
Ts = 3369.19 # stagnation temperature
Pr = array([0.494049, 0.496142, 0.502214, 0.509135, 0.517527, 0.526858, 0.536634]) # prandtl number
gamma = array([1.14, 1.14168, 1.14921, 1.15564, 1.16164, 1.1671, 1.17198]) # gamma
M = array([0, 0.999999, 1.62242, 1.85687, 2.02012, 2.1469, 2.25115]) # mach number
cstar = 1817.04 # delivered characteristic velocity
Pr0 = 0.494049 # upstream prandtl number
cp0 = 5830.22 # upstream specific heat capacity
mu0 = 1.06192 * 0.0001 # upstream dynamic viscosity
At = 0.000872 # throat section area

# 2. On the first iteration step i=0, assign the initial gas-side temperatures Twg at each station.
i = 0
Twg = array(n_s * [Twg_guess])

while True:
    # 3. At each station, calculate the gas-side heat flux (convective and radiation) for given Twg
    Dt = sqrt(At/pi)
    Taw = Ts * (1+Pr**0.33 * (gamma-1)/2 * M**2)/(1+(gamma-1)/2*M**2)
    sigma = (0.5*Twg/Ts * (1+(gamma-1)/2*M**2)+0.5)**(-0.68) * (1+(gamma-1)/2*M**2)**(-0.12)
    h = 0.026 / (Dt**0.2) * mu0**0.2 *cp0 / (Pr0**0.6) * (pc/cstar)**0.8 * (Dt/R)*0.1 *(At/pi/R**2)**0.9 * sigma
    q = h * (Taw - Twg)

    # 4. At each station, calculate the coolant heating and coolant exit temperature for known
    # input temperature (the direction of space-marching depends on the coolant flow direction).
    Tc = array(n_s * [Tci])
    for n in range(n_s-1):
        Tc[n + 1] = Tc[n] + q[n] * A[n] / cpc / mc
    Tc = Tc[::-1]

    # 5. Calculate the coolant-side heat transfer coefficient hc
    u = mc / rhoc / Ac
    Rec = u*de*rhoc / muc
    Prc = muc * cpc / lambdac
    # Nu = 0.0185 * Rec**0.8 * Prc**0.4 * (Tc/Twc)**0.1 for methane
    hc = lambda Tc, Twc: 0.0185 * Rec**0.8 *Prc**0.4 * (Tc/Twc)**0.1 * lambdac / de

    # 6. From known heat flux and coolant-side heat transfer coefficient, calculate new values
    # of the coolant-side temperature Twc and the gas-side temperature Twg
    Twc = ones(n_s)
    for n in range(n_s):
        eq = lambda Twc: Tc[n] - Twc + q[n]/hc(Tc[n], Twc)
        Twc[n] = brentq(eq, 1, 100000)
    Twg_old = Twg
    Twg = Twc + q * dy / k
    i = i + 1

    # 7. Calculate the convergence criteria
    if all(abs((Twg - Twg_old)/Twg) < 0.001):
        break

np.set_printoptions(formatter={'float_kind':"{:.2f}".format})
print(q/1000)
print(Twg)
print(Twc)
print(Tc)
print(i)
plot(Twg)
plot(Twc)
plot(Tc)
print(hc(Tc,Twg))
show()