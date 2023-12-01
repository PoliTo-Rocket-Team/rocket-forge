from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate
import sys


def main():
    if len(sys.argv) > 9:
        sys.exit("Too many input arguments.\n" + usage)
    if len(sys.argv) < 9:
        sys.exit("Too few input arguments.\n" + usage)

    try:
        ox = sys.argv[1]
        fuel = sys.argv[2]
        pc = float(sys.argv[3]) * 100000  # 40 bar
        mr = float(sys.argv[4])  # 2.9
        eps = float(sys.argv[5])  # 2.7
        epsc = float(sys.argv[6])  # 8
        At = float(sys.argv[7]) / 10**4  # 8.72 cm^2
        iter = int(sys.argv[8]) + 1  # 10
    except ValueError:
        sys.exit("ValueError\n" + usage)

    if epsc < 0 :
        epsc = None

    pamb = 101325

    get_ideal_performance(ox, fuel, pamb, pc, mr, eps, epsc, At, iter)
    get_delivered_performance()


def get_ideal_performance(ox, fuel, pamb, pc, mr, eps, epsc, At, iter):
    try:
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
    except Exception:
        sys.exit(usage)

    cstar = C.get_Cstar(Pc=pc, MR=mr)
    m = pc * At / cstar
    mf = m / (mr + 1)
    mox = mr * mf

    pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)
    pt = pc / C.get_Throat_PcOvPe(Pc=pc, MR=mr)

    Isp_vac = C.get_Isp(Pc=pc, MR=mr, eps=eps)
    Isp_sl = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pamb)[0]
    Isp_opt = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pe)[0]

    c_vac = Isp_vac * 9.80655
    c_sl = Isp_sl * 9.80655
    c_opt = Isp_opt * 9.80655

    CF_opt, CF_sl, mode = C.get_PambCf(Pamb=pamb, Pc=pc, MR=mr, eps=eps)
    CF_vac = c_vac / cstar

    Tc, Tt, Te = C.get_Temperatures(Pc=pc, MR=mr, eps=eps)
    rhoc, rhot, rhoe = C.get_Densities(Pc=pc, MR=mr, eps=eps)

    cpc, muc, lc, Prc = C.get_Chamber_Transport(Pc=pc, MR=mr, eps=eps)
    cpt, mut, lt, Prt = C.get_Throat_Transport(Pc=pc, MR=mr, eps=eps)
    cpe, mue, le, Pre = C.get_Exit_Transport(Pc=pc, MR=mr, eps=eps)

    mwt, gammat = C.get_Throat_MolWt_gamma(Pc=pc, MR=mr, eps=eps)
    mwe, gammae = C.get_exit_MolWt_gamma(Pc=pc, MR=mr, eps=eps)

    Me = C.get_MachNumber(Pc=pc, MR=mr, eps=eps)
    ac, at, ae = C.get_SonicVelocities(Pc=pc, MR=mr, eps=eps)
    Hc, Ht, He = C.get_Enthalpies(Pc=pc, MR=mr, eps=eps)
    we_opt = Me * ae

    T_vac = CF_vac * pc * At
    T_opt = CF_opt * pc * At
    T_sl = CF_sl * pc * At

    p = [pc / 100000]
    T = [Tc]
    rho = [rhoc]
    cp = [cpc]
    mu = [muc]
    l = [lc]
    Pr = [Prc]
    gamma = [0]
    M = [0]
    a = [ac]
    H = [Hc]

    for x in range(iter):
        x = 1 + x * (eps - 1) / iter
        p.append(pc / 100000 / C.get_PcOvPe(Pc=pc, MR=mr, eps=x))
        T.append(C.get_Temperatures(Pc=pc, MR=mr, eps=x)[2])
        rho.append(C.get_Densities(Pc=pc, MR=mr, eps=x)[2])
        cp.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x)[0])
        mu.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x)[1])
        l.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x)[2])
        Pr.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x)[3])
        gamma.append(C.get_exit_MolWt_gamma(Pc=pc, MR=mr, eps=x)[1])
        M.append(C.get_MachNumber(Pc=pc, MR=mr, eps=x))
        a.append(C.get_SonicVelocities(Pc=pc, MR=mr, eps=x)[2])
        H.append(C.get_Enthalpies(Pc=pc, MR=mr, eps=x)[2])

    p.insert(0, "Pressure")
    T.insert(0, "Temperature")
    rho.insert(0, "Density")
    cp.insert(0, "Heat capacity")
    mu.insert(0, "Viscosity")
    l.insert(0, "Thermal conductivity")
    Pr.insert(0, "Prandtl")
    gamma.insert(0, "Gamma")
    M.insert(0, "Mach number")
    a.insert(0, "Sonic velocity")
    H.insert(0, "Enthalpy")

    p.append("bar")
    T.append("K")
    rho.append("kg/m^3")
    cp.append("J/kg-K")
    mu.append("millipoise")
    l.append("mcal/cm-K-s")
    Pr.append("")
    gamma.append("")
    M.append("")
    a.append("m/s")
    H.append("kJ/kg")

    print("\n\033[1mTheoretical Performance (RocketCEA)\033[0m\n")
    headers = ["Parameter", "SL", "Opt", "Vac", "Unit"]
    results = [
        [
            "Characteristic velocity",
            f"{cstar:.2f}",
            f"{cstar:.2f}",
            f"{cstar:.2f}",
            "m/s",
        ],
        [
            "Effective exhaust velocity",
            f"{c_sl:.2f}",
            f"{c_opt:.2f}",
            f"{c_vac:.2f}",
            "m/s",
        ],
        ["Specific impulse", f"{Isp_sl:.2f}", f"{Isp_opt:.2f}", f"{Isp_vac:.2f}", "s"],
        ["Thrust coefficient", f"{CF_sl:.5f}", f"{CF_opt:.5f}", f"{CF_vac:.5f}", ""],
        [
            "Chamber Thrust",
            f"{T_sl / 1000:.4f}",
            f"{T_opt / 1000:.4f}",
            f"{T_vac / 1000:.4f}",
            "kN",
        ],
        ["Mass flow rate", f"{m:.4f}", f"{m:.4f}", f"{m:.4f}", "kg/s"],
        ["Fuel flow rate", f"{mf:.4f}", f"{mf:.4f}", f"{mf:.4f}", "kg/s"],
        ["Oxidizer flow rate", f"{mox:.4f}", f"{mox:.4f}", f"{mox:.4f}", "kg/s"],
    ]
    print(tabulate(results, headers, numalign="right"))

    print()

    headers = ["Parameter", "Chamber"]
    for x in range(iter):
        headers.append(f"{x / (iter - 1) * 100:.2f}%")
    headers[2] = "Throat"
    headers[-1] = "Exit"
    headers.append("Unit")

    results = [p, T, rho, cp, mu, l, Pr, gamma, M, a, H]
    print(tabulate(results, headers, numalign="right"))


def get_delivered_performance():
    # TODO
    return


usage = (
    "usage: python "
    + sys.argv[0]
    + " <Oxidizer> <Fuel> <Pc> <MR> <eps> <epsc> <At> <N>\n"
    + "<Oxidizer>: oxidizer (for example LOX or MON3)\n"
    + "<Fuel>: fuel (for example LH2, CH4, or MMH)\n"
    + "<Pc>: chamber pressure [Bar]\n"
    + "<MR>: mixture ratio\n"
    + "<eps>: supersonic area ratio\n"
    + "<epsc>: contraction ratio of finite area combustor (use -1 for infinite area combustor)\n"
    + "<At>: throat area [cm^2]\n"
    + "<N>: number of stations (integer >= 1)"
)

if __name__ == "__main__":
    print("\033[1mEfesto Rocket Forge\033[0m")
    main()
