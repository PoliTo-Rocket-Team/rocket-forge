import rocketforge.performance.config as config
import rocketforge.thermal.config as tconf
from tabulate import tabulate


def delivered():
    pc = config.pc
    eps = config.eps
    pe = config.pe
    MR = config.mr
    At = config.At
    cstar = config.cstar
    Is_vac = config.Isp_vac
    z_c = config.z_r
    z_n = config.z_n

    # Film cooling
    if tconf.film:
        k_film = (1 + (tconf.fuelfilm + config.mr*tconf.oxfilm)/100/(1 + config.mr))
    else:
        k_film = 1.0

    # Sea level pressure
    pSL = 101325

    # Nozzle exit area
    Ae = At * eps

    # Characteristic velocity
    cstar_d = z_c * cstar

    # Mass flow
    m_d = pc * At / cstar_d
    m_d_core = m_d / k_film
    m_f_d = m_d_core / (MR + 1)
    m_ox_d = m_f_d * MR
    if tconf.film:
        m_f_d = m_f_d * (1 + tconf.fuelfilm/100)
        m_ox_d = m_ox_d * (1 + tconf.oxfilm/100)

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
    T_vac_d = CF_vac_d * At * pc / k_film
    T_opt_d = CF_opt_d * At * pc / k_film
    T_SL_d = CF_SL_d * At * pc / k_film

    # Output formatting
    headers = ["Parameter", "SL", "Opt", "Vac", "Unit"]
    results = [
        ["Characteristic velocity", f"{cstar_d:.2f}", f"{cstar_d:.2f}", f"{cstar_d:.2f}", "m/s"],
        ["Effective exhaust velocity", f"{Is_SL_d * 9.80655:.2f}", f"{Is_opt_d * 9.80655:.2f}", f"{Is_vac_d * 9.80655:.2f}", "m/s"],
        ["Specific impulse", f"{Is_SL_d:.2f}", f"{Is_opt_d:.2f}", f"{Is_vac_d:.2f}", "s"],
        ["Thrust coefficient", f"{CF_SL_d:.5f}", f"{CF_opt_d:.5f}", f"{CF_vac_d:.5f}", ""],
        ["Chamber Thrust", f"{T_SL_d / 1000:.4f}", f"{T_opt_d / 1000:.4f}", f"{T_vac_d / 1000:.4f}", "kN"],
        ["Mass flow rate", f"{m_d:.4f}", f"{m_d:.4f}", f"{m_d:.4f}", "kg/s"],
        ["Fuel flow rate", f"{m_f_d:.4f}", f"{m_f_d:.4f}", f"{m_f_d:.4f}", "kg/s"],
        ["Oxidizer flow rate", f"{m_ox_d:.4f}", f"{m_ox_d:.4f}", f"{m_ox_d:.4f}", "kg/s"],
    ]
    output = tabulate(results, headers, numalign="right")

    return output
