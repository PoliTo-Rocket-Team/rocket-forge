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
from rocketforge.utils.helpers      import update_entry, update_textbox
from rocketforge.utils.logger       import logger
from customtkinter                  import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel, CTkImage
from tkinter                        import filedialog, messagebox
from configparser                   import ConfigParser
from PIL                            import Image

version = "1.0.0"
copyright = "(C) 2023-2024 Polito Rocket Team"


class RocketForge(CTk):
    def __init__(self, *args, **kwargs):
        logger.info("Starting Rocket Forge.")
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
                False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
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

        self.savebutton = CTkButton(self.sidebar)
        self.savebutton.configure(text="Save...", width=110, command=self.save_config)
        self.savebutton.place(anchor="center", relx=0.5, rely=0.89, x=0, y=0)

        self.loadbutton = CTkButton(self.sidebar)
        self.loadbutton.configure(text="Load...", width=110, command=self.load_config)
        self.loadbutton.place(anchor="center", relx=0.5, rely=0.82, x=0, y=0)

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
        self.statusbar = CTkFrame(
            self, border_width=1, corner_radius=0, height=32, width=720
        )

        CTkButton(
            self.statusbar, text="Run", command=self.run
        ).place(anchor="e", relx=0.99, rely=0.5)

        if self._get_appearance_mode() == "light":
            appearance_image = CTkImage(Image.open(resource_path("rocketforge/resources/moon.png")), size=(20, 20))
        else:
            appearance_image = CTkImage(Image.open(resource_path("rocketforge/resources/sun.png")), size=(20, 20))

        self.appearance_button = CTkButton(
            self.statusbar,
            command=self.toggle_appearance_mode,
            width=25,
            corner_radius=5,
            text="",
            image=appearance_image,
            fg_color="transparent",
            text_color=["gray10", "gray95"],
            hover_color=["gray95", "gray10"]
        )
        self.appearance_button.place(anchor="w", relx=0.01, rely=0.5)

        self.statuslabel = CTkLabel(
            self.statusbar, justify="right", text="Status: idle"
        )
        self.statuslabel.place(anchor="e", relx=0.77, rely=0.5)
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
        logger.info("Starting analysis.")
        self.statuslabel.configure(text="Status: starting...")
        self.statuslabel.update()

        try:
            logger.info("Running engine definition frame.")
            self.statuslabel.configure(text="Status: running...")
            self.statuslabel.update()
            self.initialframe.run()
            logger.info("Engine definition completed.")
        except Exception:
            logger.error("Failed to run engine definition.")

        try:
            logger.info("Loading regenerative cooling.")
            self.statuslabel.configure(text="Status: loading regenerative cooling...")
            self.statuslabel.update()
            self.thermalframe.load_regen_cooling()
            logger.info("Regenerative cooling loaded.")
        except Exception:
            logger.error("Could not load regenerative cooling.")
            self.thermalframe.regenvar.set(False)
            self.thermalframe.toggle_regen_cooling()

        try:
            logger.info("Loading radiation cooling.")
            self.statuslabel.configure(text="Status: loading radiation cooling...")
            self.statuslabel.update()
            self.thermalframe.load_rad_cooling()
            logger.info("Radiation cooling loaded.")
        except Exception:
            logger.warning("Could not load radiation cooling.")
            self.thermalframe.radvar.set(False)
            self.thermalframe.toggle_rad_cooling()

        try:
            logger.info("Loading film cooling.")
            self.statuslabel.configure(text="Status: loading film cooling...")
            self.statuslabel.update()
            self.thermalframe.load_film_cooling()
            logger.info("Film cooling loaded.")
        except Exception:
            logger.warning("Could not load film cooling.")
            self.thermalframe.filmvar.set(False)
            self.thermalframe.toggle_film_cooling()

        try:
            logger.info("Computing geometry.")
            self.statuslabel.configure(text="Status: computing geometry...")
            self.statuslabel.update()
            self.geometryframe.estimate_Tn()
            self.geometryframe.plot()
            logger.info("Geometry computed.")
        except Exception:
            logger.error("Failed to compute geometry.")

        try:
            logger.info("Computing performance.")
            self.statuslabel.configure(text="Status: computing performance...")
            self.statuslabel.update()
            self.performanceframe.run()
            self.estimate_At()
            logger.info("Performance computed.")
        except Exception:
            logger.error("Failed to compute performance.")

        try:
            logger.info("Running nested analysis.")
            self.statuslabel.configure(text="Status: running nested analysis...")
            self.statuslabel.update()
            self.nestedframe.run()
            logger.info("Nested analysis completed.")
        except Exception:
            logger.error("Failed to run nested analysis.")

        try:
            logger.info("Performing thermal analysis.")
            self.statuslabel.configure(text="Status: performing thermal analysis...")
            self.statuslabel.update()
            self.thermalframe.run()
            logger.info("Thermal analysis completed.")
        except Exception:
            logger.error("Failed to perform thermal analysis.")
            self.thermalframe.regenvar.set(False)
            self.thermalframe.toggle_regen_cooling()
            self.thermalframe.radvar.set(False)
            self.thermalframe.toggle_rad_cooling()
            self.thermalframe.filmvar.set(False)
            self.thermalframe.toggle_film_cooling()

        try: 
            logger.info("Loading tanks.")
            self.statuslabel.configure(text="Status: loading tanks...")
            self.statuslabel.update()
            self.tanksframe.compute()
            logger.info("Tanks loaded.")
        except Exception:
            logger.error("Could not load tanks.")

        try:
            logger.info("Running mission analysis.")
            self.statuslabel.configure(text="Status: running flight simulation...")
            self.statuslabel.update()
            self.missionframe.run()
            logger.info("Mission analysis completed.")
        except Exception:
            logger.error("Failed to run mission analysis.")

        logger.info("Analysis completed.")
        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()

    def estimate_At(self):
        if conf.thrust is not None:
            logger.info("Estimating throat area.")
            while abs((conf.thrust_d - conf.thrust)/conf.thrust_d) > 0.01:
                self.geometryframe.estimate_Tn()
                self.geometryframe.plot()
                self.performanceframe.run()
                conf.At = conf.thrust * conf.k_film / conf.CF_d / conf.pc
            logger.info("Throat area estimated.")

    def about_window(self):
        if self.about is None or not self.about.winfo_exists():
            self.about = ctk.CTkToplevel()
            self.about.title("About")
            self.about.configure(width=260, height=250)
            self.about.resizable(False, False)
            self.about.after(
                201,
                lambda: self.about.iconphoto(
                    False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
                ),
            )

            self.aboutframe = CTkFrame(
                self.about, border_width=3, corner_radius=0, width=260, height=250,
            )
            self.aboutframe.grid(column=0, row=0)

            if self._get_appearance_mode() == "light":
                logo = CTkImage(Image.open(resource_path("rocketforge/resources/logo_dark.png")), size=(100, 100))
            else:
                logo = CTkImage(Image.open(resource_path("rocketforge/resources/logo.png")), size=(100, 100))
            icon = CTkImage(Image.open(resource_path("rocketforge/resources/icon.png")), size=(128, 128))
            self.logo = CTkLabel(
                self.aboutframe, text="", image=logo
            )
            self.logo.place(anchor="center", relx=0.3, y=70)
            CTkLabel(
                self.aboutframe, text="", image=icon
            ).place(anchor="center", relx=0.7, y=70)
            CTkLabel(
                self.aboutframe, text="Rocket Forge", font=("Sans", 20)
            ).place(anchor="center", relx=0.5, y=135)
            CTkLabel(
                self.aboutframe, text="Version " + version
            ).place(anchor="center", relx=0.5, y=158)
            CTkLabel(
                self.aboutframe, text=copyright
            ).place(anchor="center", relx=0.5, y=180)
            CTkLabel(
                self.aboutframe, text=(
                "Main author: Alessio Improta\n"
                + "alessio.improta@studenti.polito.it"
                )
            ).place(anchor="center", relx=0.5, rely=0.88)

            self.about.after(50, self.about.lift)
            self.about.after(50, self.about.focus)

        else:
            self.about.lift()
            self.about.focus()

    def toggle_appearance_mode(self):
        if self._get_appearance_mode() == "dark":
            new_mode = "light"
            self.appearance_button.configure(image=CTkImage(Image.open(resource_path("rocketforge/resources/moon.png")), size=(20, 20)))
        else:
            new_mode = "dark"
            self.appearance_button.configure(image=CTkImage(Image.open(resource_path("rocketforge/resources/sun.png")), size=(20, 20)))
        ctk.set_appearance_mode(new_mode)
        self.update_about_window_logo()

    def update_about_window_logo(self):
        if self.about is None or not self.about.winfo_exists():
            pass
        else:
            if self._get_appearance_mode() == "light":
                logo = CTkImage(Image.open(resource_path("rocketforge/resources/logo_dark.png")), size=(100, 100))
            else:
                logo = CTkImage(Image.open(resource_path("rocketforge/resources/logo.png")), size=(100, 100))
            self.logo.configure(image=logo)

    def on_closing(self):
        """close the program"""
        quit_ = messagebox.askokcancel(title="Exit?", message="Do you want to exit?")
        if quit_:
            logger.info("Exiting Rocket Forge.")
            self.destroy()

    def save_config(self):
        logger.info("Saving configuration file.")
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
            thf = self.thermalframe
            config["Thermal"] = {
                "enable_regen": thf.regenvar.get(),
                "coolant": thf.coolant.get(),
                "coolant_flow_rate": thf.mdotcentry.get(),
                "coolant_flow_rate_uom": thf.mdotcuom.get(),
                "coolant_Ti": thf.tcientry.get(),
                "coolant_Ti_uom": thf.tciuom.get(),
                "coolant_pi": thf.pcientry.get(),
                "coolant_pi_uom": thf.pciuom.get(),
                "pressure_drops": thf.dp.get(),
                "inner_wall": thf.tentry.get(),
                "inner_wall_uom": thf.tuom.get(),
                "wall_conductivity": thf.kentry.get(),
                "number_of_channels": tconf.NC,
                "channels_ac": tconf.a1,
                "channels_at": tconf.a2,
                "channels_ae": tconf.a3,
                "channels_bc": tconf.b1,
                "channels_bt": tconf.b2,
                "channels_be": tconf.b3,
                "adv_pinj/pc": tconf.pcoOvpc,
                "adv_stations": tconf.n_stations,
                "adv_max_iter": tconf.max_iter,
                "adv_tuning": tconf.tuning_factor,
                "adv_stability": tconf.stability,
                "adv_abs_roughness": tconf.absolute_roughness,
                "adv_friction_method": tconf.dp_method,
                "enable_rad": thf.radvar.get(),
                "eps_w": thf.radepsentry.get(),
                "enable_film": thf.filmvar.get(),
                "fuel_film": thf.fuelfilm.get(),
                "ox_film": thf.oxfilm.get(),
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
            logger.info("Configuration file saved.")

        except Exception:
            logger.error("Failed to save configuration file.")

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()
        
    def load_config(self):
        logger.info("Loading configuration file.")
        self.statuslabel.configure(text="Status: loading configuration file...")
        self.statuslabel.update()

        try:
            config = ConfigParser()
            config.read(filedialog.askopenfilename(title="Load configuration file", filetypes=(("Rocket Forge files", "*.rf"), ("all files", "*.*"))))

            idf = self.initialframe

            update_entry(idf.enginenameentry, config.get("InitialData", "name"))
            update_entry(idf.pcentry, config.get("InitialData", "chamber_pressure"))
            idf.pcuom.set(config.get("InitialData", "chamber_pressure_uom"))
            idf.oxvar.set(config.get("InitialData", "oxidizer"))
            idf.fuelvar.set(config.get("InitialData", "fuel"))
            update_entry(idf.mrentry, config.get("InitialData", "mixture_ratio"))
            idf.mruom.set(config.get("InitialData", "mixture_ratio_uom"))
            update_entry(idf.epsentry, config.get("InitialData", "expansion_area_ratio"))
            update_entry(idf.peratioentry, config.get("InitialData", "expansion_pressure_ratio"))
            update_entry(idf.peentry, config.get("InitialData", "exit_pressure"))
            idf.peuom.set(config.get("InitialData", "exit_pressure_uom"))
            idf.exitcondition.set(config.get("InitialData", "exit_condition"))
            idf.optimizationmode.set(config.get("InitialData", "mixture_ratio_optimization"))
            idf.inletcondition.set(config.get("InitialData", "inlet_conditions"))
            update_entry(idf.epscentry, config.get("InitialData", "contraction_ratio"))
            update_entry(idf.thrustentry, config.get("InitialData", "thrust"))
            idf.thrustuom.set(config.get("InitialData", "thrust_uom"))
            update_entry(idf.thrustentry2, config.get("InitialData", "ambient_pressure"))
            idf.thrustuom2.set(config.get("InitialData", "ambient_pressure_uom"))

            tf = self.performanceframe.thermodynamicframe

            tf.frozenflow.set(config.get("Performance", "flow_model"))
            update_entry(tf.stationsentry, config.get("Performance", "number_of_stations"))

            gf = self.geometryframe

            gf.shape.set(config.get("Geometry", "shape"))
            gf.change_shape(config.get("Geometry", "shape"))

            update_entry(gf.throatareaentry, config.get("Geometry", "throat_area"))
            gf.throatareauom.set(config.get("Geometry", "throat_area_uom"))
            update_entry(gf.divergentlengthentry, config.get("Geometry", "divergent_length"))
            gf.divergentlengthuom.set(config.get("Geometry", "divergent_length_uom"))
            update_entry(gf.thetaexentry, config.get("Geometry", "theta_e"))
            gf.thetaexuom.set(config.get("Geometry", "theta_e_uom"))
            update_entry(gf.thetanentry, config.get("Geometry", "theta_n"))
            gf.thetanuom.set(config.get("Geometry", "theta_n_uom"))
            update_entry(gf.rnovrtentry, config.get("Geometry", "rnovrt"))
            update_entry(gf.r1ovrtentry, config.get("Geometry", "r1ovrt"))
            update_entry(gf.r2ovr2maxentry, config.get("Geometry", "r2ovr2max"))
            update_entry(gf.chamberlengthentry, config.get("Geometry", "chamber_length"))
            gf.chamberlengthuom.set(config.get("Geometry", "chamber_length_uom"))
            update_entry(gf.bentry, config.get("Geometry", "contraction_angle"))
            gf.buom.set(config.get("Geometry", "contraction_angle_uom"))
            gf.cselected.set(config.get("Geometry", "cselected"))
            update_entry(gf.cleentry, config.get("Geometry", "cle"))
            gf.cleuom.set(config.get("Geometry", "cle_uom"))
            update_entry(gf.clfentry, config.get("Geometry", "clf"))
            update_entry(gf.cthetaentry, config.get("Geometry", "ctheta"))
            gf.cthetauom.set(config.get("Geometry", "ctheta_uom"))

            thf = self.thermalframe
            thf.regenvar.set(config.get("Thermal", "enable_regen"))
            thf.coolant.set(config.get("Thermal", "coolant"))
            update_entry(thf.mdotcentry, config.get("Thermal", "coolant_flow_rate"))
            thf.mdotcuom.set(config.get("Thermal", "coolant_flow_rate_uom"))
            update_entry(thf.tcientry, config.get("Thermal", "coolant_Ti"))
            thf.tciuom.set(config.get("Thermal", "coolant_Ti_uom"))
            update_entry(thf.pcientry, config.get("Thermal", "coolant_pi"))
            thf.pciuom.set(config.get("Thermal", "coolant_pi_uom"))
            thf.dp.set(config.get("Thermal", "pressure_drops"))
            update_entry(thf.tentry, config.get("Thermal", "inner_wall"))
            thf.tuom.set(config.get("Thermal", "inner_wall_uom"))
            update_entry(thf.kentry, config.get("Thermal", "wall_conductivity"))
            tconf.NC = int(float(config.get("Thermal", "number_of_channels")))
            tconf.a1 = float(config.get("Thermal", "channels_ac"))
            tconf.a2 = float(config.get("Thermal", "channels_at"))
            tconf.a3 = float(config.get("Thermal", "channels_ae"))
            tconf.b1 = float(config.get("Thermal", "channels_bc"))
            tconf.b2 = float(config.get("Thermal", "channels_bt"))
            tconf.b3 = float(config.get("Thermal", "channels_be"))
            tconf.pcoOvpc = float(config.get("Thermal", "adv_pinj/pc"))
            tconf.n_stations = int(float(config.get("Thermal", "adv_stations")))
            tconf.max_iter = int(float(config.get("Thermal", "adv_max_iter")))
            tconf.tuning_factor = float(config.get("Thermal", "adv_tuning"))
            tconf.stability = float(config.get("Thermal", "adv_stability"))
            tconf.absolute_roughness = float(config.get("Thermal", "adv_abs_roughness"))
            tconf.dp_method = int(float(config.get("Thermal", "adv_friction_method")))
            thf.radvar.set(config.get("Thermal", "enable_rad"))
            update_entry(thf.radepsentry, config.get("Thermal", "eps_w"))
            thf.filmvar.set(config.get("Thermal", "enable_film"))
            update_entry(thf.fuelfilm, config.get("Thermal", "fuel_film"))
            update_entry(thf.oxfilm, config.get("Thermal", "ox_film"))

            ttf = self.tanksframe

            update_entry(ttf.mdotentry, config.get("Tanks", "mass_flow_rate"))
            ttf.mdotuom.set(config.get("Tanks", "mass_flow_rate_uom"))
            update_entry(ttf.mpentry, config.get("Tanks", "prop_mass"))
            ttf.mpuom.set(config.get("Tanks", "prop_mass_uom"))
            update_entry(ttf.mrentry, config.get("Tanks", "mixture_ratio"))
            update_entry(ttf.k0entry, config.get("Tanks", "k0"))
            ttf.k0uom.set(config.get("Tanks", "k0_uom"))
            update_entry(ttf.ktentry, config.get("Tanks", "kt"))
            update_entry(ttf.oxrhoentry, config.get("Tanks", "rho_ox"))
            ttf.oxrhouom.set(config.get("Tanks", "rho_ox_uom"))
            update_entry(ttf.oxrentry, config.get("Tanks", "r_ox"))
            ttf.oxruom.set(config.get("Tanks", "r_ox_uom"))
            update_entry(ttf.oxexcentry, config.get("Tanks", "exc_ox"))
            update_entry(ttf.oxxentry, config.get("Tanks", "pos_ox"))
            ttf.oxxuom.set(config.get("Tanks", "pos_ox_uom"))
            update_entry(ttf.fuelrhoentry, config.get("Tanks", "rho_fuel"))
            ttf.fuelrhouom.set(config.get("Tanks", "rho_fuel_uom"))
            update_entry(ttf.fuelrentry, config.get("Tanks", "r_fuel"))
            ttf.fuelruom.set(config.get("Tanks", "r_fuel_uom"))
            update_entry(ttf.fuelexcentry, config.get("Tanks", "exc_fuel"))
            update_entry(ttf.fuelxentry, config.get("Tanks", "pos_fuel"))
            ttf.fuelxuom.set(config.get("Tanks", "pos_fuel_uom"))
            logger.info("Configuration file loaded.")

        except Exception:
            logger.error("Failed to load configuration file.")

        self.statuslabel.configure(text="Status: idle")
        self.statuslabel.update()


if __name__ == "__main__":
    RocketForge(className="Rocket Forge").mainloop()
