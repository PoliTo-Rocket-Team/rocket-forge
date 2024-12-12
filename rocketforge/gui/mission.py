import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import sys
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

        self.enginelabel = CTkLabel(self, text="Engine is not configured")
        self.enginelabel.place(anchor="w", relx=0.02, rely=0.18, x=0, y=0)

        self.enginebutton = CTkButton(self)
        self.enginebutton.configure(text="Configure Engine...", command=self.engine_window, width=118)
        self.enginebutton.place(anchor="e", relx=0.48, rely=0.18, x=0, y=0)
        self.enginewindow = None

        self.rocketlabel = CTkLabel(self, text="Rocket is not configured")
        self.rocketlabel.place(anchor="w", relx=0.52, rely=0.18, x=0, y=0)

        self.rocketbutton = CTkButton(self)
        self.rocketbutton.configure(text="Configure Rocket...", command=self.rocket_window, width=118)
        self.rocketbutton.place(anchor="e", relx=0.98, rely=0.18, x=0, y=0)
        self.rocketwindow = None
        self.nosekindvar = tk.StringVar(value="conical")

        self.finslabel = CTkLabel(self, text="Fin sets: 0")
        self.finslabel.place(anchor="w", relx=0.02, rely=0.25, x=0, y=0)

        self.finsbutton = CTkButton(self)
        self.finsbutton.configure(text="Add Fins...", command=self.fins_window, width=118)
        self.finsbutton.place(anchor="e", relx=0.48, rely=0.25, x=0, y=0)
        self.finswindow = None
        self.fns = 0

        self.parachutelabel = CTkLabel(self, text="Parachutes: 0")
        self.parachutelabel.place(anchor="w", relx=0.52, rely=0.25, x=0, y=0)

        self.parachutebutton = CTkButton(self)
        self.parachutebutton.configure(text="Add Parachute...", command=self.parachute_window, width=118)
        self.parachutebutton.place(anchor="e", relx=0.98, rely=0.25, x=0, y=0)
        self.parachutewindow = None
        self.triggerwindow = None
        self.triggervar = ctk.IntVar(value=0)
        self.np = 0

        CTkButton(
            self, text="Plot 3D Trajectory", command=self.plot_trajectory, width=105
        ).place(anchor="center", relx=0.12, rely=0.32)

        CTkButton(
            self, text="Draw Rocket", command=self.draw_rocket, width=105
        ).place(anchor="center", relx=0.31, rely=0.32)

        CTkButton(
            self, text="Flight Plots", command=self.plot_all, width=105
        ).place(anchor="center", relx=0.5, rely=0.32)

        CTkButton(
            self, text="Rocket Plots", command=self.plot_all_rocket, width=105
        ).place(anchor="center", relx=0.69, rely=0.32)

        CTkButton(
            self, text="Engine Plots", command=self.plot_all_engine, width=105
        ).place(anchor="center", relx=0.88, rely=0.32)

        self.console = Console(self, height=300, state="disabled", wrap="word")
        self.console.place(anchor="s", relx=0.5, rely=0.99, relwidth=0.98)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def plot_trajectory(self):
        if config.flight is None:
            messagebox.showwarning(title="Warning", message="Please run the simulation first.")
            return
        msa.plot_trajectory()

    def draw_rocket(self):
        if config.rocket is None:
            messagebox.showwarning(title="Warning", message="Please configure the rocket first.")
            return
        msa.draw_rocket()

    def plot_all(self):
        if config.flight is None:
            messagebox.showwarning(title="Warning", message="Please run the simulation first.")
            return
        msa.plot_all()

    def plot_all_rocket(self):
        if config.rocket is None:
            messagebox.showwarning(title="Warning", message="Please configure the rocket first.")
            return
        msa.plot_all_rocket()

    def plot_all_engine(self):
        if config.engine is None:
            messagebox.showwarning(title="Warning", message="Please configure the engine first.")
            return
        msa.plot_all_engine()

    def run(self):
        try:
            self.console.clear()
            self.console.enable()
            msa.simulate()
            self.console.disable()
        except Exception:
            print("An error has occurred on mission frame")
            self.console.disable()
    
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
            print("An error has occurred on mission frame. Could not load environment")

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
            self.envwindow.destroy()
            msa.set_environment()
            self.envlabel.configure(text="Environment has been set")
            self.envlabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not set environment")
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
            print("An error has occurred on mission frame. Could not load rail")

    def set_rail(self):
        self.raillabel.configure(text="Setting up rail...")
        self.raillabel.update()
        try:
            config.rail_length = float(self.raillengthentry.get())
            config.inclination = float(self.inclinationentry.get())
            config.heading = float(self.headingentry.get())
            self.railwindow.destroy()
            self.raillabel.configure(text="Rail has been configured")
            self.raillabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not set rail")
            self.raillabel.configure(text="Rail is not configured")
            self.raillabel.update()

    def engine_window(self):
        if self.enginewindow is None or not self.enginewindow.winfo_exists():
            self.enginewindow = ctk.CTkToplevel()
            self.enginewindow.title("Configure Engine")
            self.enginewindow.configure(width=350, height=350)
            self.enginewindow.resizable(False, False)
            self.enginewindow.after(
                201,
                lambda: self.enginewindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.thrustlabel = CTkLabel(self.enginewindow, text="Thrust [N]")
            self.thrustlabel.place(anchor="w", relx=0.05, rely=1/14)
            self.thrustentry = CTkEntry(self.enginewindow, placeholder_text="0", width=118)
            self.thrustentry.place(anchor="e", relx=0.95, rely=1/14)

            self.chambermasslabel = CTkLabel(self.enginewindow, text="Chamber mass (no tanks) [kg]")
            self.chambermasslabel.place(anchor="w", relx=0.05, rely=3/14)
            self.chambermassentry = CTkEntry(self.enginewindow, placeholder_text="0", width=118)
            self.chambermassentry.place(anchor="e", relx=0.95, rely=3/14)

            self.engineinertialabel = CTkLabel(self.enginewindow, text="Inertia [kg m2]")
            self.engineinertialabel.place(anchor="w", relx=0.05, rely=5/14)
            self.enginei11entry = CTkEntry(self.enginewindow, placeholder_text="Ixx", width=45)
            self.enginei11entry.place(anchor="e", relx=0.65, rely=5/14)
            self.enginei22entry = CTkEntry(self.enginewindow, placeholder_text="Iyy", width=45)
            self.enginei22entry.place(anchor="e", relx=0.8, rely=5/14)
            self.enginei33entry = CTkEntry(self.enginewindow, placeholder_text="Izz", width=45)
            self.enginei33entry.place(anchor="e", relx=0.95, rely=5/14)

            self.ecogdrylabel = CTkLabel(self.enginewindow, text="Engine CoG Dry [m]")
            self.ecogdrylabel.place(anchor="w", relx=0.05, rely=7/14)
            self.ecogdryentry = CTkEntry(self.enginewindow, placeholder_text="0", width=118)
            self.ecogdryentry.place(anchor="e", relx=0.95, rely=7/14)

            self.enginepositionlabel = CTkLabel(self.enginewindow, text="Engine position [m]")
            self.enginepositionlabel.place(anchor="w", relx=0.05, rely=9/14)
            self.enginepositionentry = CTkEntry(self.enginewindow, placeholder_text="0", width=118)
            self.enginepositionentry.place(anchor="e", relx=0.95, rely=9/14)

            self.relabel = CTkLabel(self.enginewindow, text="Nozzle exit radius [m]")
            self.relabel.place(anchor="w", relx=0.05, rely=11/14)
            self.reentry = CTkEntry(self.enginewindow, placeholder_text="0", width=118)
            self.reentry.place(anchor="e", relx=0.95, rely=11/14)

            self.setenginebutton = CTkButton(self.enginewindow, text="Set", command=self.set_engine, width=90)
            self.setenginebutton.place(anchor="center", relx=0.75, rely=13/14)

            self.loadenginebutton = CTkButton(self.enginewindow, text="Load", command=self.load_engine, width=90)
            self.loadenginebutton.place(anchor="center", relx=0.25, rely=13/14)

            self.enginewindow.after(50, self.enginewindow.lift)
            self.enginewindow.after(50, self.enginewindow.focus)

        else:
            self.enginewindow.lift()
            self.enginewindow.focus()

    def load_engine(self):
        try:
            updateentry(self.thrustentry, config.thrust)
            updateentry(self.chambermassentry, config.chamber_mass)
            updateentry(self.enginei11entry, config.dry_inertia[0])
            updateentry(self.enginei22entry, config.dry_inertia[1])
            updateentry(self.enginei33entry, config.dry_inertia[2])
            updateentry(self.ecogdryentry, config.engine_CoG_dry)
            updateentry(self.reentry, config.Re)
            updateentry(self.enginepositionentry, config.engine_position)
        except Exception:
            print("An error has occurred on mission frame. Could not load engine")

    def set_engine(self):
        self.enginelabel.configure(text="Setting up engine...")
        self.enginelabel.update()
        try:
            try:
                config.thrust = float(self.thrustentry.get())
            except ValueError:
                print("An error has occurred on mission frame. set_engine function throws value error.")
                config.thrust = self.thrustentry.get()
            config.chamber_mass = float(self.chambermassentry.get())
            ei11 = float(self.enginei11entry.get())
            ei22 = float(self.enginei22entry.get())
            ei33 = float(self.enginei33entry.get())
            config.dry_inertia = (ei11, ei22, ei33)
            config.engine_CoG_dry = float(self.ecogdryentry.get())
            config.engine_position = float(self.enginepositionentry.get())
            config.Re = float(self.reentry.get())
            msa.set_engine()
            self.enginewindow.destroy()
            self.enginelabel.configure(text="Engine has been configured")
            self.enginelabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not set engine")
            config.engine = None
            self.enginelabel.configure(text="Engine is not configured")
            self.enginelabel.update()

    def rocket_window(self):
        if config.engine is None:
            messagebox.showwarning(title="Warning", message="Please configure the engine first.")
            return
        
        if self.rocketwindow is None or not self.rocketwindow.winfo_exists():
            self.rocketwindow = ctk.CTkToplevel()
            self.rocketwindow.title("Configure Rocket")
            self.rocketwindow.configure(width=350, height=300)
            self.rocketwindow.resizable(False, False)
            self.rocketwindow.after(
                201,
                lambda: self.rocketwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.rocketmasslabel = CTkLabel(self.rocketwindow, text="Rocket mass [kg]")
            self.rocketmasslabel.place(anchor="w", relx=0.05, rely=1/14)
            self.rocketmassentry = CTkEntry(self.rocketwindow, placeholder_text="0", width=118)
            self.rocketmassentry.place(anchor="e", relx=0.95, rely=1/14)
    
            self.rocketradiuslabel = CTkLabel(self.rocketwindow, text="Rocket radius [m]")
            self.rocketradiuslabel.place(anchor="w", relx=0.05, rely=3/14)
            self.rocketradiusentry = CTkEntry(self.rocketwindow, placeholder_text="0", width=118)
            self.rocketradiusentry.place(anchor="e", relx=0.95, rely=3/14)

            self.cogwmlabel = CTkLabel(self.rocketwindow, text="CoG without motor [m]")
            self.cogwmlabel.place(anchor="w", relx=0.05, rely=5/14)
            self.cogwmentry = CTkEntry(self.rocketwindow, placeholder_text="0", width=118)
            self.cogwmentry.place(anchor="e", relx=0.95, rely=5/14)

            self.rocketinertialabel = CTkLabel(self.rocketwindow, text="Inertia [kg m2]")
            self.rocketinertialabel.place(anchor="w", relx=0.05, rely=7/14)
            self.rocketi11entry = CTkEntry(self.rocketwindow, placeholder_text="Ixx", width=45)
            self.rocketi11entry.place(anchor="e", relx=0.65, rely=7/14)
            self.rocketi22entry = CTkEntry(self.rocketwindow, placeholder_text="Iyy", width=45)
            self.rocketi22entry.place(anchor="e", relx=0.8, rely=7/14)
            self.rocketi33entry = CTkEntry(self.rocketwindow, placeholder_text="Izz", width=45)
            self.rocketi33entry.place(anchor="e", relx=0.95, rely=7/14)

            self.noselengthlabel = CTkLabel(self.rocketwindow, text="Nose length [m]")
            self.noselengthlabel.place(anchor="w", relx=0.05, rely=9/14)
            self.noselengthentry = CTkEntry(self.rocketwindow, placeholder_text="0", width=118)
            self.noselengthentry.place(anchor="e", relx=0.95, rely=9/14)

            self.nosekindlabel = CTkLabel(self.rocketwindow, text="Nose shape")
            self.nosekindlabel.place(anchor="w", relx=0.05, rely=11/14)
            self.nosekindoptmenu = ctk.CTkOptionMenu(
                self.rocketwindow, variable=self.nosekindvar, width=118,
                values=[
                    "conical",
                    "lvhaack",
                    "ogive",
                    "elliptical",
                    "vonkarman",
                    "parabolic",
                    "powerseries"
                ]
            )
            self.nosekindoptmenu.place(anchor="e", relx=0.95, rely=11/14)

            self.setrocketbutton = CTkButton(self.rocketwindow, text="Set", command=self.set_rocket, width=90)
            self.setrocketbutton.place(anchor="center", relx=0.75, rely=13/14)

            self.loadrocketbutton = CTkButton(self.rocketwindow, text="Load", command=self.load_rocket, width=90)
            self.loadrocketbutton.place(anchor="center", relx=0.25, rely=13/14)

            self.rocketwindow.after(50, self.rocketwindow.lift)
            self.rocketwindow.after(50, self.rocketwindow.focus)

        else:
            self.rocketwindow.lift()
            self.rocketwindow.focus()

    def load_rocket(self):
        try:
            updateentry(self.rocketmassentry, config.rocket_mass)
            updateentry(self.rocketradiusentry, config.rocket_radius)
            updateentry(self.cogwmentry, config.rocket_CoG_dry)
            updateentry(self.rocketi11entry, config.rocket_inertia[0])
            updateentry(self.rocketi22entry, config.rocket_inertia[1])
            updateentry(self.rocketi33entry, config.rocket_inertia[2])
            updateentry(self.noselengthentry, config.nose_length)
        except Exception:
            print("An error has occurred on mission frame. Could not load rocket")

    def set_rocket(self):
        self.rocketlabel.configure(text="Setting up rocket...")
        self.rocketlabel.update()
        try:
            config.rocket_mass = float(self.rocketmassentry.get())
            config.rocket_radius = float(self.rocketradiusentry.get())
            config.rocket_CoG_dry = float(self.cogwmentry.get())
            ri11 = float(self.rocketi11entry.get())
            ri22 = float(self.rocketi22entry.get())
            ri33 = float(self.rocketi33entry.get())
            config.rocket_inertia = (ri11, ri22, ri33)
            config.nose_length = float(self.noselengthentry.get())
            config.nose_kind = self.nosekindvar.get()
            config.drag = filedialog.askopenfilename(title="Load drag coefficient file")
            msa.set_rocket()
            self.rocketwindow.destroy()
            self.rocketlabel.configure(text="Rocket has been configured")
            self.rocketlabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not set rocket")
            config.rocket = None
            self.rocketlabel.configure(text="Rocket is not configured")
            self.rocketlabel.update()
        self.nfs = 0
        self.finslabel.configure(text="Fin sets: 0")
        self.finslabel.update()
        self.np = 0
        self.parachutelabel.configure(text="Parachutes: 0")
        self.parachutelabel.update()

    def fins_window(self):
        if config.rocket is None:
            messagebox.showwarning(title="Warning", message="Please configure the rocket first.")
            return

        if self.finswindow is None or not self.finswindow.winfo_exists():
            self.finswindow = ctk.CTkToplevel()
            self.finswindow.title("Add Fins")
            self.finswindow.configure(width=350, height=300)
            self.finswindow.resizable(False, False)
            self.finswindow.after(
                201,
                lambda: self.finswindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.finsnlabel = CTkLabel(self.finswindow, text="Fins number")
            self.finsnlabel.place(anchor="w", relx=0.05, rely=1/14)
            self.finsnentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finsnentry.place(anchor="e", relx=0.95, rely=1/14)

            self.finsrclabel = CTkLabel(self.finswindow, text="Fins root chord [m]")
            self.finsrclabel.place(anchor="w", relx=0.05, rely=3/14)
            self.finsrcentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finsrcentry.place(anchor="e", relx=0.95, rely=3/14)

            self.finstclabel = CTkLabel(self.finswindow, text="Fins tip chord [m]")
            self.finstclabel.place(anchor="w", relx=0.05, rely=5/14)
            self.finstcentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finstcentry.place(anchor="e", relx=0.95, rely=5/14)

            self.finsslabel = CTkLabel(self.finswindow, text="Fins span [m]")
            self.finsslabel.place(anchor="w", relx=0.05, rely=7/14)
            self.finssentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finssentry.place(anchor="e", relx=0.95, rely=7/14)

            self.finsswlabel = CTkLabel(self.finswindow, text="Fins sweep length [m]")
            self.finsswlabel.place(anchor="w", relx=0.05, rely=9/14)
            self.finsswentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finsswentry.place(anchor="e", relx=0.95, rely=9/14)

            self.finsposlabel = CTkLabel(self.finswindow, text="Fins position [m]")
            self.finsposlabel.place(anchor="w", relx=0.05, rely=11/14)
            self.finsposentry = CTkEntry(self.finswindow, placeholder_text="0", width=118)
            self.finsposentry.place(anchor="e", relx=0.95, rely=11/14)

            self.setfinsbutton = CTkButton(self.finswindow, text="Add", command=self.add_fins, width=90)
            self.setfinsbutton.place(anchor="center", relx=0.5, rely=13/14)

            self.finswindow.after(50, self.finswindow.lift)
            self.finswindow.after(50, self.finswindow.focus)

        else:
            self.finswindow.lift()
            self.finswindow.focus()

    def add_fins(self):
        self.finslabel.configure(text="Adding fin set...")
        self.finslabel.update()
        try:
            config.nfins = int(float(self.finsnentry.get()))
            config.root_chord = float(self.finsrcentry.get())
            config.tip_chord = float(self.finstcentry.get())
            config.span = float(self.finssentry.get()) 
            config.sweep_length = float(self.finsswentry.get())
            config.fins_position = float(self.finsposentry.get())
            msa.add_fins()
            self.nfs += 1
            self.finswindow.destroy()
            self.finslabel.configure(text=f"Fin sets: {self.nfs}")
            self.finslabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not add fins")
            config.rocket = None
            self.rocketlabel.configure(text="Rocket is not configured")
            self.rocketlabel.update()
            self.nfs = 0
            self.finslabel.configure(text="Fin sets: 0")
            self.finslabel.update()
            self.np = 0
            self.parachutelabel.configure(text="Parachutes: 0")
            self.parachutelabel.update()

    def parachute_window(self):
        if config.rocket is None:
            messagebox.showwarning(title="Warning", message="Please configure the rocket first.")
            return

        if self.parachutewindow is None or not self.parachutewindow.winfo_exists():
            self.parachutewindow = ctk.CTkToplevel()
            self.parachutewindow.title("Add Parachute")
            self.parachutewindow.configure(width=350, height=300)
            self.parachutewindow.resizable(False, False)
            self.parachutewindow.after(
                201,
                lambda: self.parachutewindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            self.namelabel = CTkLabel(self.parachutewindow, text="Parachute name")
            self.namelabel.place(anchor="w", relx=0.05, rely=1/14)
            self.nameentry = CTkEntry(self.parachutewindow, placeholder_text="name", width=118)
            self.nameentry.place(anchor="e", relx=0.95, rely=1/14)

            self.cdslabel = CTkLabel(self.parachutewindow, text="Drag coefficient * reference area")
            self.cdslabel.place(anchor="w", relx=0.05, rely=3/14)
            self.cdsentry = CTkEntry(self.parachutewindow, placeholder_text="0", width=118)
            self.cdsentry.place(anchor="e", relx=0.95, rely=3/14)

            self.triggerlabel = CTkLabel(self.parachutewindow, text="Trigger")
            self.triggerlabel.place(anchor="w", relx=0.05, rely=5/14)
            self.triggerbutton = CTkButton(self.parachutewindow, text="Set Trigger...", command=self.trigger_window, width=118)
            self.triggerbutton.place(anchor="e", relx=0.95, rely=5/14)

            self.samplabel = CTkLabel(self.parachutewindow, text="Sampling rate")
            self.samplabel.place(anchor="w", relx=0.05, rely=7/14)
            self.sampentry = CTkEntry(self.parachutewindow, placeholder_text="0", width=118)
            self.sampentry.place(anchor="e", relx=0.95, rely=7/14)

            self.laglabel = CTkLabel(self.parachutewindow, text="Lag")
            self.laglabel.place(anchor="w", relx=0.05, rely=9/14)
            self.lagentry = CTkEntry(self.parachutewindow, placeholder_text="0", width=118)
            self.lagentry.place(anchor="e", relx=0.95, rely=9/14)

            self.noiselabel = CTkLabel(self.parachutewindow, text="Noise [Pa]")
            self.noiselabel.place(anchor="w", relx=0.05, rely=11/14)
            self.noiseentry1 = CTkEntry(self.parachutewindow, placeholder_text="mean", width=45)
            self.noiseentry1.place(anchor="e", relx=0.65, rely=11/14)
            self.noiseentry2 = CTkEntry(self.parachutewindow, placeholder_text="rms", width=45)
            self.noiseentry2.place(anchor="e", relx=0.8, rely=11/14)
            self.noiseentry3 = CTkEntry(self.parachutewindow, placeholder_text="tau", width=45)
            self.noiseentry3.place(anchor="e", relx=0.95, rely=11/14)

            self.addparachutebutton = CTkButton(self.parachutewindow, text="Add", command=self.add_parachute, width=90)
            self.addparachutebutton.place(anchor="center", relx=0.5, rely=13/14)

            self.parachutewindow.after(50, self.parachutewindow.lift)
            self.parachutewindow.after(50, self.parachutewindow.focus)

        else:
            self.parachutewindow.lift()
            self.parachutewindow.focus()

    def trigger_window(self):
        if self.triggerwindow is None or not self.triggerwindow.winfo_exists():
            self.triggerwindow = ctk.CTkToplevel()
            self.triggerwindow.title("Set Trigger")
            self.triggerwindow.configure(width=350, height=300)
            self.triggerwindow.resizable(False, False)
            self.triggerwindow.after(
                201,
                lambda: self.triggerwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            ctk.CTkRadioButton(
                self.triggerwindow,
                text="Apogee",
                variable=self.triggervar,
                value=0,
            ).place(anchor="w", relx=0.05, rely=1/12)

            ctk.CTkRadioButton(
                self.triggerwindow,
                text="Descending at AGL height [m]",
                variable=self.triggervar,
                value=1,
            ).place(anchor="w", relx=0.05, rely=3/12)
            self.t1entry = CTkEntry(self.triggerwindow, placeholder_text="0", width=118)
            self.t1entry.place(anchor="e", relx=0.95, rely=3/12)

            ctk.CTkRadioButton(
                self.triggerwindow,
                text="Ascending at AGL height [m]",
                variable=self.triggervar,
                value=2,
            ).place(anchor="w", relx=0.05, rely=5/12)
            self.t2entry = CTkEntry(self.triggerwindow, placeholder_text="0", width=118)
            self.t2entry.place(anchor="e", relx=0.95, rely=5/12)

            ctk.CTkRadioButton(
                self.triggerwindow,
                text="Descending at freestream pressure [Pa]",
                variable=self.triggervar,
                value=3,
            ).place(anchor="w", relx=0.05, rely=7/12)
            self.t3entry = CTkEntry(self.triggerwindow, placeholder_text="0", width=118)
            self.t3entry.place(anchor="e", relx=0.95, rely=7/12)

            ctk.CTkRadioButton(
                self.triggerwindow,
                text="Ascending at freestream pressure [Pa]",
                variable=self.triggervar,
                value=4,
            ).place(anchor="w", relx=0.05, rely=9/12)
            self.t4entry = CTkEntry(self.triggerwindow, placeholder_text="0", width=118)
            self.t4entry.place(anchor="e", relx=0.95, rely=9/12)

            self.settriggerbutton = CTkButton(self.triggerwindow, text="Set", command=self.set_trigger, width=90)
            self.settriggerbutton.place(anchor="center", relx=0.5, rely=11/12)

            self.triggerwindow.after(50, self.triggerwindow.lift)
            self.triggerwindow.after(50, self.triggerwindow.focus)

    def set_trigger(self):
        if self.triggervar.get() == 0:
            config.trigger = "apogee"
        if self.triggervar.get() == 1:
            agl = float(self.t1entry.get())
            config.trigger = lambda p, h, y: True if y[5] < 0 and h <= agl else False
        if self.triggervar.get() == 2:
            agl = float(self.t2entry.get())
            config.trigger = lambda p, h, y: True if y[5] > 0 and h >= agl else False
        if self.triggervar.get() == 3:
            fsp = float(self.t3entry.get())
            config.trigger = lambda p, h, y: True if y[5] < 0 and p > fsp else False
        if self.triggervar.get() == 4:
            fsp = float(self.t4entry.get())
            config.trigger = lambda p, h, y: True if y[5] > 0 and p < fsp else False
        self.triggerwindow.destroy()
        self.triggervar.set(0)

    def add_parachute(self):
        if config.trigger == None:
            messagebox.showwarning(title="Warning", message="Please set the trigger first.")
            return
        
        self.parachutelabel.configure(text="Adding parachute...")
        self.parachutelabel.update()
        try:
            config.parachute = self.nameentry.get()
            config.cd_s = float(self.cdsentry.get())
            config.sampling_rate = float(self.sampentry.get())
            config.lag = float(self.lagentry.get())
            noise1 = float(self.noiseentry1.get())
            noise2 = float(self.noiseentry2.get())
            noise3 = float(self.noiseentry3.get())
            config.noise = (noise1, noise2, noise3)
            msa.add_parachute()
            self.np += 1
            self.parachutewindow.destroy()
            self.parachutelabel.configure(text=f"Parachutes: {self.np}")
            self.parachutelabel.update()
        except Exception:
            print("An error has occurred on mission frame. Could not add parachute")
            config.rocket = None
            self.rocketlabel.configure(text="Rocket is not configured")
            self.rocketlabel.update()
            self.nfs = 0
            self.finslabel.configure(text="Fin sets: 0")
            self.finslabel.update()
            self.np = 0
            self.parachutelabel.configure(text="Parachutes: 0")
            self.parachutelabel.update()
        config.trigger = None


class Console(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        kwargs.update({"state": "disabled"})
        ctk.CTkTextbox.__init__(self, *args, **kwargs)
        self.bind("<Destroy>", self.reset)
        self.old_stdout = sys.stdout
        sys.stdout = self
        self.enabled = False
    
    def clear(self):
        self.configure(state="normal")
        self.delete("0.0", "20000.0")
        self.configure(state="disabled")
    
    def write(self, content):
        if self.enabled:
            self.configure(state="normal")
            self.insert("end", content)
            self.configure(state="disabled")

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
    
    def reset(self, event):
        sys.stdout = self.old_stdout
