import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkCheckBox
import rocketforge.thermal.config as config


class ThermalFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(ThermalFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Thermal Analysis")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.filmcb = CTkCheckBox(self)
        self.filmcb.configure(text="Enable film cooling along injector head", command=self.toggle_film_cooling)
        self.filmcb.place(anchor="w", relx=0.02, rely=0.11)

        CTkLabel(self, text="Oxidizer film cooling percentage").place(anchor="w", relx=0.02, rely=0.18)
        CTkLabel(self, text="%").place(anchor="e", relx=0.48, rely=0.18)
        self.oxfilm = CTkEntry(self)
        self.oxfilm.configure(state="disabled", width=80)
        self.oxfilm.place(anchor="e", relx=0.46, rely=0.18)

        CTkLabel(self, text="Fuel film cooling percentage").place(anchor="w", relx=0.02, rely=0.25)
        CTkLabel(self, text="%").place(anchor="e", relx=0.48, rely=0.25)
        self.fuelfilm = CTkEntry(self)
        self.fuelfilm.configure(state="disabled", width=80)
        self.fuelfilm.place(anchor="e", relx=0.46, rely=0.25)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def toggle_film_cooling(self):
        config.film = not config.film
        self.oxfilm.configure(state="normal" if config.film else "disabled")
        self.fuelfilm.configure(state="normal" if config.film else "disabled")

    def load_film_cooling(self):
        config.oxfilm = 0.0 if self.oxfilm.get() == "" else float(self.oxfilm.get())
        config.fuelfilm = 0.0 if self.fuelfilm.get() == "" else float(self.fuelfilm.get())