import tkinter as tk
import customtkinter as ctk
import rocketforge.performance.config as conf
import rocketforge.utils.config as config
from rocketforge.gui.initialframe   import InitialFrame
from rocketforge.gui.performance    import PerformanceFrame
from rocketforge.gui.geometry       import GeometryFrame
from rocketforge.gui.nested         import NestedFrame
from rocketforge.gui.thermal        import ThermalFrame
from rocketforge.gui.tanks          import TanksFrame
from rocketforge.gui.mission        import MissionFrame
from rocketforge.utils.resources    import resource_path
from customtkinter                  import CTk, CTkButton, CTkFrame, CTkLabel, CTkImage
from tkinter                        import messagebox
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
        self.statuslabel.configure(text="Status: starting...")
        self.statuslabel.update()

        try:
            self.statuslabel.configure(text="Status: running...")
            self.statuslabel.update()
            self.initialframe.run()
        except Exception:
            pass

        try:
            self.statuslabel.configure(text="Status: loading regenerative cooling...")
            self.statuslabel.update()
            self.thermalframe.load_regen_cooling()
        except Exception:
            self.thermalframe.regenvar.set(False)
            self.thermalframe.toggle_regen_cooling()

        try:
            self.statuslabel.configure(text="Status: loading radiation cooling...")
            self.statuslabel.update()
            self.thermalframe.load_rad_cooling()
        except Exception:
            self.thermalframe.radvar.set(False)
            self.thermalframe.toggle_rad_cooling()

        try:
            self.statuslabel.configure(text="Status: loading film cooling...")
            self.statuslabel.update()
            self.thermalframe.load_film_cooling()
        except Exception:
            self.thermalframe.filmvar.set(False)
            self.thermalframe.toggle_film_cooling()

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
            self.statuslabel.configure(text="Status: running nested analysis...")
            self.statuslabel.update()
            self.nestedframe.run()
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
            iter = 0
            while abs(conf.thrust_d - conf.thrust) > 1.0e-5 * conf.thrust_d:
                iter += 1
                conf.At = conf.thrust * conf.k_film / conf.CF_d / conf.pc
                self.geometryframe.estimate_Tn()
                self.geometryframe.plot()
                self.performanceframe.run()
                if iter == 10:
                    break

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
            self.destroy()

    def save_config(self):
        config.save_config(self)
        
    def load_config(self):
        config.load_config(self)

if __name__ == "__main__":
    RocketForge(className="Rocket Forge").mainloop()
