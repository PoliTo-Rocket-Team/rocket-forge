import tkinter as tk
import customtkinter as ctk
import os
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu
from tabulate import tabulate
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketforge.utils.conversions import pressure_uom
from rocketforge.utils.helpers import updatetextbox
from rocketforge.performance.mixtureratio import optimizemr, optimizermr_at_pe
from rocketforge.performance.theoreticalperf import theoretical


class InitialFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(InitialFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Engine Definition")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.enginenamelabel = CTkLabel(self)
        self.enginenamelabel.configure(text="Engine name")
        self.enginenamelabel.place(anchor="w", relx=0.02, rely=0.11, x=0, y=0)

        self.enginenameentry = CTkEntry(self)
        self.enginenameentry.configure(placeholder_text="Engine name...", width=118)
        self.enginenameentry.place(anchor="e", relx=0.48, rely=0.11, x=0, y=0)

        self.pclabel = CTkLabel(self)
        self.pclabel.configure(text="Chamber Pressure")
        self.pclabel.place(anchor="w", relx=0.02, rely=0.18, x=0, y=0)

        self.pcentry = CTkEntry(self)
        self.pcentry.configure(placeholder_text=0, width=59)
        self.pcentry.place(anchor="e", relx=229/600, rely=0.18, x=0, y=0)

        self.pcoptmenu = CTkOptionMenu(self)
        self.pcuom = tk.StringVar(value="bar")
        self.pcoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.pcuom, width=59
        )
        self.pcoptmenu.place(anchor="e", relx=0.48, rely=0.18, x=0, y=0)

        self.oxidizerlabel = CTkLabel(self)
        self.oxidizerlabel.configure(text="Oxidizer")
        self.oxidizerlabel.place(anchor="w", relx=0.02, rely=0.25, x=0, y=0)

        self.oxoptmenu = CTkOptionMenu(self)
        self.oxvar = tk.StringVar(value="LOX")
        self.oxoptmenu.configure(
            values=[
                "90_H2O2",
                "98_H2O2",
                "AIR",
                "AIRSIMP",
                "CLF3",
                "CLF5",
                "F2",
                "GO2",
                "GOX",
                "H2O",
                "H2O2",
                "HAN315",
                "HNO3",
                "IRFNA",
                "LO2",
                "LO2_NASA",
                "LOX",
                "MON15",
                "MON25",
                "MON3",
                "N2F4",
                "N2H4",
                "N2O",
                "N2O3",
                "N2O4",
                "N2O_nbp",
                "O2",
                "OF2",
                "Peroxide90",
                "Peroxide98",
            ],
            variable=self.oxvar,
            width=118,
        )
        self.oxoptmenu.place(anchor="e", relx=0.48, rely=0.25, x=0, y=0)

        self.fuellabel = CTkLabel(self)
        self.fuellabel.configure(text="Fuel")
        self.fuellabel.place(anchor="w", relx=0.02, rely=0.32, x=0, y=0)

        self.fueloptmenu = CTkOptionMenu(self)
        self.fuelvar = tk.StringVar(value="CH4")
        self.fueloptmenu.configure(
            values=[
                "A50",
                "Acetylene",
                "AL",
                "AP",
                "B2H6",
                "C2H2",
                "C2H5OH",
                "C2H6",
                "C2H6_167",
                "C3H8",
                "CFx",
                "CH3OH",
                "CH4",
                "CINCH",
                "DMAZ",
                "ECP_dimer",
                "Ethanol",
                "ETHANOL",
                "Gasoline",
                "GCH4",
                "GH2",
                "GH2_160",
                "H2",
                "H2O",
                "HTPB",
                "Isopropanol",
                "JetA",
                "JP10",
                "JP4",
                "JPX",
                "Kerosene",
                "Kerosene90_H2O10",
                "LCH4_NASA",
                "LH2",
                "LH2_NASA",
                "M20",
                "M20_NH3",
                "Methanol",
                "METHANOL",
                "MHF3",
                "MMH",
                "N2H4",
                "NH3",
                "NITROMETHANE",
                "Propane",
                "Propylene",
                "propylene",
                "RP1",
                "RP1_NASA",
                "RP_1",
                "UDMH",
            ],
            variable=self.fuelvar,
            width=118,
        )
        self.fueloptmenu.place(anchor="e", relx=0.48, rely=0.32, x=0, y=0)

        self.mrlabel = CTkLabel(self)
        self.mrlabel.configure(text="Mixture Ratio")
        self.mrlabel.place(anchor="w", relx=0.02, rely=0.39, x=0, y=0)

        self.mrentry = CTkEntry(self)
        self.mrentry.configure(placeholder_text="0", width=59)
        self.mrentry.place(anchor="e", relx=229/600, rely=0.39, x=0, y=0)

        self.mroptmenu = CTkOptionMenu(self)
        self.mruom = tk.StringVar(value="O/F")
        self.mroptmenu.configure(
            values=["O/F", "alpha"], variable=self.mruom, width=59
        )
        self.mroptmenu.place(anchor="e", relx=0.48, rely=0.39, x=0, y=0)

        self.exitcondlabel = CTkLabel(self)
        self.exitcondlabel.configure(text="Nozzle exit condition")
        self.exitcondlabel.place(anchor="w", relx=0.02, rely=0.46, x=0, y=0)

        self.exitcondition = ctk.IntVar(value=2)

        self.epsRB = ctk.CTkRadioButton(
            self,
            text="Expansion area ratio",
            variable=self.exitcondition,
            value=0,
        )
        self.epsRB.place(anchor="w", relx=0.01, rely=0.6)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(placeholder_text=0, width=118)
        self.epsentry.place(anchor="e", relx=0.48, rely=0.6, x=0, y=0)

        self.peratioRB = ctk.CTkRadioButton(
            self,
            text="Pressure ratio (pc/pe)",
            variable=self.exitcondition,
            value=1,
        )
        self.peratioRB.place(anchor="w", relx=0.01, rely=0.67)

        self.peratioentry = CTkEntry(self)
        self.peratioentry.configure(placeholder_text=0, width=118)
        self.peratioentry.place(anchor="e", relx=0.48, rely=0.67, x=0, y=0)

        self.peRB = ctk.CTkRadioButton(
            self,
            text="Exit Pressure",
            variable=self.exitcondition,
            value=2,
        )
        self.peRB.place(anchor="w", relx=0.01, rely=0.53)

        self.peentry = CTkEntry(self)
        self.peentry.configure(placeholder_text=0, width=59)
        self.peentry.place(anchor="e", relx=229/600, rely=0.53, x=0, y=0)

        self.peoptmenu = CTkOptionMenu(self)
        self.peuom = tk.StringVar(value="bar")
        self.peoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.peuom, width=59
        )
        self.peoptmenu.place(anchor="e", relx=0.48, rely=0.53, x=0, y=0)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(
                self,
                height=90,
                state="disabled",
                wrap="none",
                font=("Courier New", 12),
            )
        else:
            self.textbox = ctk.CTkTextbox(
                self, height=90, state="disabled", wrap="none", font=("Mono", 12)
            )
        self.textbox.place(relwidth=0.98, relx=0.01, rely=0.79, anchor="nw")

        self.optimizationlabel = CTkLabel(self)
        self.optimizationlabel.configure(text="Mixture ratio optimization")
        self.optimizationlabel.place(anchor="w", relx=0.52, rely=0.11, x=0, y=0)

        self.optimizationmode = ctk.IntVar(value=0)

        self.nooptimizationRB = ctk.CTkRadioButton(
            self,
            text="Use input mixture ratio",
            variable=self.optimizationmode,
            value=0,
        )
        self.nooptimizationRB.place(anchor="w", relx=0.51, rely=0.18)

        self.peratioRB = ctk.CTkRadioButton(
            self,
            text="Maximize vacuum specific impulse",
            variable=self.optimizationmode,
            value=1,
        )
        self.peratioRB.place(anchor="w", relx=0.51, rely=0.25)

        self.peRB = ctk.CTkRadioButton(
            self,
            text="Maximize adapted specific impulse",
            variable=self.optimizationmode,
            value=2,
        )
        self.peRB.place(anchor="w", relx=0.51, rely=0.32)

        self.peRB = ctk.CTkRadioButton(
            self,
            text="Maximize sea level specific impulse",
            variable=self.optimizationmode,
            value=3,
        )
        self.peRB.place(anchor="w", relx=0.51, rely=0.39)

        self.inletcondition = ctk.IntVar(value=0)

        self.nozinletlabel = CTkLabel(self)
        self.nozinletlabel.configure(text="Nozzle inlet condition")
        self.nozinletlabel.place(anchor="w", relx=0.52, rely=0.46, x=0, y=0)

        self.epscRB = ctk.CTkRadioButton(
            self,
            text="Contraction area ratio",
            variable=self.inletcondition,
            value=0,
        )
        self.epscRB.place(anchor="w", relx=0.51, rely=0.53, x=0, y=0)

        self.epscentry = CTkEntry(self)
        self.epscentry.configure(placeholder_text="0", width=118)
        self.epscentry.place(anchor="e", relx=0.98, rely=0.53, x=0, y=0)

        self.massfluxRB = ctk.CTkRadioButton(
            self,
            text="Mass flow rate (TODO)",
            variable=self.inletcondition,
            value=1,
        )
        self.massfluxRB.place(anchor="w", relx=0.51, rely=0.6, x=0, y=0)

        self.infepscRB = ctk.CTkRadioButton(
            self,
            text="Infinite area combustor",
            variable=self.inletcondition,
            value=2,
        )
        self.infepscRB.place(anchor="w", relx=0.51, rely=0.67, x=0, y=0)

        self.thrustlabel = CTkLabel(self)
        self.thrustlabel.configure(text="Nominal thrust (TODO)")
        self.thrustlabel.place(anchor="w", relx=0.02, rely=0.74, x=0, y=0)

        self.thrustentry = CTkEntry(self)
        self.thrustentry.configure(placeholder_text="0", width=59)
        self.thrustentry.place(anchor="e", relx=229/600, rely=0.74, x=0, y=0)

        self.thrustoptmenu = CTkOptionMenu(self)
        self.thrustuom = tk.StringVar(value="kN")
        self.thrustoptmenu.configure(
            values=["MN", "kN", "N", "kgf", "lbf"], variable=self.thrustuom, width=59
        )
        self.thrustoptmenu.place(anchor="e", relx=0.48, rely=0.74, x=0, y=0)

        self.thrustlabel2 = CTkLabel(self)
        self.thrustlabel2.configure(text="at ambient pressure")
        self.thrustlabel2.place(anchor="w", relx=0.49, rely=0.74, x=0, y=0)

        self.thrustentry2 = CTkEntry(self)
        self.thrustentry2.configure(placeholder_text="0", width=59)
        self.thrustentry2.place(anchor="e", relx=469/600, rely=0.74, x=0, y=0)

        self.thrustoptmenu2 = CTkOptionMenu(self)
        self.thrustuom2 = tk.StringVar(value="bar")
        self.thrustoptmenu2.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.thrustuom2, width=59
        )
        self.thrustoptmenu2.place(anchor="e", relx=0.88, rely=0.74, x=0, y=0)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def expressrun(self):
        try: 
            ox = self.oxoptmenu.get()
            fuel = self.fueloptmenu.get()
            pc = float(self.pcentry.get()) * pressure_uom(self.pcuom.get())
            if self.inletcondition.get() == 0:
                epsc = float(self.epscentry.get())
            else:
                epsc = None

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

            mr_s = C.getMRforER(ERphi=1)

            if self.optimizationmode.get() == 0:
                if self.mruom.get() == "O/F":
                    mr = float(self.mrentry.get())
                    alpha = mr / mr_s
                elif self.mruom.get() == "alpha":
                    alpha = float(self.mrentry.get())
                    mr = alpha * mr_s

                if self.exitcondition.get() == 0:
                    eps = float(self.epsentry.get())
                    pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)
                elif self.exitcondition.get() == 1:
                    eps = C.get_eps_at_PcOvPe(
                        Pc=pc, MR=mr, PcOvPe=float(self.peratioentry.get())
                    )
                    pe = pc / float(self.peratioentry.get())
                elif self.exitcondition.get() == 2:
                    pe = float(self.peentry.get()) * pressure_uom(self.peuom.get())
                    eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=pc / pe)

            elif self.exitcondition.get() == 0:
                eps = float(self.epsentry.get())
                mr = optimizemr(C, pc, eps, self.optimizationmode.get())
                alpha = mr / mr_s
                pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)

            else:
                if self.exitcondition.get() == 1:
                    pe = pc / float(self.peratioentry.get())
                elif self.exitcondition.get() == 2:
                    pe = float(self.peentry.get()) * pressure_uom(self.peuom.get())
                mr = optimizermr_at_pe(C, pc, pe, self.optimizationmode.get())
                eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=pc / pe)
                alpha = mr / mr_s

            results = [
                ["Expansion Area Ratio", eps, ""],
                ["Expansion pressure ratio", pc / pe, ""],
                ["Exit Pressure", pe / 100000, "bar"],
                ["Mixture Ratio", mr, ""],
                ["Mixture Ratio (stoichiometric)", mr_s, ""],
                ["Alpha (oxidizer excess coefficient)", alpha, ""],
            ]
            output2 = tabulate(results, numalign="right", tablefmt="plain", floatfmt=".3f")
            output1 = theoretical(ox, fuel, pc, mr, eps)[-3]
            output = output1 + 2 * "\n" + output2
        except Exception as err:
            output = str(err)

        updatetextbox(self.textbox, output, True)

        return ox, fuel, pc, mr, eps, epsc