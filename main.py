#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
import os, sys
from rocketforge.initialframe   import InitialFrame
from rocketforge.performance    import PerformanceFrame
from rocketforge.thermal        import ThermalFrame
from rocketforge.geometry       import GeometryFrame
from customtkinter              import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel, CTkImage
from PIL                        import Image

version = "1.0.0"
copyright = "(C) 2023-2024 Polito Rocket Team"


class RocketForge:
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(resource_path("theme.json"))

        ctk1 = CTk(className="Rocket Forge")
        ctk1.configure(height=800, padx=5, pady=5, width=1200)
        ctk1.resizable(False, False)
        ctk1.title("Rocket Forge")
        ctk1.protocol("WM_DELETE_WINDOW", self.on_closing)
        ctk1.after(
            201,
            lambda: ctk1.iconphoto(
                False, tk.PhotoImage(file=resource_path("icon.png"))
            ),
        )

        # Initial data frame
        self.initialframe = InitialFrame(ctk1)
        self.initialframe.grid(column=1, row=0)

        # Performance frame
        self.performanceframe = PerformanceFrame(ctk1)
        self.performanceframe.grid(column=1, row=0)

        # Thermal analysis frame
        self.thermalframe = ThermalFrame(ctk1)
        self.thermalframe.grid(column=1, row=0)

        # Geometry frame
        self.geometryframe = GeometryFrame(ctk1)
        self.geometryframe.grid(column=1, row=0)

        # Sidebar
        self.sidebar = CTkFrame(ctk1)
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
        self.loadbutton.configure(text="Load...", width=180)
        self.loadbutton.place(anchor="center", relx=0.5, rely=0.85, x=0, y=0)

        self.savebutton = CTkButton(self.sidebar)
        self.savebutton.configure(text="Save...", width=180)
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
        self.statusbar = CTkFrame(ctk1)
        self.statusbar.configure(border_width=5, corner_radius=0, height=50, width=1200)
        self.runbutton = CTkButton(self.statusbar)
        self.runbutton.configure(text="Run", command=self.execute)
        self.runbutton.place(anchor="e", relx=0.98, rely=0.5, x=0, y=0)
        self.statuslabel = CTkLabel(self.statusbar)
        self.statuslabel.configure(justify="right", text="Current status: idle")
        self.statuslabel.place(anchor="e", relx=0.85, rely=0.5, x=0, y=0)
        self.statusbar.grid(column=0, columnspan=2, row=1)

        # Raise initial frame
        self.initialframe.tkraise()

        # Top level windows
        self.about = None
        self.preferences = None
        self.appearance_mode = tk.StringVar(value="System")

        # Main widget
        self.mainwindow = ctk1

    def run(self):
        self.mainwindow.mainloop()

    def execute(self):
        self.initialframe.expressrun()
        geometry = self.geometryframe.loadgeometry()

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
        quit_ = tk.messagebox.askokcancel(title="Exit?", message="Do you want to exit?")
        if quit_:
            sys.exit(0)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    RocketForge().run()
