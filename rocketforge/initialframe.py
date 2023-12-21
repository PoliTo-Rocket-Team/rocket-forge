#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
import os, math
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu
from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate

class InitialFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(InitialFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Initial Data"
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.enginedefinitionlabel = CTkLabel(self)
        self.enginedefinitionlabel.configure(text="Engine Definition")
        self.enginedefinitionlabel.place(anchor="w", relx=0.05, rely=0.19, x=0, y=0)

        self.enginenamelabel = CTkLabel(self)
        self.enginenamelabel.configure(text="Engine name:")
        self.enginenamelabel.place(anchor="w", relx=0.05, rely=0.24, x=0, y=0)

        self.enginenameentry = CTkEntry(self)
        self.enginenameentry.configure(placeholder_text="Engine name...", width=200)
        self.enginenameentry.place(anchor="w", relx=0.2, rely=0.24, x=0, y=0)

        self.descriptionlabel = CTkLabel(self)
        self.descriptionlabel.configure(text="Engine description:")
        self.descriptionlabel.place(anchor="w", relx=0.05, rely=0.29, x=0, y=0)

        self.description = ctk.CTkTextbox(self)
        self.description.configure(
            width=750, height=66
        )
        self.description.place(anchor="nw", relx=0.2, rely=0.27, x=0, y=0)

        self.pclabel = CTkLabel(self)
        self.pclabel.configure(text="Chamber Pressure:")
        self.pclabel.place(anchor="w", relx=0.05, rely=0.39, x=0, y=0)

        self.pcentry = CTkEntry(self)
        self.pcentry.configure(placeholder_text=0, width=100)
        self.pcentry.place(anchor="w", relx=0.2, rely=0.39, x=0, y=0)

        self.pcoptmenu = CTkOptionMenu(self)
        self.pcuom = tk.StringVar(value="bar")
        self.pcoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.pcuom, width=100
        )
        self.pcoptmenu.place(anchor="w", relx=0.3, rely=0.39, x=0, y=0)

        self.propellantlabel = CTkLabel(self)
        self.propellantlabel.configure(text="Propellant Specification")
        self.propellantlabel.place(anchor="w", relx=0.05, rely=0.47, x=0, y=0)

        self.oxidizerlabel = CTkLabel(self)
        self.oxidizerlabel.configure(text="Oxidizer:")
        self.oxidizerlabel.place(anchor="w", relx=0.05, rely=0.52, x=0, y=0)

        self.oxoptmenu = CTkOptionMenu(self)
        self.oxvar = tk.StringVar(value="LOX")
        self.oxoptmenu.configure(
            values=[
                "LOX",
                "MON3",
                "MON10",
                "N2O4",
                "N2O3",
                "AIR",
                "F2",
                "GOX",
                "HNO3",
                "N2F4",
                "IRFNA",
            ],
            variable=self.oxvar,
            width=200,
        )
        self.oxoptmenu.place(anchor="w", relx=0.2, rely=0.52, x=0, y=0)

        self.fuellabel = CTkLabel(self)
        self.fuellabel.configure(text="Fuel:")
        self.fuellabel.place(anchor="w", relx=0.05, rely=0.57, x=0, y=0)

        self.fueloptmenu = CTkOptionMenu(self)
        self.fuelvar = tk.StringVar(value="CH4")
        self.fueloptmenu.configure(
            values=[
                "LH2",
                "CH4",
                "MMH",
                "CH3OH",
                "JetA",
                "UDMH",
                "H2O",
                "GH2",
                "M20",
                "RP1",
                "C2H2",
                "N2H4",
                "Methanol",
                "Propane",
                "HTPB",
            ],
            variable=self.fuelvar,
            width=200,
        )
        self.fueloptmenu.place(anchor="w", relx=0.2, rely=0.57, x=0, y=0)

        self.mrlabel = CTkLabel(self)
        self.mrlabel.configure(text="Mixture Ratio:")
        self.mrlabel.place(anchor="w", relx=0.05, rely=0.62, x=0, y=0)

        self.mrentry = CTkEntry(self)
        self.mrentry.configure(placeholder_text="0", width=100)
        self.mrentry.place(anchor="w", relx=0.2, rely=0.62, x=0, y=0)

        self.mroptmenu = CTkOptionMenu(self)
        self.mruom = tk.StringVar(value="O/F")
        self.mroptmenu.configure(
            values=["O/F", "alpha"], variable=self.mruom, width=100
        )
        self.mroptmenu.place(anchor="w", relx=0.3, rely=0.62, x=0, y=0)

        self.exitcondlabel = CTkLabel(self)
        self.exitcondlabel.configure(text="Nozzle exit condition")
        self.exitcondlabel.place(anchor="w", relx=0.55, rely=0.47, x=0, y=0)

        self.exitcondition = ctk.IntVar(value=0)

        self.epsRB = ctk.CTkRadioButton(
            self,
            text="Expansion area ratio",
            variable=self.exitcondition,
            value=0,
        )
        self.epsRB.place(anchor="w", relx=0.55, rely=0.52)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(placeholder_text=0, width=200)
        self.epsentry.place(anchor="w", relx=0.75, rely=0.52, x=0, y=0)

        self.peratioRB = ctk.CTkRadioButton(
            self,
            text="Expansion pressure ratio",
            variable=self.exitcondition,
            value=1,
        )
        self.peratioRB.place(anchor="w", relx=0.55, rely=0.57)

        self.peratioentry = CTkEntry(self)
        self.peratioentry.configure(placeholder_text=0, width=200)
        self.peratioentry.place(anchor="w", relx=0.75, rely=0.57, x=0, y=0)

        self.peRB = ctk.CTkRadioButton(
            self,
            text="Exit Pressure",
            variable=self.exitcondition,
            value=2,
        )
        self.peRB.place(anchor="w", relx=0.55, rely=0.62)

        self.peentry = CTkEntry(self)
        self.peentry.configure(placeholder_text=0, width=100)
        self.peentry.place(anchor="w", relx=0.75, rely=0.62, x=0, y=0)

        self.peoptmenu = CTkOptionMenu(self)
        self.peuom = tk.StringVar(value="bar")
        self.peoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.peuom, width=100
        )
        self.peoptmenu.place(anchor="w", relx=0.85, rely=0.62, x=0, y=0)

        self.theoreticallabel = CTkLabel(self)
        self.theoreticallabel.configure(text="Theoretical (ideal) performance")
        self.theoreticallabel.place(anchor="w", relx=0.05, rely=0.7, x=0, y=0)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(self, width=850, height=175, state="disabled", wrap="none", font=("Courier New", 12))
        else:
            self.textbox = ctk.CTkTextbox(self, width=850, height=175, state="disabled", wrap="none", font=("Mono", 12))
        self.textbox.place(relwidth=.9, relx=0.05, rely=0.73, anchor="nw")

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def expressrun(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "200.0")
        self.textbox.insert("0.0", self.computeResults())
        self.textbox.configure(state="disabled")

    def computeResults(self):

        pamb = 101325

        try:
            C = CEA_Obj(
                oxName=self.oxoptmenu.get(),
                fuelName=self.fueloptmenu.get(),
                fac_CR=None,
                cstar_units="m/s",
                pressure_units="Pa",
                temperature_units="K",
                sonic_velocity_units="m/s",
                enthalpy_units="kJ/kg",
                density_units="kg/m^3",
                specific_heat_units="J/kg-K",
            )

            pc = float(self.pcentry.get()) * convert_pressure_uom(self.pcuom.get())
            mr_s = C.getMRforER(ERphi=1)

            if self.mruom.get() == "O/F":
                mr = float(self.mrentry.get())
                alpha = mr / mr_s
            elif self.mruom.get() == "alpha":
                alpha = float(self.mrentry.get())
                mr = alpha * mr_s

            cstar = C.get_Cstar(Pc=pc, MR=mr)

            if self.exitcondition.get() == 0:
                eps = float(self.epsentry.get())
                pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)
            elif self.exitcondition.get() == 1:
                eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=float(self.peratioentry.get()))
                pe = pc / float(self.peratioentry.get())
            elif self.exitcondition.get() == 2:
                pe = float(self.peentry.get()) * convert_pressure_uom(self.peuom.get())
                eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=pc/pe)

            Isp_vac = C.get_Isp(Pc=pc, MR=mr, eps=eps)
            Isp_sl = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pamb)[0]
            Isp_opt = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pe)[0]

            c_vac = Isp_vac * 9.80655
            c_sl = Isp_sl * 9.80655
            c_opt = Isp_opt * 9.80655

            CF_opt, CF_sl, mode = C.get_PambCf(Pamb=pamb, Pc=pc, MR=mr, eps=eps)
            CF_vac = c_vac / cstar
        except Exception as err:
            return err

        headers = ["Parameter", "Sea level", "Optimum", "Vacuum", "Unit"]
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
        output1 = tabulate(results, headers, numalign="right", tablefmt="plain")

        results = [
            ["Expansion Area Ratio", eps, ""],
            ["Expansion pressure ratio", pc/pe, ""],
            ["Exit Pressure", pe/100000, "bar"],
            ["Mixture Ratio", mr, ""],
            ["Mixture Ratio (stoichiometric)", mr_s, ""],
            ["Alpha (oxidizer excess coefficient)", alpha, ""],
        ]
        output2 = tabulate(results, numalign="right", tablefmt="plain", floatfmt=".4f")

        return output1 + 2 * "\n" + output2

        
def convert_pressure_uom(uom: str) -> float:
    uoms = {
        "Pa": 1,
        "MPa": 1000000,
        "bar": 100000,
        "atm": 101325,
        "psia": 6894.8
    }
    return uoms[uom]


if __name__ == "__main__":
    root = tk.Tk()
    widget = InitialFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
