from rocketcea.cea_obj_w_units import CEA_Obj
import sys


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

    Is_vac_frozen = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=1)

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

    p = [pc]
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
        p.append(pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=x))
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
    
    return [Te, Tc, we, cstar, Isp_vac, pe, Is_vac_frozen]


usage = (
    "usage: python "
    + sys.argv[0]
    + " <Oxidizer> <Fuel> <Pc> <MR> <eps> <epsc> <At> <N>\n"
    + "<Oxidizer>: oxidizer (for example LOX or MON3)\n"
    + "<Fuel>: fuel (for example LH2, CH4, or MMH)\n"
    + "<Pc>: chamber pressure [Pa]\n"
    + "<MR>: mixture ratio\n"
    + "<eps>: supersonic area ratio\n"
    + "<epsc>: contraction ratio of finite area combustor (use -1 for infinite area combustor)\n"
    + "<At>: throat area [m^2]\n"
    + "<N>: number of stations (integer >= 1)"
)

if len(sys.argv) > 9:
    sys.exit("Too many input arguments.\n" + usage)
if len(sys.argv) < 9:
    sys.exit("Too few input arguments.\n" + usage)

try:
    ox = sys.argv[1]
    fuel = sys.argv[2]
    pc = float(sys.argv[3])
    mr = float(sys.argv[4])
    eps = float(sys.argv[5])
    epsc = float(sys.argv[6])
    At = float(sys.argv[7])
    iter = int(sys.argv[8]) + 1
except ValueError:
    sys.exit("ValueError\n" + usage)

if epsc < 0 :
    epsc = None

pamb = 101325

x = get_ideal_performance(ox, fuel, pamb, pc, mr, eps, epsc, At, iter)
