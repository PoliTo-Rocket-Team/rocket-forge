import customtkinter as ctk
import tkinter as tk
import sys, os
from rocketforge.performance import theoretical

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme.json")

appWidth, appHeight = 800, 600


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Rocket Forge")
        self.geometry(f"{appWidth}x{appHeight}")
        self.resizable(False, False)
        self.after(201, lambda :self.iconphoto(False, tk.PhotoImage(file=resource_path('icon.png'))))

        self.oxLabel = ctk.CTkLabel(self, text="Oxidizer", font=("Sans", 16))
        self.oxLabel.place(relx=0.05, rely=0.1, anchor="w")

        oxidizers = [
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
        ]
        self.oxvar = ctk.StringVar(value="LOX")
        self.oxopt = ctk.CTkOptionMenu(
            self, values=oxidizers, variable=self.oxvar, font=("Sans", 16)
        )
        self.oxopt.place(relx=0.45, rely=0.1, anchor="e")

        self.fuelLabel = ctk.CTkLabel(self, text="Fuel", font=("Sans", 16))
        self.fuelLabel.place(relx=0.55, rely=0.1, anchor="w")

        fuels = [
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
        ]
        self.fuelvar = ctk.StringVar(value="CH4")
        self.fuelopt = ctk.CTkOptionMenu(
            self, values=fuels, variable=self.fuelvar, font=("Sans", 16)
        )
        self.fuelopt.place(relx=0.95, rely=0.1, anchor="e")

        self.pcLabel = ctk.CTkLabel(
            self, text="Chamber pressure", font=("Sans", 16)
        )
        self.pcLabel.place(relx=0.05, rely=0.2, anchor="w")

        self.pcEntry = ctk.CTkEntry(self, placeholder_text="0", font=("Sans", 16), width=65)
        self.pcEntry.place(relx=0.275, rely=0.2, anchor="w")

        uom = [
            "bar",
            "Pa",
            "MPa",
            "atm",
            "psia"
        ]
        self.pcvar = ctk.StringVar(value="bar")
        self.pcopt = ctk.CTkOptionMenu(
            self, values=uom, variable=self.pcvar, font=("Sans", 16), width=75
        )
        self.pcopt.place(relx=0.45, rely=0.2, anchor="e")

        self.mrLabel = ctk.CTkLabel(self, text="Mixture Ratio", font=("Sans", 16))
        self.mrLabel.place(relx=0.05, rely=0.3, anchor="w")

        self.mrEntry = ctk.CTkEntry(self, placeholder_text="0", font=("Sans", 16))
        self.mrEntry.place(relx=0.45, rely=0.3, anchor="e")

        self.epsLabel = ctk.CTkLabel(
            self, text="Supersonic area ratio", font=("Sans", 16)
        )
        self.epsLabel.place(relx=0.05, rely=0.4, anchor="w")

        self.epsEntry = ctk.CTkEntry(self, placeholder_text="0", font=("Sans", 16))
        self.epsEntry.place(relx=0.45, rely=0.4, anchor="e")

        self.iterLabel = ctk.CTkLabel(
            self, text="Number of stations", font=("Sans", 16)
        )
        self.iterLabel.place(relx=0.55, rely=0.2, anchor="w")

        self.iterEntry = ctk.CTkEntry(self, placeholder_text="0", font=("Sans", 16))
        self.iterEntry.place(relx=0.95, rely=0.2, anchor="e")

        self.facVar = ctk.IntVar(value=False)
        self.facSwitch = ctk.CTkSwitch(
            self,
            text="Finite area combustor",
            variable=self.facVar,
            onvalue=True,
            offvalue=False,
            font=("Sans", 16),
        )
        self.facSwitch.place(relx=0.55, rely=0.3, anchor="w")

        self.epscLabel = ctk.CTkLabel(self, text="Contraction Ratio", font=("Sans", 16))
        self.epscLabel.place(relx=0.55, rely=0.4, anchor="w")

        self.epscEntry = ctk.CTkEntry(self, placeholder_text="0", font=("Sans", 16))
        self.epscEntry.place(relx=0.95, rely=0.4, anchor="e")

        self.frozenVar = ctk.IntVar(value=0)

        self.equilibriumRB = ctk.CTkRadioButton(
            self,
            text="Equilibrium",
            variable=self.frozenVar,
            value=0,
            font=("Sans", 16),
        )
        self.equilibriumRB.place(relx=0.5, rely=0.49, anchor="center")

        self.frozenRB = ctk.CTkRadioButton(
            self, text="Frozen", variable=self.frozenVar, value=1, font=("Sans", 16)
        )
        self.frozenRB.place(relx=0.45, rely=0.54, anchor="w")

        self.button = ctk.CTkButton(
            self,
            text="Generate Results",
            corner_radius=32,
            command=self.printResults,
            font=("Sans", 16),
        )
        self.button.place(relx=0.5, rely=0.61, anchor="center")

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(self, width=750, height=190, wrap="none", font=("Courier New", 12))
        else:
            self.textbox = ctk.CTkTextbox(self, width=750, height=190, wrap="none", font=("Mono", 12))
        self.textbox.place(relx=0.5, rely=0.66, anchor="n")

    def printResults(self):
        self.textbox.delete("0.0", "200.0")
        self.textbox.insert("0.0", self.computeResults())

    def computeResults(self):
        if self.facVar.get():
            try:
                epsc = float(self.epscEntry.get())
            except Exception as err:
                return err
        else:
            epsc = None

        if self.pcvar.get() == "bar":
            conv_factor = 100000
        elif self.pcvar.get() == "Pa":
            conv_factor = 1
        elif self.pcvar.get() == "MPa":
            conv_factor = 1000000
        elif self.pcvar.get() == "atm":
            conv_factor = 101325
        elif self.pcvar.get() == "psia":
            conv_factor = 6894.8

        try:
            return theoretical(
                self.oxvar.get(),
                self.fuelvar.get(),
                float(self.pcEntry.get()) * conv_factor,
                float(self.mrEntry.get()),
                float(self.epsEntry.get()),
                epsc,
                int(self.iterEntry.get()),
                self.frozenVar.get(),
            )[-2]
        except Exception as err:
            return err


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = App(className="Rocket Forge")
    app.mainloop()
