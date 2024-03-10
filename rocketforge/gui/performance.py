import tkinter as tk
import customtkinter as ctk
import os
from customtkinter          import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkButton
from rocketforge.performance.theoreticalperf  import theoretical
from rocketforge.performance.corrfactors      import correction_factors
from rocketforge.performance.deliveredperf    import delivered
from rocketforge.utils.helpers                import updateentry, updatetextbox


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
        self.thermodynamicframe.place(anchor="center", relx=0.5, rely=0.59)

        self.deliveredframe = DeliveredFrame(self)
        self.deliveredframe.configure(height=550, width=900)
        self.deliveredframe.place(anchor="center", relx=0.5, rely=0.59)

        self.thermodynamicbutton = CTkButton(self, width=450)
        self.thermodynamicbutton.configure(
            text="Thermodynamic properties", command=lambda: self.switchtab(1),
        )
        self.thermodynamicbutton.place(anchor="w", relx=0.05, rely=0.2)

        self.deliveredbutton = CTkButton(self, width=450)
        self.deliveredbutton.configure(
            text="Delivered performance", command=lambda: self.switchtab(0),
            fg_color=["gray55","gray25"], hover_color=["gray50","gray20"]
        )
        self.deliveredbutton.place(anchor="e", relx=0.95, rely=0.2)

        self.on = self.thermodynamicbutton.cget("fg_color")
        self.on_hover = self.thermodynamicbutton.cget("hover_color")
        self.off = self.deliveredbutton.cget("fg_color")
        self.off_hover = self.deliveredbutton.cget("hover_color")
        self.thermodynamicframe.tkraise()
        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def switchtab(self, t):
        if t == 0:
            self.deliveredframe.tkraise()
            self.deliveredbutton.configure(
                fg_color=self.on, hover_color=self.on_hover,
            )
            self.thermodynamicbutton.configure(
                fg_color=self.off, hover_color=self.off_hover,
            )
        else:
            self.thermodynamicframe.tkraise()
            self.deliveredbutton.configure(
                fg_color=self.off, hover_color=self.off_hover,
            )
            self.thermodynamicbutton.configure(
                fg_color=self.on, hover_color=self.on_hover,
            )

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

        updatetextbox(self.thermodynamicframe.textbox, x[-1], True)

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

        updateentry(self.deliveredframe.reactioneffentry, z_r, True)
        updateentry(self.deliveredframe.nozzleeffentry, z_n, True)
        updateentry(self.deliveredframe.overalleffentry, z_overall, True)
        updateentry(self.deliveredframe.BLeffentry, z_f, True)
        updateentry(self.deliveredframe.diveffentry, z_d, True)
        updateentry(self.deliveredframe.multiphaseeffentry, z_z, True)

        output = delivered(pc, eps, pe, mr, At, cstar, Isp_vac, z_r, z_n)

        updatetextbox(self.deliveredframe.textbox, output, True)


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