from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkButton
import math, os


class PerformanceFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(PerformanceFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False),
            text="Performance Analysis",
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.thermodynamicframe = ThermodynamicFrame(self)
        self.thermodynamicframe.configure(height=550, width=900)
        self.thermodynamicframe.place(anchor="center", relx=0.5, rely=0.6)

        self.deliveredframe = DeliveredFrame(self)
        self.deliveredframe.configure(height=550, width=900)
        self.deliveredframe.place(anchor="center", relx=0.5, rely=0.6)

        self.thermodynamicbutton = CTkButton(self, width=425)
        self.thermodynamicbutton.configure(
            text="Thermodynamic properties",
            command=lambda: self.thermodynamicframe.tkraise(),
        )
        self.thermodynamicbutton.place(anchor="w", relx=0.05, rely=0.2)

        self.deliveredbutton = CTkButton(self, width=425)
        self.deliveredbutton.configure(
            text="Delivered performance", command=lambda: self.deliveredframe.tkraise()
        )
        self.deliveredbutton.place(anchor="e", relx=0.95, rely=0.2)

        self.thermodynamicframe.tkraise()
        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def loadengine(self, ox, fuel, mr, pc, eps, geometry):
        At, Le, theta_e = geometry

        if self.thermodynamicframe.frozenflow.get() == 0:
            frozen = 0
            frozenatthroat = 0
        elif self.thermodynamicframe.frozenflow.get() == 1:
            frozen = 1
            frozenatthroat = 0
        elif self.thermodynamicframe.frozenflow.get() == 2:
            frozen = 1
            frozenatthroat = 1

        if self.thermodynamicframe.inletconditions.get() == 0:
            epsc = None
        elif self.thermodynamicframe.inletconditions.get() == 1:
            epsc = None  # TODO
        elif self.thermodynamicframe.inletconditions.get() == 2:
            epsc = float(self.thermodynamicframe.contractionentry.get())

        iter = int(self.thermodynamicframe.stationsentry.get()) + 1

        x = theoretical(ox, fuel, pc, mr, eps, epsc, iter, frozen, frozenatthroat)

        self.thermodynamicframe.textbox.configure(state="normal")
        self.thermodynamicframe.textbox.delete("0.0", "200.0")
        self.thermodynamicframe.textbox.insert("0.0", x[-1])
        self.thermodynamicframe.textbox.configure(state="disabled")

        cstar = x[0]
        Isp_vac = x[1]
        Isp_vac_eq = x[2]
        Isp_vac_frozen = x[3]
        td_properties = x[-2]

        pe = float(td_properties[0][-2]) * 100000
        Tc = float(td_properties[1][1])
        Te = float(td_properties[1][-2])
        we = float(td_properties[8][-2]) * float(td_properties[9][-2])

        if self.deliveredframe.multiphase.get() == 0:
            Z, Cs = 0, 0
        else:
            Z = float(self.deliveredframe.condmassfracentry.get())
            Cs = 0 # TODO

        z_r, z_n, z_overall, z_f, z_d, z_z = correction_factors(pc, eps, At, Le, theta_e, Isp_vac_eq, Isp_vac_frozen, Tc, Te, we, Z, Cs)

        self.deliveredframe.reactioneffentry.configure(state="normal")
        self.deliveredframe.reactioneffentry.insert("0", f"{z_r:.4f}")
        self.deliveredframe.reactioneffentry.configure(state="disabled")

        self.deliveredframe.nozzleeffentry.configure(state="normal")
        self.deliveredframe.nozzleeffentry.insert("0", f"{z_n:.4f}")
        self.deliveredframe.nozzleeffentry.configure(state="disabled")

        self.deliveredframe.overalleffentry.configure(state="normal")
        self.deliveredframe.overalleffentry.insert("0", f"{z_overall:.4f}")
        self.deliveredframe.overalleffentry.configure(state="disabled")

        self.deliveredframe.BLeffentry.configure(state="normal")
        self.deliveredframe.BLeffentry.insert("0", f"{z_f:.4f}")
        self.deliveredframe.BLeffentry.configure(state="disabled")

        self.deliveredframe.diveffentry.configure(state="normal")
        self.deliveredframe.diveffentry.insert("0", f"{z_d:.4f}")
        self.deliveredframe.diveffentry.configure(state="disabled")

        self.deliveredframe.multiphaseeffentry.configure(state="normal")
        self.deliveredframe.multiphaseeffentry.insert("0", f"{z_z:.4f}")
        self.deliveredframe.multiphaseeffentry.configure(state="disabled")

        x = delivered(pc, eps, pe, mr, At, cstar, Isp_vac, z_r, z_n)

        self.deliveredframe.textbox.configure(state="normal")
        self.deliveredframe.textbox.delete("0.0", "200.0")
        self.deliveredframe.textbox.insert("0.0", x[-1])
        self.deliveredframe.textbox.configure(state="disabled")


class ThermodynamicFrame(CTkFrame):
    def __init__(self, master=None, **kw):
        super(ThermodynamicFrame, self).__init__(master, **kw)

        self.inletconditions = ctk.IntVar(value=0)

        self.iacRB = ctk.CTkRadioButton(
            self, text="Infinite area combustor", variable=self.inletconditions, value=0
        )
        self.iacRB.place(anchor="w", relx=0.05, rely=0.1)

        self.massfluxRB = ctk.CTkRadioButton(
            self, text="Mass flux", variable=self.inletconditions, value=1
        )
        self.massfluxRB.place(anchor="w", relx=0.05, rely=0.17)

        self.massfluxentry = CTkEntry(self)
        self.massfluxentry.configure(placeholder_text="0", width=90)
        self.massfluxentry.place(anchor="w", relx=0.3, rely=0.17)

        self.massfluxoptmenu = ctk.CTkOptionMenu(self)
        self.massfluxuom = tk.StringVar(value="kg/s")
        self.massfluxoptmenu.configure(
            values=["kg/s", "lb/s"], variable=self.massfluxuom, width=90
        )
        self.massfluxoptmenu.place(anchor="w", relx=0.4, rely=0.17)

        self.contractionRB = ctk.CTkRadioButton(
            self, text="Contraction area ratio", variable=self.inletconditions, value=2
        )
        self.contractionRB.place(anchor="w", relx=0.05, rely=0.24)

        self.contractionentry = CTkEntry(self)
        self.contractionentry.configure(placeholder_text="0", width=180)
        self.contractionentry.place(anchor="w", relx=0.3, rely=0.24)

        self.frozenflow = ctk.IntVar(value=0)

        self.equilibriumRB = ctk.CTkRadioButton(
            self, text="Shifting equilibrium flow", variable=self.frozenflow, value=0
        )
        self.equilibriumRB.place(anchor="w", relx=0.65, rely=0.1)

        self.frozenRB = ctk.CTkRadioButton(
            self, text="Frozen equilibrium flow", variable=self.frozenflow, value=1
        )
        self.frozenRB.place(anchor="w", relx=0.65, rely=0.17)

        self.frozenatthroatRB = ctk.CTkRadioButton(
            self, text="Frozen at throat flow", variable=self.frozenflow, value=2
        )
        self.frozenatthroatRB.place(anchor="w", relx=0.65, rely=0.24)

        self.thermodynamiclabel = CTkLabel(self)
        self.thermodynamiclabel.configure(text="Thermodynamic properties")
        self.thermodynamiclabel.place(anchor="w", relx=0.05, rely=0.38)

        self.stationslabel = CTkLabel(self)
        self.stationslabel.configure(text="Number of stations")
        self.stationslabel.place(anchor="w", relx=0.05, rely=0.45)

        self.stationsentry = CTkEntry(self)
        self.stationsentry.configure(placeholder_text="1", width=180)
        self.stationsentry.insert("0", "1")
        self.stationsentry.place(anchor="w", relx=0.3, rely=0.45)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(
                self,
                height=220,
                state="disabled",
                wrap="none",
                font=("Courier New", 12),
            )
        else:
            self.textbox = ctk.CTkTextbox(
                self, height=220, state="disabled", wrap="none", font=("Mono", 12)
            )
        self.textbox.place(relwidth=0.9, relx=0.5, rely=0.52, anchor="n")


class DeliveredFrame(CTkFrame):
    def __init__(self, master=None, **kw):
        super(DeliveredFrame, self).__init__(master, **kw)

        self.multiphase = ctk.IntVar(value=0)

        self.multiphaseCB = ctk.CTkCheckBox(
            self,
            text="Consider multiphase flow effects",
            variable=self.multiphase,
            onvalue=1,
            offvalue=0,
        )
        self.multiphaseCB.place(anchor="w", relx=0.065, rely=0.07)

        self.condheatcapacitylabel = CTkLabel(self)
        self.condheatcapacitylabel.configure(text="Condensed phase heat capacity")
        self.condheatcapacitylabel.place(anchor="w", relx=0.1, rely=0.13)

        self.condheatcapacityentry = CTkEntry(self)
        self.condheatcapacityentry.configure(placeholder_text="0")
        self.condheatcapacityentry.place(anchor="w", relx=0.45, rely=0.13)

        self.condheatcapacityoptmenu = ctk.CTkOptionMenu(self)
        self.condheatcapacityuom = tk.StringVar(value="")
        self.condheatcapacityoptmenu.configure(
            values=["", ""], variable=self.condheatcapacityuom, width=90
        )
        self.condheatcapacityoptmenu.place(anchor="w", relx=0.61, rely=0.13)

        self.condmassfraclabel = CTkLabel(self)
        self.condmassfraclabel.configure(
            text="Mass fraction of condensed phase at nozzle exit"
        )
        self.condmassfraclabel.place(anchor="w", relx=0.1, rely=0.19)

        self.condmassfracentry = CTkEntry(self)
        self.condmassfracentry.configure(placeholder_text="0")
        self.condmassfracentry.place(anchor="w", relx=0.45, rely=0.19)

        self.reactionefflabel = CTkLabel(self)
        self.reactionefflabel.configure(text="Reaction efficiency")
        self.reactionefflabel.place(anchor="w", relx=0.05, rely=0.3)

        self.reactioneffentry = CTkEntry(self)
        self.reactioneffentry.configure(state="disabled")
        self.reactioneffentry.place(anchor="w", relx=0.29, rely=0.3)

        self.nozzleefflabel = CTkLabel(self)
        self.nozzleefflabel.configure(text="Nozzle efficiency")
        self.nozzleefflabel.place(anchor="w", relx=0.05, rely=0.37)

        self.nozzleeffentry = CTkEntry(self)
        self.nozzleeffentry.configure(state="disabled")
        self.nozzleeffentry.place(anchor="w", relx=0.29, rely=0.37)

        self.overallefflabel = CTkLabel(self)
        self.overallefflabel.configure(text="Overall efficiency")
        self.overallefflabel.place(anchor="w", relx=0.05, rely=0.44)

        self.overalleffentry = CTkEntry(self)
        self.overalleffentry.configure(state="disabled")
        self.overalleffentry.place(anchor="w", relx=0.29, rely=0.44)

        self.BLefflabel = CTkLabel(self)
        self.BLefflabel.configure(text="Boundary layer efficiency")
        self.BLefflabel.place(anchor="w", relx=0.55, rely=0.3)

        self.BLeffentry = CTkEntry(self)
        self.BLeffentry.configure(state="disabled")
        self.BLeffentry.place(anchor="w", relx=0.79, rely=0.3)

        self.divefflabel = CTkLabel(self)
        self.divefflabel.configure(text="Divergence efficiency")
        self.divefflabel.place(anchor="w", relx=0.55, rely=0.37)

        self.diveffentry = CTkEntry(self)
        self.diveffentry.configure(state="disabled")
        self.diveffentry.place(anchor="w", relx=0.79, rely=0.37)

        self.multiphaseefflabel = CTkLabel(self)
        self.multiphaseefflabel.configure(text="Multiphase flow efficiency")
        self.multiphaseefflabel.place(anchor="w", relx=0.55, rely=0.44)

        self.multiphaseeffentry = CTkEntry(self)
        self.multiphaseeffentry.configure(state="disabled")
        self.multiphaseeffentry.place(anchor="w", relx=0.79, rely=0.44)

        self.deliveredlabel = CTkLabel(self)
        self.deliveredlabel.configure(text="Estimated delivered performance")
        self.deliveredlabel.place(anchor="w", relx=0.05, rely=0.55)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(
                self,
                height=200,
                state="disabled",
                wrap="none",
                font=("Courier New", 12),
            )
        else:
            self.textbox = ctk.CTkTextbox(
                self, height=200, state="disabled", wrap="none", font=("Mono", 12)
            )
        self.textbox.place(relwidth=0.9, relx=0.5, rely=0.6, anchor="n")


def theoretical(ox, fuel, pc, mr, eps, epsc, iter, frozen, frozenatthroat):
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

    pe = pc / C.get_PcOvPe(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )

    Isp_vac = C.get_Isp(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )
    Isp_vac_eq = C.get_Isp(
        Pc=pc, MR=mr, eps=eps
    )
    Isp_vac_fr = C.get_Isp(
        Pc=pc, MR=mr, eps=eps, frozen=1
    )
    Isp_sl = C.estimate_Ambient_Isp(
        Pc=pc, MR=mr, eps=eps, Pamb=pamb, frozen=frozen, frozenAtThroat=frozenatthroat
    )[0]
    Isp_opt = C.estimate_Ambient_Isp(
        Pc=pc, MR=mr, eps=eps, Pamb=pe, frozen=frozen, frozenAtThroat=frozenatthroat
    )[0]

    c_vac = Isp_vac * 9.80655
    c_sl = Isp_sl * 9.80655
    c_opt = Isp_opt * 9.80655

    CF_opt, CF_sl, mode = C.get_PambCf(Pamb=pamb, Pc=pc, MR=mr, eps=eps)
    CF_vac = c_vac / cstar

    Tc, Tt, Te = C.get_Temperatures(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )
    rhoc, rhot, rhoe = C.get_Densities(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )

    cpc, muc, lc, Prc = C.get_Chamber_Transport(Pc=pc, MR=mr, eps=eps, frozen=frozen)

    ac, at, ae = C.get_SonicVelocities(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )
    Hc, Ht, He = C.get_Enthalpies(
        Pc=pc, MR=mr, eps=eps, frozen=frozen, frozenAtThroat=frozenatthroat
    )

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
        p.append(
            pc
            / 100000
            / C.get_PcOvPe(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )
        )
        T.append(
            C.get_Temperatures(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[2]
        )
        rho.append(
            C.get_Densities(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[2]
        )
        cp.append(
            C.get_Exit_Transport(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[0]
        )
        mu.append(
            C.get_Exit_Transport(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[1]
        )
        l.append(
            C.get_Exit_Transport(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[2]
        )
        Pr.append(
            C.get_Exit_Transport(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[3]
        )
        gamma.append(
            C.get_exit_MolWt_gamma(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[1]
        )
        M.append(
            C.get_MachNumber(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )
        )
        a.append(
            C.get_SonicVelocities(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[2]
        )
        H.append(
            C.get_Enthalpies(
                Pc=pc, MR=mr, eps=x, frozen=frozen, frozenAtThroat=frozenatthroat
            )[2]
        )

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
        Isp_vac_eq,
        Isp_vac_fr,
        results,
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
    # Coefficients from NASA SP8120 Boundary Layer Loss Recommendation
    a = 0.13956490814036465
    b = 0.4839954048378114
    c = -1.5290708783162201
    d = 1.8872208607881908
    e = 1.2281287531868839
    f = 1.1165014352424605
    g = 0.08873349847277191
    pxd = 2 * pc * rt * 0.00014503773800722 * 39.37007874
    loss = g*eps/pxd + (c + d * math.log(e + eps*f))/( a + b*math.log(pxd))
    z_f = (100.0 - loss) / 100.0

    # Nozzle correction factor
    z_n = z_f * z_d * z_z

    # Overall correction factor
    z_overall = z_n * z_r

    return z_r, z_n, z_overall, z_f, z_d, z_z


def delivered(pc, eps, pe, MR, At, cstar, Is_vac, z_c, z_n):

    pSL = 101325
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
    output = tabulate(results, headers, numalign="right")

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
