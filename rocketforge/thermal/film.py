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
        pressure_units="Pa",
        temperature_units="K",
        sonic_velocity_units="m/s",
        enthalpy_units="kJ/kg",
        density_units="kg/m^3",
        specific_heat_units="J/kg-K",
    )

    Tg_equilibrium = C.get_Temperatures(Pc=pc, MR=mr, eps=eps, frozen=0, frozenAtThroat=0)
    Tg = Tg_equilibrium[0]

    return Tg

ox = 'O2'
fuel = 'CH4'
pc = 40 # bar
mr = 2.9
eps = 2.7
Tg = perf(ox, fuel, pc, mr, eps, epsc=None, i=2, fr=0, fat=0) # K

Tl = 220 # K

properties = methane_properties(pc, Tl)

density = properties[2]

print("La densità del metano è:", density, "kg/m3")



    


