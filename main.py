#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
import os, sys
from rocketforge.initialframe   import InitialFrame
from rocketforge.performance    import PerformanceFrame
from rocketforge.thermal        import ThermalFrame
from rocketforge.geometry       import GeometryFrame
from customtkinter              import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel, CTkImage
from tkinter                    import filedialog, messagebox
from configparser               import ConfigParser
from PIL                        import Image

version = "1.0.0"
copyright = "(C) 2023-2024 Polito Rocket Team"


class RocketForge(CTk):
    def __init__(self, *args, **kwargs):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(resource_path("theme.json"))

        super().__init__(*args, **kwargs)
        self.configure(height=800, padx=5, pady=5, width=1200)
        self.resizable(False, False)
        self.title("Rocket Forge")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.after(
            201,
            lambda: self.iconphoto(
                False, tk.PhotoImage(file=resource_path("icon.png"))
            ),
        )

        # Initial data frame
        self.initialframe = InitialFrame(self)
        self.initialframe.grid(column=1, row=0)

        # Performance frame
        self.performanceframe = PerformanceFrame(self)
        self.performanceframe.grid(column=1, row=0)

        # Thermal analysis frame
        self.thermalframe = ThermalFrame(self)
        self.thermalframe.grid(column=1, row=0)

        # Geometry frame
        self.geometryframe = GeometryFrame(self)
        self.geometryframe.grid(column=1, row=0)

        # Sidebar
        self.sidebar = CTkFrame(self)
        self.sidebar.configure(border_width=5, corner_radius=0, height=750, width=200)

        self.aboutbutton = CTkButton(self.sidebar)
        self.aboutbutton.configure(
            text="About...", width=180, command=self.about_window
        )
        self.aboutbutton.place(anchor="center", relx=0.5, rely=0.95, x=0, y=0)

        self.preferencesbutton = CTkButton(self.sidebar)
        self.preferencesbutton.configure(
            text="Preferences...", width=180, command=self.preferences_window
        )
        self.preferencesbutton.place(anchor="center", relx=0.5, rely=0.90, x=0, y=0)

        self.loadbutton = CTkButton(self.sidebar)
        self.loadbutton.configure(text="Load...", width=180, command=self.load_config)
        self.loadbutton.place(anchor="center", relx=0.5, rely=0.85, x=0, y=0)

        self.savebutton = CTkButton(self.sidebar)
        self.savebutton.configure(text="Save...", width=180, command=self.save_config)
        self.savebutton.place(anchor="center", relx=0.5, rely=0.8, x=0, y=0)

        self.initialdatabutton = CTkButton(self.sidebar)
        self.initialdatabutton.configure(
            text="Initial Data", width=180, command=lambda: self.initialframe.tkraise()
        )
        self.initialdatabutton.place(anchor="center", relx=0.5, rely=0.2, x=0, y=0)

        self.performancebutton = CTkButton(self.sidebar)
        self.performancebutton.configure(
            text="Performance",
            width=180,
            command=lambda: self.performanceframe.tkraise(),
        )
        self.performancebutton.place(anchor="center", relx=0.5, rely=0.25, x=0, y=0)

        self.thermalbutton = CTkButton(self.sidebar)
        self.thermalbutton.configure(
            text="Thermal analysis",
            width=180,
            command=lambda: self.thermalframe.tkraise(),
        )
        self.thermalbutton.place(anchor="center", relx=0.5, rely=0.3, x=0, y=0)

        self.geometrybutton = CTkButton(self.sidebar)
        self.geometrybutton.configure(
            text="Geometry", width=180, command=lambda: self.geometryframe.tkraise()
        )
        self.geometrybutton.place(anchor="center", relx=0.5, rely=0.35, x=0, y=0)

        self.logoframe = CTkFrame(self.sidebar)
        self.logoframe.configure(border_width=5, height=100, width=180)
        logoimage = CTkImage(Image.open(resource_path("icon.png")), size=(90, 90))
        self.logoimage = CTkLabel(self.logoframe, text="", image=logoimage)
        self.logoimage.place(anchor="center", relx=0.3, rely=0.5)
        self.logolabel = CTkLabel(self.logoframe)
        self.logolabel.configure(
            font=CTkFont("Sans", 18, "bold", "roman", False, False),
            justify="center",
            text="Rocket\nForge",
        )
        self.logolabel.place(
            anchor="center", relx=0.7, rely=0.5, x=0, y=0
        )
        self.logoframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.sidebar.grid(column=0, row=0)

        # Status bar
        self.statusbar = CTkFrame(self)
        self.statusbar.configure(border_width=5, corner_radius=0, height=50, width=1200)
        self.runbutton = CTkButton(self.statusbar)
        self.runbutton.configure(text="Run", command=self.run)
        self.runbutton.place(anchor="e", relx=0.98, rely=0.5, x=0, y=0)
        self.statuslabel = CTkLabel(self.statusbar)
        self.statuslabel.configure(justify="right", text="Status: idle")
        self.statuslabel.place(anchor="e", relx=0.85, rely=0.5, x=0, y=0)
        self.statusbar.grid(column=0, columnspan=2, row=1)

        # Raise initial frame
        self.initialframe.tkraise()

        # Top level windows
        self.about = None
        self.preferences = None
        self.appearance_mode = tk.StringVar(value="System")

    def run(self):
        self.statuslabel.configure(text="Status: running...")
        self.statuslabel.update()
        try:
            ox, fuel, mr, pc, eps = self.initialframe.expressrun()
            geometry = self.geometryframe.loadgeometry()
        except Exception:
            geometry = (0, 0, 0)

        try:
            self.performanceframe.loadengine(ox, fuel, mr, pc, eps, geometry)
        except Exception:
            pass
        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()

    def about_window(self):
        if self.about is None or not self.about.winfo_exists():
            self.about = ctk.CTkToplevel()
            self.about.title("About")
            self.about.configure(width=300, height=200)
            self.about.resizable(False, False)
            self.about.after(
                201,
                lambda: self.about.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            aboutimage = CTkImage(Image.open(resource_path("icon.png")), size=(128, 128))
            self.aboutimage = CTkLabel(self.about, text="", image=aboutimage)
            self.aboutimage.place(anchor="center", relx=0.5, rely=0.28)
            self.aboutname = CTkLabel(self.about, text="Rocket Forge", font=("Sans", 20))
            self.aboutname.place(anchor="center", relx=0.5, rely=0.6)
            self.aboutversion = CTkLabel(self.about, text="Version "+version)
            self.aboutversion.place(anchor="center", relx=0.5, rely=0.75)
            self.copyright = CTkLabel(self.about, text=copyright)
            self.copyright.place(anchor="center", relx=0.5, rely=0.9)

            self.about.after(50, self.about.lift)
            self.about.after(50, self.about.focus)

        else:
            self.about.lift()
            self.about.focus()

    def preferences_window(self):
        if self.preferences is None or not self.preferences.winfo_exists():
            self.preferences = ctk.CTkToplevel()
            self.preferences.title("Preferences")
            self.preferences.configure(width=400, height=300)
            self.preferences.resizable(False, False)
            self.preferences.after(
                201,
                lambda: self.preferences.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.appearance_mode_label = CTkLabel(
                self.preferences, text="Appearance Mode:", anchor="w"
            )
            self.appearance_mode_label.place(anchor="w", relx=0.1, rely=0.1)
            self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
                self.preferences,
                values=["System", "Light", "Dark"],
                variable=self.appearance_mode,
                command=self.change_appearance_mode_event,
            )
            self.appearance_mode_optionemenu.place(anchor="w", relx=0.5, rely=0.1)

            self.preferences.after(50, self.preferences.lift)
            self.preferences.after(50, self.preferences.focus)

        else:
            self.preferences.lift()
            self.preferences.focus()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def on_closing(self):
        """close the program"""
        quit_ = messagebox.askokcancel(title="Exit?", message="Do you want to exit?")
        if quit_:
            sys.exit(0)

    def save_config(self):
        self.statuslabel.configure(text="Status: saving configuration file...")
        self.statuslabel.update()

        try:
            config = ConfigParser()
            config["InitialData"] = {
                "name": self.initialframe.enginenameentry.get(),
                "description": self.initialframe.description.get("1.0",'end-1c'),
                "chamber_pressure": self.initialframe.pcentry.get(),
                "chamber_pressure_uom": self.initialframe.pcuom.get(),
                "oxidizer": self.initialframe.oxvar.get(),
                "fuel": self.initialframe.fuelvar.get(),
                "mixture_ratio": self.initialframe.mrentry.get(),
                "mixture_ratio_uom": self.initialframe.mruom.get(),
                "expansion_area_ratio": self.initialframe.epsentry.get(),
                "expansion_pressure_ratio": self.initialframe.peratioentry.get(),
                "exit_pressure": self.initialframe.peentry.get(),
                "exit_pressure_uom": self.initialframe.peuom.get(),
                "exit_condition": self.initialframe.exitcondition.get(),
                "mixture_ratio_optimization": self.initialframe.optimizationmode.get(),
            }
            tf = self.performanceframe.thermodynamicframe
            df = self.performanceframe.deliveredframe
            config["Performance"] = {
                "inlet_conditions": tf.inletconditions.get(),
                "mass_flux": tf.massfluxentry.get(),
                "mass_flux_uom": tf.massfluxuom.get(),
                "contraction_ratio": tf.contractionentry.get(),
                "flow_model": tf.frozenflow.get(),
                "number_of_stations": tf.stationsentry.get(),
                "consider_multiphase": df.multiphase.get(),
                "condensed_heat_capacity": df.condheatcapacityentry.get(),
                "condensed_heat_capacity_uom": df.condheatcapacityuom.get(),
                "mass_frac_condensed": df.condmassfracentry.get(),
            }
            config["Geometry"] = {
                "throat_area": self.geometryframe.throatareaentry.get(),
                "throat_area_uom": self.geometryframe.throatareauom.get(),
                "divergent_length": self.geometryframe.divergentlengthentry.get(),
                "divergent_length_uom": self.geometryframe.divergentlengthuom.get(),
                "theta_e": self.geometryframe.thetaexentry.get(),
                "theta_e_uom": self.geometryframe.thetaexuom.get(),
            }

            with open(filedialog.asksaveasfilename(), "w") as f:
                config.write(f)

        except Exception:
            pass

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()
        

    def load_config(self):
        self.statuslabel.configure(text="Status: loading configuration file...")
        self.statuslabel.update()

        try:
            config = ConfigParser()
            config.read(filedialog.askopenfilename())

            def updateentry(entry: ctk.CTkEntry, value):
                entry.delete("0", "200")
                entry.insert("0", value)

            idf = self.initialframe

            updateentry(idf.enginenameentry, config.get("InitialData", "name"))
            idf.description.delete("0.0", "200.0")
            idf.description.insert("0.0", config.get("InitialData", "description"))
            updateentry(idf.pcentry, config.get("InitialData", "chamber_pressure"))
            idf.pcuom.set(config.get("InitialData", "chamber_pressure_uom"))
            idf.oxvar.set(config.get("InitialData", "oxidizer"))
            idf.fuelvar.set(config.get("InitialData", "fuel"))
            updateentry(idf.mrentry, config.get("InitialData", "mixture_ratio"))
            idf.mruom.set(config.get("InitialData", "mixture_ratio_uom"))
            updateentry(idf.epsentry, config.get("InitialData", "expansion_area_ratio"))
            updateentry(idf.peratioentry, config.get("InitialData", "expansion_pressure_ratio"))
            updateentry(idf.peentry, config.get("InitialData", "exit_pressure"))
            idf.peuom.set(config.get("InitialData", "exit_pressure_uom"))
            idf.exitcondition.set(config.get("InitialData", "exit_condition"))
            idf.optimizationmode.set(config.get("InitialData", "mixture_ratio_optimization"))

            tf = self.performanceframe.thermodynamicframe
            df = self.performanceframe.deliveredframe

            tf.inletconditions.set(config.get("Performance", "inlet_conditions"))
            updateentry(tf.massfluxentry, config.get("Performance", "mass_flux"))
            tf.massfluxuom.set(config.get("Performance", "mass_flux_uom"))
            updateentry(tf.contractionentry, config.get("Performance", "contraction_ratio"))
            tf.frozenflow.set(config.get("Performance", "flow_model"))
            updateentry(tf.stationsentry, config.get("Performance", "number_of_stations"))
            df.multiphase.set(config.get("Performance", "consider_multiphase"))
            updateentry(df.condheatcapacityentry, config.get("Performance", "condensed_heat_capacity"))
            df.condheatcapacityuom.set(config.get("Performance", "condensed_heat_capacity_uom"))
            updateentry(df.condmassfracentry, config.get("Performance", "mass_frac_condensed"))

            gf = self.geometryframe

            updateentry(gf.throatareaentry, config.get("Geometry", "throat_area"))
            gf.throatareauom.set(config.get("Geometry", "throat_area_uom"))
            updateentry(gf.divergentlengthentry, config.get("Geometry", "divergent_length"))
            gf.divergentlengthuom.set(config.get("Geometry", "divergent_length_uom"))
            updateentry(gf.thetaexentry, config.get("Geometry", "theta_e"))
            gf.thetaexuom.set(config.get("Geometry", "theta_e_uom"))

        except Exception:
            pass

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    RocketForge(className="Rocket Forge").mainloop()
