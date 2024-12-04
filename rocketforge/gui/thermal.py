import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkButton, CTkFrame, CTkLabel, CTkCheckBox, CTkOptionMenu
import rocketforge.thermal.config as config


class ThermalFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(ThermalFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self, border_width=0, height=28, width=590)
        CTkLabel(self.topframe, text="Thermal Analysis").place(anchor="center", relx=0.5, rely=0.5, x=0, y=0) 
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.regenframe = CTkFrame(self, border_width=0, height=28, width=590)
        CTkLabel(self.regenframe, text="Regenerative cooling").place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.regenframe.place(anchor="center", relx=0.5, rely=0.11, x=0, y=0)
        
        CTkCheckBox(
            self,
            text="Enable regenerative cooling",
            command=self.toggle_regen_cooling
        ).place(anchor="w", relx=0.02, rely=0.18)

        CTkLabel(self, text="Coolant").place(anchor="w", relx=0.52, rely=0.18)
        self.coolant = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.coolant, width=118
        ).place(anchor="e", relx=0.98, rely=0.18, x=0, y=0)

        CTkLabel(self, text="Coolant mass flow rate").place(anchor="w", relx=0.02, rely=0.25)
        self.mdotcentry = CTkEntry(self, state="disabled", width=59)
        self.mdotcentry.place(anchor="e", relx=229/600, rely=0.25)
        self.mdotcuom = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.mdotcuom, width=59
        ).place(anchor="e", relx=0.48, rely=0.25, x=0, y=0)

        CTkButton(self, text="Fuel mass flow rate", width=135).place(anchor="w", relx=0.49, rely=0.25)
        CTkButton(self, text="Oxidizer mass flow rate", width=135).place(anchor="e", relx=0.95, rely=0.25)

        CTkLabel(self, text="Coolant inlet temperature").place(anchor="w", relx=0.02, rely=0.32)
        self.tcientry = CTkEntry(self, state="disabled", width=59)
        self.tcientry.place(anchor="e", relx=229/600, rely=0.32)
        self.tciuom = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.tciuom, width=59
        ).place(anchor="e", relx=0.48, rely=0.32, x=0, y=0)

        CTkLabel(self, text="Coolant inlet pressure").place(anchor="w", relx=0.52, rely=0.32)
        self.pcientry = CTkEntry(self, state="disabled", width=59)
        self.pcientry.place(anchor="e", relx=529/600, rely=0.32)
        self.pciuom = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.pciuom, width=59
        ).place(anchor="e", relx=0.98, rely=0.32, x=0, y=0)

        CTkLabel(self, text="Inner wall thickness").place(anchor="w", relx=0.02, rely=0.39)
        self.tentry = CTkEntry(self, state="disabled", width=59)
        self.tentry.place(anchor="e", relx=229/600, rely=0.39)
        self.tuom = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.tuom, width=59
        ).place(anchor="e", relx=0.48, rely=0.39, x=0, y=0)

        CTkLabel(self, text="Wall conductivity").place(anchor="w", relx=0.52, rely=0.39)
        self.kentry = CTkEntry(self, state="disabled", width=59)
        self.kentry.place(anchor="e", relx=529/600, rely=0.39)
        self.kuom = tk.StringVar(value="")
        CTkOptionMenu(
            self,
            values=[""],
            variable=self.kuom, width=59
        ).place(anchor="e", relx=0.98, rely=0.39, x=0, y=0)

        CTkButton(self, text="Channels geometry...", width=135).place(anchor="center", relx=0.25, rely=0.46)
        CTkButton(self, text="Advanced options...", width=135).place(anchor="center", relx=0.75, rely=0.46)

        self.filmframe = CTkFrame(self, border_width=0, height=28, width=590)
        CTkLabel(self.filmframe, text="Radiation cooling").place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.filmframe.place(anchor="center", relx=0.5, rely=0.53, x=0, y=0)

        CTkCheckBox(
            self,
            text="Enable radiation cooling (work in progress)",
            command=self.toggle_rad_cooling
        ).place(anchor="w", relx=0.02, rely=0.60)

        CTkLabel(self, text="Wall emissivity").place(anchor="w", relx=0.52, rely=0.60)
        self.radepsentry = CTkEntry(self, state="disabled", width=118)
        self.radepsentry.place(anchor="e", relx=0.98, rely=0.60)

        self.filmframe = CTkFrame(self, border_width=0, height=28, width=590)
        CTkLabel(self.filmframe, text="Film cooling").place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.filmframe.place(anchor="center", relx=0.5, rely=0.67, x=0, y=0)

        CTkCheckBox(
            self,
            text="Enable film cooling along injector head (thermal model still in development)",
            command=self.toggle_film_cooling
        ).place(anchor="w", relx=0.02, rely=0.74)

        CTkLabel(self, text="Fuel film cooling percentage").place(anchor="w", relx=0.02, rely=0.81)
        CTkLabel(self, text="%").place(anchor="e", relx=0.48, rely=0.81)
        self.fuelfilm = CTkEntry(self, state="disabled", width=80)
        self.fuelfilm.place(anchor="e", relx=0.46, rely=0.81)

        CTkLabel(self, text="Oxidizer film cooling percentage").place(anchor="w", relx=0.52, rely=0.81)
        CTkLabel(self, text="%").place(anchor="e", relx=0.98, rely=0.81)
        self.oxfilm = CTkEntry(self, state="disabled", width=80)
        self.oxfilm.place(anchor="e", relx=0.96, rely=0.81)

        CTkButton(self, text="Plot temperatures", width=135).place(anchor="center", relx=0.125, rely=0.92)
        CTkButton(self, text="Plot wall heat flux", width=135).place(anchor="center", relx=0.375, rely=0.92)
        CTkButton(self, text="Plot channels geometry", width=135).place(anchor="center", relx=0.625, rely=0.92)
        CTkButton(self, text="Details", width=135).place(anchor="center", relx=0.875, rely=0.92)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def toggle_film_cooling(self):
        config.film = not config.film
        self.oxfilm.configure(state="normal" if config.film else "disabled")
        self.fuelfilm.configure(state="normal" if config.film else "disabled")

    def toggle_regen_cooling(self):
        ...

    def toggle_rad_cooling(self):
        ...

    def load_film_cooling(self):
        config.oxfilm = 0.0 if self.oxfilm.get() == "" else float(self.oxfilm.get())
        config.fuelfilm = 0.0 if self.fuelfilm.get() == "" else float(self.fuelfilm.get())