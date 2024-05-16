import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def methane_properties(pres, temper):
    
    var = float(pres) # pres turns into a float variable
    fraz = var % 1 # calculation of the fractional part

    # pressure is rounded to the nearest integer or nearest half integer

    if fraz <= 0.25:
        var_rounded = int(var)
    if 0.25 < fraz <= 0.75:
        var_rounded = int(var)+0.5
    if fraz > 0.75:
        var_rounded = int(var)+1

    # data extraction from NIST_Methane.xlsx
    sheetname = str(var_rounded)
    testdata = pd.read_excel('rocketforge/thermal/NIST_Methane.xlsx', sheet_name=sheetname)
    temp = np.array(testdata['Temperature (K)'])
    tc = np.array(testdata['Therm. Cond. (W/m*K)'])
    rho = np.array(testdata['Density (kg/m3)'])
    mu = np.array(testdata['Viscosity (Pa*s)'])
    cp = np.array(testdata['Cp (J/g*K)'])
    cv = np.array(testdata['Cv (J/g*K)'])

    # data interpolation
    ftc = interp1d(temp, tc, kind='cubic')
    frho = interp1d(temp, rho, kind='cubic')
    fmu = interp1d(temp, mu, kind='cubic')
    fcp = interp1d(temp, cp, kind='cubic')
    fcv = interp1d(temp, cv, kind='cubic')

    # calculation of properties from interpolated curves
    lambd = ftc(temper)
    mu = fmu(temper)
    rho = frho(temper)
    cp = fcp(temper)
    cv = fcv(temper)
    gamma = cp/cv

    list = [lambd, mu, rho, cp, cv, gamma]

    return list