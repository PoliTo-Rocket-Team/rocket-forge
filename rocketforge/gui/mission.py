import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import rocketforge.mission.config as config
import rocketforge.mission.analysis as msa
from rocketforge.utils.helpers import updateentry
from rocketforge.utils.resources import resource_path
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkButton


class MissionFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(MissionFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Mission Analysis")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.envlabel = CTkLabel(self, text="Environment is not set")
        self.envlabel.place(anchor="w", relx=0.02, rely=0.11, x=0, y=0)

        self.envbutton = CTkButton(self)
        self.envbutton.configure(text="Set Environment...", command=self.environment_window, width=118)
        self.envbutton.place(anchor="e", relx=0.48, rely=0.11, x=0, y=0)
        self.envwindow = None

        self.raillabel = CTkLabel(self, text="Rail is not configured")
        self.raillabel.place(anchor="w", relx=0.52, rely=0.11, x=0, y=0)

        self.railbutton = CTkButton(self)
        self.railbutton.configure(text="Configure Rail...", command=self.rail_window, width=118)
        self.railbutton.place(anchor="e", relx=0.98, rely=0.11, x=0, y=0)
        self.railwindow = None

        self.configure(border_width=1, corner_radius=0, height=480, width=600)
    
    def environment_window(self):
        if self.envwindow is None or not self.envwindow.winfo_exists():
            self.envwindow = ctk.CTkToplevel()
            self.envwindow.title("Set Environment")
            self.envwindow.configure(width=250, height=350)
            self.envwindow.resizable(False, False)
            self.envwindow.after(
                201,
                lambda: self.envwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.latitudelabel = CTkLabel(self.envwindow, text="Latitude")
            self.latitudelabel.place(anchor="sw", relx=0.05, rely=0.105)
            self.latitudeentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.latitudeentry.place(anchor="se", relx=0.95, rely=0.105)

            self.longitudelabel = CTkLabel(self.envwindow, text="Longitude")
            self.longitudelabel.place(anchor="sw", relx=0.05, rely=0.23)
            self.longitudeentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.longitudeentry.place(anchor="se", relx=0.95, rely=0.23)

            self.elevationlabel = CTkLabel(self.envwindow, text="Elevation")
            self.elevationlabel.place(anchor="sw", relx=0.05, rely=0.355)
            self.elevationentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.elevationentry.place(anchor="se", relx=0.95, rely=0.355)

            self.yearlabel = CTkLabel(self.envwindow, text="Year")
            self.yearlabel.place(anchor="sw", relx=0.05, rely=0.48)
            self.yearentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.yearentry.place(anchor="se", relx=0.95, rely=0.48)

            self.monthlabel = CTkLabel(self.envwindow, text="Month")
            self.monthlabel.place(anchor="sw", relx=0.05, rely=0.605)
            self.monthentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.monthentry.place(anchor="se", relx=0.95, rely=0.605)

            self.daylabel = CTkLabel(self.envwindow, text="Day")
            self.daylabel.place(anchor="sw", relx=0.05, rely=0.73)
            self.dayentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.dayentry.place(anchor="se", relx=0.95, rely=0.73)

            self.hourlabel = CTkLabel(self.envwindow, text="Hour")
            self.hourlabel.place(anchor="sw", relx=0.05, rely=0.855)
            self.hourentry = CTkEntry(self.envwindow, placeholder_text="0", width=118)
            self.hourentry.place(anchor="se", relx=0.95, rely=0.855)

            self.setenvbutton = CTkButton(self.envwindow, text="Set", command=self.set_environment, width=90)
            self.setenvbutton.place(anchor="s", relx=0.75, rely=0.97)

            self.loadenvbutton = CTkButton(self.envwindow, text="Load", command=self.load_environment, width=90)
            self.loadenvbutton.place(anchor="s", relx=0.25, rely=0.97)

            self.envwindow.after(50, self.envwindow.lift)
            self.envwindow.after(50, self.envwindow.focus)

        else:
            self.envwindow.lift()
            self.envwindow.focus()

    def load_environment(self):
        try:
            updateentry(self.latitudeentry, config.latitude)
            updateentry(self.longitudeentry, config.longitude)
            updateentry(self.elevationentry, config.elevation)
            updateentry(self.yearentry, config.year)
            updateentry(self.monthentry, config.month)
            updateentry(self.dayentry, config.day)
            updateentry(self.hourentry, config.hour)
        except Exception:
            pass

    def set_environment(self):
        self.envlabel.configure(text="Setting up environment...")
        self.envlabel.update()
        try:
            config.latitude = float(self.latitudeentry.get())
            config.longitude = float(self.longitudeentry.get())
            config.elevation = float(self.elevationentry.get())
            config.year = int(float(self.yearentry.get()))
            config.month = int(float(self.monthentry.get()))
            config.day = int(float(self.dayentry.get()))
            config.hour = int(float(self.hourentry.get()))
            msa.set_environment()
            self.envlabel.configure(text="Environment has been set")
            self.envlabel.update()
        except Exception:
            self.envlabel.configure(text="An error has occurred")
            self.envlabel.update()
    
    def rail_window(self):
        if self.railwindow is None or not self.railwindow.winfo_exists():
            self.railwindow = ctk.CTkToplevel()
            self.railwindow.title("Configure Rail")
            self.railwindow.configure(width=250, height=180)
            self.railwindow.resizable(False, False)
            self.railwindow.after(
                201,
                lambda: self.railwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.raillengthlabel = CTkLabel(self.railwindow, text="Rail length [m]")
            self.raillengthlabel.place(anchor="w", relx=0.05, rely=0.14)
            self.raillengthentry = CTkEntry(self.railwindow, placeholder_text="0", width=118)
            self.raillengthentry.place(anchor="e", relx=0.95, rely=0.14)

            self.inclinationlabel = CTkLabel(self.railwindow, text="Inclination [deg]")
            self.inclinationlabel.place(anchor="w", relx=0.05, rely=0.38)
            self.inclinationentry = CTkEntry(self.railwindow, placeholder_text="0", width=118)
            self.inclinationentry.place(anchor="e", relx=0.95, rely=0.38)

            self.headinglabel = CTkLabel(self.railwindow, text="Heading [deg]")
            self.headinglabel.place(anchor="w", relx=0.05, rely=0.62)
            self.headingentry = CTkEntry(self.railwindow, placeholder_text="0", width=118)
            self.headingentry.place(anchor="e", relx=0.95, rely=0.62)

            self.setrailbutton = CTkButton(self.railwindow, text="Set", command=self.set_rail, width=90)
            self.setrailbutton.place(anchor="center", relx=0.75, rely=0.86)

            self.loadrailbutton = CTkButton(self.railwindow, text="Load", command=self.load_rail, width=90)
            self.loadrailbutton.place(anchor="center", relx=0.25, rely=0.86)

            self.railwindow.after(50, self.railwindow.lift)
            self.railwindow.after(50, self.railwindow.focus)

        else:
            self.railwindow.lift()
            self.railwindow.focus()

    def load_rail(self):
        try:
            updateentry(self.raillengthentry, config.rail_length)
            updateentry(self.inclinationentry, config.inclination)
            updateentry(self.headingentry, config.heading)
        except Exception:
            pass

    def set_rail(self):
        self.raillabel.configure(text="Setting up rail...")
        self.raillabel.update()
        try:
            config.rail_length = float(self.raillengthentry.get())
            config.inclination = float(self.inclinationentry.get())
            config.heading = float(self.headingentry.get())
            self.raillabel.configure(text="Rail has been configured")
            self.raillabel.update()
        except Exception:
            self.raillabel.configure(text="Rail is not configured")
            self.raillabel.update()
