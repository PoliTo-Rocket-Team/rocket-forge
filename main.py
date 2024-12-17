import tkinter as tk
import customtkinter as ctk
import rocketforge.performance.config as conf
import rocketforge.thermal.config as tconf
from rocketforge.gui.initialframe   import InitialFrame
from rocketforge.gui.performance    import PerformanceFrame
from rocketforge.gui.geometry       import GeometryFrame
from rocketforge.gui.nested         import NestedFrame
from rocketforge.gui.thermal        import ThermalFrame
from rocketforge.gui.tanks          import TanksFrame
from rocketforge.gui.mission        import MissionFrame
from rocketforge.utils.resources    import resource_path
from rocketforge.utils.helpers      import updateentry, updatetextbox
from customtkinter                  import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel, CTkImage
from tkinter                        import filedialog, messagebox
from configparser                   import ConfigParser
from PIL                            import Image

version = "1.0.0"
copyright = "(C) 2023-2024 Polito Rocket Team"


class RocketForge(CTk):
    def __init__(self, *args, **kwargs):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(resource_path("theme.json"))

        super().__init__(*args, **kwargs)
        self.withdraw()
        self.configure(height=480, padx=0, pady=0, width=720)
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

        # Geometry frame
        self.geometryframe = GeometryFrame(self)
        self.geometryframe.grid(column=1, row=0)

        # Nested analysis frame
        self.nestedframe = NestedFrame(self)
        self.nestedframe.grid(column=1, row=0)

        # Thermal analysis frame
        self.thermalframe = ThermalFrame(self)
        self.thermalframe.grid(column=1, row=0)

        # Tanks design frame
        self.tanksframe = TanksFrame(self)
        self.tanksframe.grid(column=1, row=0)

        # Mission analysis frame
        self.missionframe = MissionFrame(self)
        self.missionframe.grid(column=1, row=0)

        # Sidebar
        self.sidebar = CTkFrame(self)
        self.sidebar.configure(border_width=1, corner_radius=0, height=480, width=120)

        self.aboutbutton = CTkButton(self.sidebar)
        self.aboutbutton.configure(
            text="About...", width=110, command=self.about_window
        )
        self.aboutbutton.place(anchor="center", relx=0.5, rely=0.96, x=0, y=0)

        self.preferencesbutton = CTkButton(self.sidebar)
        self.preferencesbutton.configure(
            text="Preferences...", width=110, command=self.preferences_window
        )
        self.preferencesbutton.place(anchor="center", relx=0.5, rely=0.89, x=0, y=0)

        self.loadbutton = CTkButton(self.sidebar)
        self.loadbutton.configure(text="Load...", width=110, command=self.load_config)
        self.loadbutton.place(anchor="center", relx=0.5, rely=0.82, x=0, y=0)

        self.savebutton = CTkButton(self.sidebar)
        self.savebutton.configure(text="Save...", width=110, command=self.save_config)
        self.savebutton.place(anchor="center", relx=0.5, rely=0.75, x=0, y=0)

        self.initialdatabutton = CTkButton(self.sidebar)
        self.initialdatabutton.configure(
            text="Engine Definition", width=110, command=lambda: self.initialframe.tkraise()
        )
        self.initialdatabutton.place(anchor="center", relx=0.5, rely=0.04, x=0, y=0)

        self.performancebutton = CTkButton(self.sidebar)
        self.performancebutton.configure(
            text="Performance",
            width=110,
            command=lambda: self.performanceframe.tkraise(),
        )
        self.performancebutton.place(anchor="center", relx=0.5, rely=0.11, x=0, y=0)

        self.geometrybutton = CTkButton(self.sidebar)
        self.geometrybutton.configure(
            text="Geometry", width=110, command=lambda: self.geometryframe.tkraise()
        )
        self.geometrybutton.place(anchor="center", relx=0.5, rely=0.18, x=0, y=0)

        self.nestedbutton = CTkButton(self.sidebar)
        self.nestedbutton.configure(
            text="Nested Analysis",
            width=110,
            command=lambda: self.nestedframe.tkraise(),
        )
        self.nestedbutton.place(anchor="center", relx=0.5, rely=0.25, x=0, y=0)

        self.thermalbutton = CTkButton(self.sidebar)
        self.thermalbutton.configure(
            text="Thermal Analysis",
            width=110,
            command=lambda: self.thermalframe.tkraise(),
        )
        self.thermalbutton.place(anchor="center", relx=0.5, rely=0.32, x=0, y=0)

        self.tanksbutton = CTkButton(self.sidebar)
        self.tanksbutton.configure(
            text="Tanks Design",
            width=110,
            command=lambda: self.tanksframe.tkraise(),
        )
        self.tanksbutton.place(anchor="center", relx=0.5, rely=0.39, x=0, y=0)

        self.missionbutton = CTkButton(self.sidebar)
        self.missionbutton.configure(
            text="Mission Analysis",
            width=110,
            command=lambda: self.missionframe.tkraise(),
        )
        self.missionbutton.place(anchor="center", relx=0.5, rely=0.46, x=0, y=0)

        self.sidebar.grid(column=0, row=0)

        # Status bar
        self.statusbar = CTkFrame(self)
        self.statusbar.configure(border_width=1, corner_radius=0, height=32, width=720)
        self.runbutton = CTkButton(self.statusbar)
        self.runbutton.configure(text="Run", command=self.run)
        self.runbutton.place(anchor="e", relx=0.99, rely=0.5, x=0, y=0)
        self.statuslabel = CTkLabel(self.statusbar)
        self.statuslabel.configure(justify="right", text="Status: idle")
        self.statuslabel.place(anchor="e", relx=0.77, rely=0.5, x=0, y=0)
        self.statusbar.grid(column=0, columnspan=2, row=1)

        # Raise initial frame
        self.initialframe.tkraise()

        # Top level windows
        self.about = None
        self.preferences = None
        self.appearance_mode = tk.StringVar(value="System")

        self.update()
        self.deiconify()

    def run(self):
        self.statuslabel.configure(text="Status: starting...")
        self.statuslabel.update()

        if tconf.regen:
            try:
                self.statuslabel.configure(text="Status: loading regenerative cooling...")
                self.statuslabel.update()
                self.thermalframe.load_regen_cooling()
            except Exception:
                self.thermalframe.regenvar.set(False)
                self.thermalframe.toggle_regen_cooling()
        
        if tconf.rad:
            try:
                self.statuslabel.configure(text="Status: loading radiation cooling...")
                self.statuslabel.update()
                self.thermalframe.load_rad_cooling()
            except Exception:
                self.thermalframe.radvar.set(False)
                self.thermalframe.toggle_rad_cooling()

        if tconf.film:
            try:
                self.statuslabel.configure(text="Status: loading film cooling...")
                self.statuslabel.update()
                self.thermalframe.load_film_cooling()
            except Exception:
                self.thermalframe.filmvar.set(False)
                self.thermalframe.toggle_film_cooling()

        try:
            self.statuslabel.configure(text="Status: running...")
            self.statuslabel.update()
            self.initialframe.run()
        except Exception:
            pass

        try:
            self.statuslabel.configure(text="Status: computing geometry...")
            self.statuslabel.update()
            self.geometryframe.estimate_Tn()
            self.geometryframe.plot()
        except Exception:
            pass

        try:
            self.statuslabel.configure(text="Status: computing performance...")
            self.statuslabel.update()
            self.performanceframe.run()
            self.estimate_At()
        except Exception:
            pass

        try:
            self.statuslabel.configure(text="Status: performing thermal analysis...")
            self.statuslabel.update()
            self.thermalframe.run()
        except Exception:
            self.thermalframe.regenvar.set(False)
            self.thermalframe.toggle_regen_cooling()
            self.thermalframe.radvar.set(False)
            self.thermalframe.toggle_rad_cooling()
            self.thermalframe.filmvar.set(False)
            self.thermalframe.toggle_film_cooling()

        try: 
            self.statuslabel.configure(text="Status: loading tanks...")
            self.statuslabel.update()
            self.tanksframe.compute()
        except Exception:
            pass

        try:
            self.statuslabel.configure(text="Status: running flight simulation...")
            self.statuslabel.update()
            self.missionframe.run()
        except Exception:
            pass

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()

    def estimate_At(self):
        if conf.thrust is not None:
            while abs((conf.thrust_d - conf.thrust)/conf.thrust_d) > 0.01:
                self.geometryframe.estimate_Tn()
                self.geometryframe.plot()
                self.performanceframe.run()
                conf.At = conf.thrust * conf.k_film / conf.CF_d / conf.pc

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
            self.preferences.configure(width=300, height=80)
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
            self.appearance_mode_label.place(anchor="w", relx=0.05, rely=0.5)
            self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
                self.preferences,
                values=["System", "Light", "Dark"],
                variable=self.appearance_mode,
                command=self.change_appearance_mode_event,
            )
            self.appearance_mode_optionemenu.place(anchor="e", relx=0.95, rely=0.5)

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
            self.destroy()

    def save_config(self):
        self.statuslabel.configure(text="Status: saving configuration file...")
        self.statuslabel.update()

        try:
            config = ConfigParser()
            config["InitialData"] = {
                "name": self.initialframe.enginenameentry.get(),
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
                "inlet_conditions": self.initialframe.inletcondition.get(),
                "contraction_ratio": self.initialframe.epscentry.get(),
                "thrust": self.initialframe.thrustentry.get(),
                "thrust_uom": self.initialframe.thrustuom.get(),
                "ambient_pressure": self.initialframe.thrustentry2.get(),
                "ambient_pressure_uom": self.initialframe.thrustuom2.get(),
            }
            tf = self.performanceframe.thermodynamicframe
            config["Performance"] = {
                "flow_model": tf.frozenflow.get(),
                "number_of_stations": tf.stationsentry.get(),
            }
            gf = self.geometryframe
            config["Geometry"] = {
                "throat_area": gf.throatareaentry.get(),
                "throat_area_uom": gf.throatareauom.get(),
                "shape": gf.shape.get(),
                "divergent_length": gf.divergentlengthentry.get(),
                "divergent_length_uom": gf.divergentlengthuom.get(),
                "theta_e": gf.thetaexentry.get(),
                "theta_e_uom": gf.thetaexuom.get(),
                "rnovrt": gf.rnovrtentry.get(),
                "theta_n": gf.thetanentry.get(),
                "theta_n_uom": gf.thetanuom.get(),
                "r1ovrt": gf.r1ovrtentry.get(),
                "chamber_length": gf.chamberlengthentry.get(),
                "chamber_length_uom": gf.chamberlengthuom.get(),
                "contraction_angle": gf.bentry.get(),
                "contraction_angle_uom": gf.buom.get(),
                "r2ovr2max": gf.r2ovr2maxentry.get(),
                "cselected": gf.cselected.get(),
                "cle": gf.cleentry.get(),
                "cle_uom": gf.cleuom.get(),
                "clf": gf.clfentry.get(),
                "ctheta": gf.cthetaentry.get(),
                "ctheta_uom": gf.cthetauom.get(),
            }
            ttf = self.tanksframe
            config["Tanks"] = {
                "mass_flow_rate": ttf.mdotentry.get(),
                "mass_flow_rate_uom": ttf.mdotuom.get(),
                "prop_mass": ttf.mpentry.get(),
                "prop_mass_uom": ttf.mpuom.get(),
                "mixture_ratio": ttf.mrentry.get(),
                "k0": ttf.k0entry.get(),
                "k0_uom": ttf.k0uom.get(),
                "kt": ttf.ktentry.get(),
                "rho_ox": ttf.oxrhoentry.get(),
                "rho_ox_uom": ttf.oxrhouom.get(),
                "r_ox": ttf.oxrentry.get(),
                "r_ox_uom": ttf.oxruom.get(),
                "exc_ox": ttf.oxexcentry.get(),
                "pos_ox": ttf.oxxentry.get(),
                "pos_ox_uom": ttf.oxxuom.get(),
                "rho_fuel": ttf.fuelrhoentry.get(),
                "rho_fuel_uom": ttf.fuelrhouom.get(),
                "r_fuel": ttf.fuelrentry.get(),
                "r_fuel_uom": ttf.fuelruom.get(),
                "exc_fuel": ttf.fuelexcentry.get(),
                "pos_fuel": ttf.fuelxentry.get(),
                "pos_fuel_uom":ttf.fuelxuom.get(),
            }

            with open(filedialog.asksaveasfilename(defaultextension=".rf"), "w") as f:
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
            config.read(filedialog.askopenfilename(title="Load configuration file", filetypes=(("Rocket Forge files", "*.rf"), ("all files", "*.*"))))

            idf = self.initialframe

            updateentry(idf.enginenameentry, config.get("InitialData", "name"))
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
            idf.inletcondition.set(config.get("InitialData", "inlet_conditions"))
            updateentry(idf.epscentry, config.get("InitialData", "contraction_ratio"))
            updateentry(idf.thrustentry, config.get("InitialData", "thrust"))
            idf.thrustuom.set(config.get("InitialData", "thrust_uom"))
            updateentry(idf.thrustentry2, config.get("InitialData", "ambient_pressure"))
            idf.thrustuom2.set(config.get("InitialData", "ambient_pressure_uom"))

            tf = self.performanceframe.thermodynamicframe

            tf.frozenflow.set(config.get("Performance", "flow_model"))
            updateentry(tf.stationsentry, config.get("Performance", "number_of_stations"))

            gf = self.geometryframe

            gf.shape.set(config.get("Geometry", "shape"))
            gf.change_shape(config.get("Geometry", "shape"))

            updateentry(gf.throatareaentry, config.get("Geometry", "throat_area"))
            gf.throatareauom.set(config.get("Geometry", "throat_area_uom"))
            updateentry(gf.divergentlengthentry, config.get("Geometry", "divergent_length"))
            gf.divergentlengthuom.set(config.get("Geometry", "divergent_length_uom"))
            updateentry(gf.thetaexentry, config.get("Geometry", "theta_e"))
            gf.thetaexuom.set(config.get("Geometry", "theta_e_uom"))
            updateentry(gf.thetanentry, config.get("Geometry", "theta_n"))
            gf.thetanuom.set(config.get("Geometry", "theta_n_uom"))
            updateentry(gf.rnovrtentry, config.get("Geometry", "rnovrt"))
            updateentry(gf.r1ovrtentry, config.get("Geometry", "r1ovrt"))
            updateentry(gf.r2ovr2maxentry, config.get("Geometry", "r2ovr2max"))
            updateentry(gf.chamberlengthentry, config.get("Geometry", "chamber_length"))
            gf.chamberlengthuom.set(config.get("Geometry", "chamber_length_uom"))
            updateentry(gf.bentry, config.get("Geometry", "contraction_angle"))
            gf.buom.set(config.get("Geometry", "contraction_angle_uom"))
            gf.cselected.set(config.get("Geometry", "cselected"))
            updateentry(gf.cleentry, config.get("Geometry", "cle"))
            gf.cleuom.set(config.get("Geometry", "cle_uom"))
            updateentry(gf.clfentry, config.get("Geometry", "clf"))
            updateentry(gf.cthetaentry, config.get("Geometry", "ctheta"))
            gf.cthetauom.set(config.get("Geometry", "ctheta_uom"))

            ttf = self.tanksframe

            updateentry(ttf.mdotentry, config.get("Tanks", "mass_flow_rate"))
            ttf.mdotuom.set(config.get("Tanks", "mass_flow_rate_uom"))
            updateentry(ttf.mpentry, config.get("Tanks", "prop_mass"))
            ttf.mpuom.set(config.get("Tanks", "prop_mass_uom"))
            updateentry(ttf.mrentry, config.get("Tanks", "mixture_ratio"))
            updateentry(ttf.k0entry, config.get("Tanks", "k0"))
            ttf.k0uom.set(config.get("Tanks", "k0_uom"))
            updateentry(ttf.ktentry, config.get("Tanks", "kt"))
            updateentry(ttf.oxrhoentry, config.get("Tanks", "rho_ox"))
            ttf.oxrhouom.set(config.get("Tanks", "rho_ox_uom"))
            updateentry(ttf.oxrentry, config.get("Tanks", "r_ox"))
            ttf.oxruom.set(config.get("Tanks", "r_ox_uom"))
            updateentry(ttf.oxexcentry, config.get("Tanks", "exc_ox"))
            updateentry(ttf.oxxentry, config.get("Tanks", "pos_ox"))
            ttf.oxxuom.set(config.get("Tanks", "pos_ox_uom"))
            updateentry(ttf.fuelrhoentry, config.get("Tanks", "rho_fuel"))
            ttf.fuelrhouom.set(config.get("Tanks", "rho_fuel_uom"))
            updateentry(ttf.fuelrentry, config.get("Tanks", "r_fuel"))
            ttf.fuelruom.set(config.get("Tanks", "r_fuel_uom"))
            updateentry(ttf.fuelexcentry, config.get("Tanks", "exc_fuel"))
            updateentry(ttf.fuelxentry, config.get("Tanks", "pos_fuel"))
            ttf.fuelxuom.set(config.get("Tanks", "pos_fuel_uom"))

        except Exception:
            pass

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()


if __name__ == "__main__":
    RocketForge(className="Rocket Forge").mainloop()
