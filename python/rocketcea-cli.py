from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate
import sys, math


def main():
    if len(sys.argv) > 9:
        sys.exit("Too many input arguments.\n" + usage)
    if len(sys.argv) < 9:
        sys.exit("Too few input arguments.\n" + usage)

    try:
        ox = sys.argv[1]
        fuel = sys.argv[2]
        pc = float(sys.argv[3]) * 100000
        mr = float(sys.argv[4])
        eps = float(sys.argv[5])
        epsc = float(sys.argv[6])
        At = float(sys.argv[7]) / 10**4
        iter = int(sys.argv[8]) + 1
    except ValueError:
        sys.exit("ValueError\n" + usage)

    if epsc < 0 :
        epsc = None

    pamb = 101325

    Le = 0.05344
    theta_ex = 8 / 180 * math.pi

    Z, Cs = 0, 0

    h0, a, b = 0, 1, 1

    pe, cstar, Is_vac, Tc, Te, we = get_ideal_performance(ox, fuel, pamb, pc, mr, eps, epsc, At, iter)
    get_delivered_performance(pc, pe, mr, eps, At, Le, theta_ex, cstar, Is_vac, Tc, Te, we, Z, Cs, h0, a, b, pamb)


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
    we = Me * ae

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
        x = 1 + x * (eps - 1) / (iter - 1)
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

    headers = ["Parameter", "Chamber"]
    for x in range(iter):
        headers.append(f"{x / (iter - 1) * 100:.2f}%")
    headers[2] = "Throat"
    headers[-1] = "Exit"
    headers.append("Unit")

    results = [p, T, rho, cp, mu, l, Pr, gamma, M, a, H]
    # print()
    # print(tabulate(results, headers, numalign="right"))

    return pe, cstar, Isp_vac, Tc, Te, we 


def get_delivered_performance(pc, pe, MR, eps, At, Le, theta_ex, cstar, Is_vac, Tc, Te, we, Z, Cs, h0, a, b, pSL):

    Ae = At * eps
    re = math.sqrt(Ae / math.pi)
    rt = math.sqrt(At / math.pi)

    # Finite reaction rate combustion factor
    er1 = (h0 / rt)**a * (pSL / pc)**b * math.log10(re /rt)
    er2 = max(0, 0.021 - 0.01 * math.log(pc / 2 / 10**6))
    z_r = (1 - er1) * (1 - er2)

    # Multi-phase loss factor
    z_zw = 1 - Z * Cs / we**2 * (Tc - Te * (1 + math.log(Tc / Te)))
    z_zt = 1 - Z / 2
    z_z = 0.2 * z_zw + 0.8 * z_zt

    # Divergence loss factor
    alpha = math.atan((re - rt) / Le)
    z_d = 0.5 * (1 + math.cos((alpha + theta_ex) / 2))

    # Friction loss factor (TODO)
    z_f = 0.98695

    # Drag correction factor
    z_drag = z_r * z_f * z_z

    # Nozzle correction factor
    z_n = z_f * z_d * z_z

    # Chamber correction factor
    z_c = z_r
    cstar_d = z_c * cstar

    # Mass flow
    m_d = pc * At / cstar_d
    m_f_d = m_d / (MR + 1)
    m_ox_d = m_f_d * MR

    # Specific impulse
    Fe = Ae / m_d
    Is_vac_d = z_c * z_n * Is_vac
    Is_opt_d = Is_vac_d - Fe * pe / 9.80655
    Is_SL_d = Is_vac_d - Fe * pSL / 9.80655

    # Thrust coefficient
    CF_vac_d = Is_vac_d * 9.80655 / cstar_d
    CF_opt_d = Is_opt_d * 9.80655 / cstar_d
    CF_SL_d = Is_SL_d * 9.80655 / cstar_d

    # Chamber thrust
    T_vac_d = CF_vac_d * At * pc
    T_opt_d = CF_opt_d * At * pc
    T_SL_d = CF_SL_d * At * pc
    
    print("\n\033[1mDelivered Performance\033[0m\n")
    headers = ["Parameter", "SL", "Opt", "Vac", "Unit"]
    results = [
        [
            "Characteristic velocity",
            f"{cstar_d:.2f}",
            f"{cstar_d:.2f}",
            f"{cstar_d:.2f}",
            "m/s",
        ],
        [
            "Effective exhaust velocity",
            f"{Is_SL_d * 9.80655:.2f}",
            f"{Is_opt_d * 9.80655:.2f}",
            f"{Is_vac_d * 9.80655:.2f}",
            "m/s",
        ],
        ["Specific impulse", f"{Is_SL_d:.2f}", f"{Is_opt_d:.2f}", f"{Is_vac_d:.2f}", "s"],
        ["Thrust coefficient", f"{CF_SL_d:.5f}", f"{CF_opt_d:.5f}", f"{CF_vac_d:.5f}", ""],
        [
            "Chamber Thrust",
            f"{T_SL_d / 1000:.4f}",
            f"{T_opt_d / 1000:.4f}",
            f"{T_vac_d / 1000:.4f}",
            "kN",
        ],
        ["Mass flow rate", f"{m_d:.4f}", f"{m_d:.4f}", f"{m_d:.4f}", "kg/s"],
        ["Fuel flow rate", f"{m_f_d:.4f}", f"{m_f_d:.4f}", f"{m_f_d:.4f}", "kg/s"],
        ["Oxidizer flow rate", f"{m_ox_d:.4f}", f"{m_ox_d:.4f}", f"{m_ox_d:.4f}", "kg/s"],
    ]
    print(tabulate(results, headers, numalign="right"))
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
