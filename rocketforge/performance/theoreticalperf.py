import rocketforge.performance.config as config
from tabulate import tabulate
from rocketcea.cea_obj_w_units import CEA_Obj


def theoretical(i=2, fr=0, fat=0):
    ox = config.ox
    fuel = config.fuel
    pc = config.pc
    mr = config.mr
    eps = config.eps
    epsc = config.epsc

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

    # Characteristic velocity
    cstar = C.get_Cstar(Pc=pc, MR=mr)

    # Vacuum specific impulse
    Isp_vac = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)

    # Vacuum specific impulse (equilibrium)
    Isp_vac_eq = C.get_Isp(Pc=pc, MR=mr, eps=eps)

    # Vacuum specific impulse (frozen)
    Isp_vac_fr = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=1)

    # Temperature
    Tc, Tt, Te = C.get_Temperatures(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)

    # Density
    rhoc, rhot, rhoe = C.get_Densities(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)

    # Chamber transport properties
    cpc, muc, lc, Prc = C.get_Chamber_Transport(Pc=pc, MR=mr, eps=eps, frozen=fr)

    # Sonic velocity
    ac, at, ae = C.get_SonicVelocities(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)

    # Enthalpy
    Hc, Ht, He = C.get_Enthalpies(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)

    # Thermodynamic properties initialization
    p = ["Pressure", pc / 100000]
    T = ["Temperature", Tc]
    rho = ["Density", rhoc]
    cp = ["Heat capacity", cpc]
    mu = ["Viscosity", muc / 1.0e4]
    l = ["Thermal conductivity", lc]
    Pr = ["Prandtl", Prc]
    gamma = ["Gamma", 0]
    M = ["Mach number", 0]
    a = ["Sonic velocity", ac]
    H = ["Enthalpy", Hc]

    # Thermodynamic properties calculations
    for x in range(i):
        x = 1 + x * (eps - 1) / (i - 1)
        p.append(pc / 100000 / C.get_PcOvPe(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat))
        T.append(C.get_Temperatures(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
        rho.append(C.get_Densities(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
        cp.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[0])
        mu.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[1] / 1.0e4)
        l.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
        Pr.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[3])
        gamma.append(C.get_exit_MolWt_gamma(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[1])
        M.append(C.get_MachNumber(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat))
        a.append(C.get_SonicVelocities(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
        H.append(C.get_Enthalpies(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])

    # Thermodynamic properties units of measure
    p.append("bar")
    T.append("K")
    rho.append("kg/m^3")
    cp.append("J/kg-K")
    mu.append("Pa-s")
    l.append("mcal/cm-K-s")
    Pr.append("")
    gamma.append("")
    M.append("")
    a.append("m/s")
    H.append("kJ/kg")

    # Output formatting (thermodynamic properties)
    headers = ["Parameter", "Chamber"]
    for x in range(i):
        headers.append(f"{x / (i - 1) * 100:.2f}%")
    headers[2] = "Throat"
    headers[-1] = "Exit"
    headers.append("Unit")
    results = [p, T, rho, cp, mu, l, Pr, gamma, M, a, H]
    output = tabulate(results, headers, numalign="right")

    config.cstar = cstar
    config.Isp_vac = Isp_vac
    config.Isp_vac_eq = Isp_vac_eq
    config.Isp_vac_fr = Isp_vac_fr
    config.td_props = results
    config.gammae = results[7][-2]
    config.Me = results[8][-2]

    return output