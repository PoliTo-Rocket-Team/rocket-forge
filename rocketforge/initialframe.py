#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
import os
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu


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

        self.enginenamelabel = CTkLabel(self)
        self.enginenamelabel.configure(text="Engine name:")
        self.enginenamelabel.place(anchor="w", relx=0.05, rely=0.25, x=0, y=0)

        self.enginenameentry = CTkEntry(self)
        self.enginenameentry.configure(placeholder_text="Engine name...", width=200)
        self.enginenameentry.place(anchor="w", relx=0.2, rely=0.25, x=0, y=0)

        self.enginedescriptionlabel = CTkLabel(self)
        self.enginedescriptionlabel.configure(text="Engine description:")
        self.enginedescriptionlabel.place(anchor="w", relx=0.05, rely=0.3, x=0, y=0)

        self.enginedescriptionentry = CTkEntry(self)
        self.enginedescriptionentry.configure(
            placeholder_text="Engine description...", width=750
        )
        self.enginedescriptionentry.place(anchor="w", relx=0.2, rely=0.3, x=0, y=0)

        self.enginedefinitionlabel = CTkLabel(self)
        self.enginedefinitionlabel.configure(text="Engine Definition")
        self.enginedefinitionlabel.place(anchor="w", relx=0.05, rely=0.2, x=0, y=0)

        self.pclabel = CTkLabel(self)
        self.pclabel.configure(text="Chamber Pressure:")
        self.pclabel.place(anchor="w", relx=0.05, rely=0.35, x=0, y=0)

        self.pcentry = CTkEntry(self)
        self.pcentry.configure(placeholder_text=0, width=100)
        self.pcentry.place(anchor="w", relx=0.2, rely=0.35, x=0, y=0)

        self.pcoptmenu = CTkOptionMenu(self)
        self.pcuom = tk.StringVar(value="bar")
        self.pcoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.pcuom, width=100
        )
        self.pcoptmenu.place(anchor="w", relx=0.3, rely=0.35, x=0, y=0)

        self.propellantlabel = CTkLabel(self)
        self.propellantlabel.configure(text="Propellant Specification")
        self.propellantlabel.place(anchor="w", relx=0.05, rely=0.45, x=0, y=0)

        self.oxidizerlabel = CTkLabel(self)
        self.oxidizerlabel.configure(text="Oxidizer:")
        self.oxidizerlabel.place(anchor="w", relx=0.05, rely=0.5, x=0, y=0)

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
        self.oxoptmenu.place(anchor="w", relx=0.2, rely=0.5, x=0, y=0)

        self.fuellabel = CTkLabel(self)
        self.fuellabel.configure(text="Fuel:")
        self.fuellabel.place(anchor="w", relx=0.05, rely=0.55, x=0, y=0)

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
        self.fueloptmenu.place(anchor="w", relx=0.2, rely=0.55, x=0, y=0)

        self.mrlabel = CTkLabel(self)
        self.mrlabel.configure(text="Mixture Ratio:")
        self.mrlabel.place(anchor="w", relx=0.05, rely=0.6, x=0, y=0)

        self.mrentry = CTkEntry(self)
        self.mrentry.configure(placeholder_text="0", width=100)
        self.mrentry.place(anchor="w", relx=0.2, rely=0.6, x=0, y=0)

        self.mroptmenu = CTkOptionMenu(self)
        self.mruom = tk.StringVar(value="O/F")
        self.mroptmenu.configure(
            values=["O/F", "alpha"], variable=self.mruom, width=100
        )
        self.mroptmenu.place(anchor="w", relx=0.3, rely=0.6, x=0, y=0)

        self.exitcondlabel = CTkLabel(self)
        self.exitcondlabel.configure(text="Nozzle exit condition")
        self.exitcondlabel.place(anchor="w", relx=0.55, rely=0.45, x=0, y=0)

        self.exitcondition = ctk.IntVar(value=1)

        self.peRB = ctk.CTkRadioButton(
            self,
            text="Pressure",
            variable=self.exitcondition,
            value=0,
        )
        self.peRB.place(anchor="w", relx=0.55, rely=0.5)

        self.peentry = CTkEntry(self)
        self.peentry.configure(placeholder_text=0, width=100)
        self.peentry.place(anchor="w", relx=0.75, rely=0.5, x=0, y=0)

        self.peoptmenu = CTkOptionMenu(self)
        self.peuom = tk.StringVar(value="bar")
        self.peoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.peuom, width=100
        )
        self.peoptmenu.place(anchor="w", relx=0.85, rely=0.5, x=0, y=0)

        self.epsRB = ctk.CTkRadioButton(
            self,
            text="Expansion area ratio",
            variable=self.exitcondition,
            value=1,
        )
        self.epsRB.place(anchor="w", relx=0.55, rely=0.55)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(placeholder_text=0, width=200)
        self.epsentry.place(anchor="w", relx=0.75, rely=0.55, x=0, y=0)

        self.peratioRB = ctk.CTkRadioButton(
            self,
            text="Expansion pressure ratio",
            variable=self.exitcondition,
            value=2,
        )
        self.peratioRB.place(anchor="w", relx=0.55, rely=0.6)

        self.peratioentry = CTkEntry(self)
        self.peratioentry.configure(placeholder_text=0, width=200)
        self.peratioentry.place(anchor="w", relx=0.75, rely=0.6, x=0, y=0)

        self.theoreticallabel = CTkLabel(self)
        self.theoreticallabel.configure(text="Theoretical (ideal) performance")
        self.theoreticallabel.place(anchor="w", relx=0.05, rely=0.7, x=0, y=0)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(self, width=850, height=175, wrap="none", font=("Courier New", 12))
        else:
            self.textbox = ctk.CTkTextbox(self, width=850, height=175, wrap="none", font=("Mono", 12))
        self.textbox.place(relwidth=.9, relx=0.05, rely=0.73, anchor="nw")

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)


if __name__ == "__main__":
    root = tk.Tk()
    widget = InitialFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
