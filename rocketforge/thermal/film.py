import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from rocketcea.cea_obj_w_units import CEA_Obj
from methane_calculator import methane_properties


def perf(ox, fuel, pc, mr, eps, epsc=None, i=2, fr=0, fat=0):
    # Sea level pressure
    pamb = 101325

    # CEA_Obj
    C = CEA_Obj(
        oxName=ox,
        fuelName=fuel,
        fac_CR=epsc,
        cstar_units="m/s",
        pressure_units="bar",
        temperature_units="K",
        sonic_velocity_units="m/s",
        enthalpy_units="kJ/kg",
        density_units="kg/m^3",
        specific_heat_units="J/kg-K",
    )

    Tg_equilibrium = C.get_Temperatures(Pc=pc, MR=mr, eps=eps, frozen=0, frozenAtThroat=0)
    rho = C.get_Densities(Pc=pc, MR=mr, eps=eps, frozen=0, frozenAtThroat=0)
    a=C.get_SonicVelocities(Pc=pc, MR=mr, eps=eps, frozen=0, frozenAtThroat=0)
    M=C.get_MachNumber(Pc=pc, MR=mr, eps=eps, frozen=0, frozenAtThroat=0)
    Tg = Tg_equilibrium[0]
    rho_g=rho[0]
    a_g=a[0]

    list = [Tg,rho_g,a_g]

    return list

ox = 'O2'
fuel = 'CH4'
pc = 40 # bar
mr = 2.9
eps = 2.7
m_dot = 1.90893 # kg/s
A_c = np.pi*(0.09423/2)**2 #m2
Tl_sat = 186.11
Tg = perf(ox, fuel, pc, mr, eps, epsc=None, i=2, fr=0, fat=0)[0]
rho_g = perf(ox, fuel, pc, mr, eps, epsc=None, i=2, fr=0, fat=0)[1]
a_g=perf(ox, fuel, pc, mr, eps, epsc=None, i=2, fr=0, fat=0)[2]

Tl = 220 # K

properties = methane_properties(pc, Tl)

cp_l = properties[3]
rho_l = properties[2]
mu_l=properties[1]
lambda_l=properties[0]
pr_l=mu_l*cp_l/lambda_l
u_g = m_dot/(rho_g*A_c)

print(u_g)



    


