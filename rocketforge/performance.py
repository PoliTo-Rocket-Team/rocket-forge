from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel
import math


class PerformanceFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(PerformanceFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Performance Analysis"
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)


def theoretical(ox, fuel, pc, mr, eps, epsc, iter, frozen):
    pamb = 101325

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

    cstar = C.get_Cstar(Pc=pc, MR=mr)

    pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps, frozen=frozen)

    Isp_vac = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=frozen)
    Isp_sl = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pamb, frozen=frozen)[0]
    Isp_opt = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pe, frozen=frozen)[0]

    c_vac = Isp_vac * 9.80655
    c_sl = Isp_sl * 9.80655
    c_opt = Isp_opt * 9.80655

    CF_opt, CF_sl, mode = C.get_PambCf(Pamb=pamb, Pc=pc, MR=mr, eps=eps)
    CF_vac = c_vac / cstar

    Tc, Tt, Te = C.get_Temperatures(Pc=pc, MR=mr, eps=eps, frozen=frozen)
    rhoc, rhot, rhoe = C.get_Densities(Pc=pc, MR=mr, eps=eps, frozen=frozen)

    cpc, muc, lc, Prc = C.get_Chamber_Transport(Pc=pc, MR=mr, eps=eps, frozen=frozen)

    ac, at, ae = C.get_SonicVelocities(Pc=pc, MR=mr, eps=eps, frozen=frozen)
    Hc, Ht, He = C.get_Enthalpies(Pc=pc, MR=mr, eps=eps, frozen=frozen)

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
        p.append(pc / 100000 / C.get_PcOvPe(Pc=pc, MR=mr, eps=x, frozen=frozen))
        T.append(C.get_Temperatures(Pc=pc, MR=mr, eps=x, frozen=frozen)[2])
        rho.append(C.get_Densities(Pc=pc, MR=mr, eps=x, frozen=frozen)[2])
        cp.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=frozen)[0])
        mu.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=frozen)[1])
        l.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=frozen)[2])
        Pr.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=frozen)[3])
        gamma.append(C.get_exit_MolWt_gamma(Pc=pc, MR=mr, eps=x, frozen=frozen)[1])
        M.append(C.get_MachNumber(Pc=pc, MR=mr, eps=x, frozen=frozen))
        a.append(C.get_SonicVelocities(Pc=pc, MR=mr, eps=x, frozen=frozen)[2])
        H.append(C.get_Enthalpies(Pc=pc, MR=mr, eps=x, frozen=frozen)[2])

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
    ]
    output = tabulate(results, headers, numalign="right")

    headers = ["Parameter", "Chamber"]
    for x in range(iter):
        headers.append(f"{x / (iter - 1) * 100:.2f}%")
    headers[2] = "Throat"
    headers[-1] = "Exit"
    headers.append("Unit")

    results = [p, T, rho, cp, mu, l, Pr, gamma, M, a, H]
    output2 = tabulate(results, headers, numalign="right")

    return (
        cstar,
        Isp_vac,
        Isp_opt,
        Isp_sl,
        CF_vac,
        CF_opt,
        CF_sl,
        results,
        output,
        output2,
    )


def correction_factors(
    pc, eps, At, Le, theta_ex, Is_vac, Is_vac_frozen, Tc, Te, we, Z, Cs
):
    Ae = At * eps
    re = math.sqrt(Ae / math.pi)
    rt = math.sqrt(At / math.pi)

    # Finite reaction rate combustion factor
    er1 = 0.34 - 0.34 * Is_vac_frozen / Is_vac
    er2 = max(0, 0.021 - 0.01 * math.log(pc / 2 / 10**6))
    z_r = (1 - er1) * (1 - er2)

    # Multi-phase loss factor
    z_zw = 1 - Z * Cs / we**2 * (Tc - Te * (1 + math.log(Tc / Te)))
    z_zt = 1 - Z / 2
    z_z = 0.2 * z_zw + 0.8 * z_zt

    # Divergence loss factor
    alpha = math.atan((re - rt) / Le)
    z_d = 0.5 * (1 + math.cos((alpha + theta_ex) / 2))

    # Friction loss factor
    z_f = z_f = 0.997732 - 0.403077 * (pc * rt) ** (-0.5598)

    # Drag correction factor
    z_drag = z_r * z_f * z_z

    # Nozzle correction factor
    z_n = z_f * z_d * z_z

    # Chamber correction factor
    z_c = z_r

    results = [
        ["Chamber correction factor", z_c],
        ["Nozzle correction factor", z_n],
        ["Drag correction factor", z_drag],
        ["Friction loss factor", z_f],
        ["Divergence correction factor", z_d],
        ["Multi-phase loss factor", z_z],
    ]
    output = tabulate(results)

    return z_r, z_c, z_z, z_d, z_f, z_n, z_drag, output


def delivered(pc, eps, pe, MR, At, cstar, Is_vac, pSL, z_c, z_n):
    Ae = At * eps

    # Characteristic velocity
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
        [
            "Specific impulse",
            f"{Is_SL_d:.2f}",
            f"{Is_opt_d:.2f}",
            f"{Is_vac_d:.2f}",
            "s",
        ],
        [
            "Thrust coefficient",
            f"{CF_SL_d:.5f}",
            f"{CF_opt_d:.5f}",
            f"{CF_vac_d:.5f}",
            "",
        ],
        [
            "Chamber Thrust",
            f"{T_SL_d / 1000:.4f}",
            f"{T_opt_d / 1000:.4f}",
            f"{T_vac_d / 1000:.4f}",
            "kN",
        ],
        ["Mass flow rate", f"{m_d:.4f}", f"{m_d:.4f}", f"{m_d:.4f}", "kg/s"],
        ["Fuel flow rate", f"{m_f_d:.4f}", f"{m_f_d:.4f}", f"{m_f_d:.4f}", "kg/s"],
        [
            "Oxidizer flow rate",
            f"{m_ox_d:.4f}",
            f"{m_ox_d:.4f}",
            f"{m_ox_d:.4f}",
            "kg/s",
        ],
    ]
    output = tabulate(
        results, headers, numalign="right"
    )

    return (
        cstar_d,
        m_d,
        m_f_d,
        m_ox_d,
        Is_vac_d,
        Is_opt_d,
        Is_SL_d,
        CF_vac_d,
        CF_opt_d,
        CF_SL_d,
        T_vac_d,
        T_opt_d,
        T_SL_d,
        output,
    )


if __name__ == "__main__":
    root = tk.Tk()
    widget = PerformanceFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
