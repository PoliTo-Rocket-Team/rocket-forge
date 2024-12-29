import tkinter as tk
import customtkinter as ctk
import rocketforge.performance.config as pconf
import rocketforge.thermal.config as tconf
import rocketforge.mission.config as config
import rocketforge.mission.analysis as msa
from customtkinter import CTkEntry, CTkFrame, CTkLabel, CTkButton
from rocketforge.utils.conversions import mass_uom, mdot_uom, density_uom, length_uom
from rocketforge.utils.helpers import update_entry
from numpy import pi


class TanksFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(TanksFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Tanks Design")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.oxframe = CTkFrame(self)
        self.oxframe.configure(border_width=0, height=28, width=293)
        self.oxlabel = CTkLabel(self.oxframe)
        self.oxlabel.configure(text="Oxidizer Tank")
        self.oxlabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.oxframe.place(anchor="w", relx=0.008, rely=0.32, x=0, y=0)

        self.fuelframe = CTkFrame(self)
        self.fuelframe.configure(border_width=0, height=28, width=293)
        self.fuellabel = CTkLabel(self.fuelframe)
        self.fuellabel.configure(text="Fuel Tank")
        self.fuellabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.fuelframe.place(anchor="e", relx=0.992, rely=0.32, x=0, y=0)

        self.mdotlabel = CTkLabel(self, text="Mass flow rate")
        self.mdotlabel.place(anchor="w", relx=0.02, rely=0.11)

        self.mplabel = CTkLabel(self, text="Propellant mass")
        self.mplabel.place(anchor="w", relx=0.02, rely=0.18)

        self.mtlabel = CTkLabel(self, text="Tanks mass (k0 + kt*mp)")
        self.mtlabel.place(anchor="w", relx=0.02, rely=0.25)

        self.mrlabel = CTkLabel(self, text="Mixture ratio")
        self.mrlabel.place(anchor="w", relx=0.52, rely=0.11)

        self.tblabel = CTkLabel(self, text="Flux time")
        self.tblabel.place(anchor="w", relx=0.52, rely=0.18)

        self.k0label = CTkLabel(self, text="k0")
        self.k0label.place(anchor="w", relx=0.52, rely=0.25)

        self.ktlabel = CTkLabel(self, text="kt")
        self.ktlabel.place(anchor="w", relx=0.82, rely=0.25)

        self.oxrholabel = CTkLabel(self, text="Oxidizer density")
        self.oxrholabel.place(anchor="w", relx=0.02, rely=0.39)

        self.oxrlabel = CTkLabel(self, text="Oxidizer tank radius")
        self.oxrlabel.place(anchor="w", relx=0.02, rely=0.46)

        self.oxhlabel = CTkLabel(self, text="Oxidizer tank height")
        self.oxhlabel.place(anchor="w", relx=0.02, rely=0.53)

        self.oxexclabel = CTkLabel(self, text="Oxidizer excess")
        self.oxexclabel.place(anchor="w", relx=0.02, rely=0.6)

        self.oxxlabel = CTkLabel(self, text="Oxidizer tank position")
        self.oxxlabel.place(anchor="w", relx=0.02, rely=0.67)

        self.oxmdotlabel = CTkLabel(self, text="Oxidizer mass flow rate")
        self.oxmdotlabel.place(anchor="w", relx=0.02, rely=0.74)

        self.oxmlabel = CTkLabel(self, text="Oxidizer mass")
        self.oxmlabel.place(anchor="w", relx=0.02, rely=0.81)

        self.fuelrholabel = CTkLabel(self, text="Fuel density")
        self.fuelrholabel.place(anchor="w", relx=0.52, rely=0.39)

        self.fuelrlabel = CTkLabel(self, text="Fuel tank radius")
        self.fuelrlabel.place(anchor="w", relx=0.52, rely=0.46)

        self.fuelhlabel = CTkLabel(self, text="Fuel tank height")
        self.fuelhlabel.place(anchor="w", relx=0.52, rely=0.53)

        self.fuelexclabel = CTkLabel(self, text="Fuel excess")
        self.fuelexclabel.place(anchor="w", relx=0.52, rely=0.6)

        self.fuelxlabel = CTkLabel(self, text="Fuel tank position")
        self.fuelxlabel.place(anchor="w", relx=0.52, rely=0.67)

        self.fuelmdotlabel = CTkLabel(self, text="Fuel mass flow rate")
        self.fuelmdotlabel.place(anchor="w", relx=0.52, rely=0.74)

        self.fuelmlabel = CTkLabel(self, text="Fuel mass")
        self.fuelmlabel.place(anchor="w", relx=0.52, rely=0.81)

        self.mdotentry = CTkEntry(self, placeholder_text="0", width=59)
        self.mdotentry.place(anchor="e", relx=229/600, rely=0.11)

        self.mdotoptmenu = ctk.CTkOptionMenu(self)
        self.mdotuom = tk.StringVar(value="kg/s")
        self.mdotoptmenu.configure(
            values=["kg/s", "g/s", "lb/s"], variable=self.mdotuom, width=60
        )
        self.mdotoptmenu.place(anchor="e", relx=0.48, rely=0.11)

        self.mpentry = CTkEntry(self, placeholder_text="0", width=59)
        self.mpentry.place(anchor="e", relx=229/600, rely=0.18)

        self.mpoptmenu = ctk.CTkOptionMenu(self)
        self.mpuom = tk.StringVar(value="kg")
        self.mpoptmenu.configure(
            values=["kg", "g", "lb"], variable=self.mpuom, width=60
        )
        self.mpoptmenu.place(anchor="e", relx=0.48, rely=0.18)

        self.mtentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.mtentry.place(anchor="e", relx=229/600, rely=0.25)

        self.mtoptmenu = ctk.CTkOptionMenu(self)
        self.mtuom = tk.StringVar(value="kg")
        self.mtoptmenu.configure(
            values=[], variable=self.mtuom, width=60
        )
        self.mtoptmenu.place(anchor="e", relx=0.48, rely=0.25)

        self.mrentry = CTkEntry(self, placeholder_text="0", width=118)
        self.mrentry.place(anchor="e", relx=0.98, rely=0.11)

        self.tbentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.tbentry.place(anchor="e", relx=529/600, rely=0.18)

        self.tboptmenu = ctk.CTkOptionMenu(self)
        self.tbuom = tk.StringVar(value="s")
        self.tboptmenu.configure(
            values=[], variable=self.tbuom, width=60
        )
        self.tboptmenu.place(anchor="e", relx=0.98, rely=0.18)

        self.k0entry = CTkEntry(self, placeholder_text="0", width=59)
        self.k0entry.place(anchor="e", relx=410/600, rely=0.25)

        self.k0optmenu = ctk.CTkOptionMenu(self)
        self.k0uom = tk.StringVar(value="kg")
        self.k0optmenu.configure(
            values=["kg", "g", "lb"], variable=self.k0uom, width=60
        )
        self.k0optmenu.place(anchor="e", relx=0.78, rely=0.25)

        self.ktentry = CTkEntry(self, placeholder_text="0", width=59)
        self.ktentry.place(anchor="e", relx=0.98, rely=0.25)

        self.oxrhoentry = CTkEntry(self, placeholder_text="0", width=59)
        self.oxrhoentry.place(anchor="e", relx=229/600, rely=0.39)

        self.oxrhooptmenu = ctk.CTkOptionMenu(self)
        self.oxrhouom = tk.StringVar(value="kg/m3")
        self.oxrhooptmenu.configure(
            values=["kg/m3", "g/ml", "g/cm3", "lb/in3", "lb/ft3", "lb/gal"], variable=self.oxrhouom, width=60
        )
        self.oxrhooptmenu.place(anchor="e", relx=0.48, rely=0.39)

        self.oxrentry = CTkEntry(self, placeholder_text="0", width=59)
        self.oxrentry.place(anchor="e", relx=229/600, rely=0.46)

        self.oxroptmenu = ctk.CTkOptionMenu(self)
        self.oxruom = tk.StringVar(value="m")
        self.oxroptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.oxruom, width=60
        )
        self.oxroptmenu.place(anchor="e", relx=0.48, rely=0.46)

        self.oxhentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.oxhentry.place(anchor="e", relx=229/600, rely=0.53)

        self.oxhoptmenu = ctk.CTkOptionMenu(self)
        self.oxhuom = tk.StringVar(value="m")
        self.oxhoptmenu.configure(
            values=[], variable=self.oxhuom, width=60
        )
        self.oxhoptmenu.place(anchor="e", relx=0.48, rely=0.53)

        self.oxexcentry = CTkEntry(self, placeholder_text="0", width=118)
        self.oxexcentry.place(anchor="e", relx=0.48, rely=0.6)

        self.oxxentry = CTkEntry(self, placeholder_text="0", width=59)
        self.oxxentry.place(anchor="e", relx=229/600, rely=0.67)

        self.oxxoptmenu = ctk.CTkOptionMenu(self)
        self.oxxuom = tk.StringVar(value="m")
        self.oxxoptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.oxxuom, width=60
        )
        self.oxxoptmenu.place(anchor="e", relx=0.48, rely=0.67)

        self.oxmdotentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.oxmdotentry.place(anchor="e", relx=229/600, rely=0.74)

        self.oxmdotoptmenu = ctk.CTkOptionMenu(self)
        self.oxmdotuom = tk.StringVar(value="kg/s")
        self.oxmdotoptmenu.configure(
            values=[], variable=self.oxmdotuom, width=60
        )
        self.oxmdotoptmenu.place(anchor="e", relx=0.48, rely=0.74)

        self.oxmentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.oxmentry.place(anchor="e", relx=229/600, rely=0.81)

        self.oxmoptmenu = ctk.CTkOptionMenu(self)
        self.oxmuom = tk.StringVar(value="kg")
        self.oxmoptmenu.configure(
            values=[], variable=self.oxmuom, width=60
        )
        self.oxmoptmenu.place(anchor="e", relx=0.48, rely=0.81)

        self.fuelrhoentry = CTkEntry(self, placeholder_text="0", width=59)
        self.fuelrhoentry.place(anchor="e", relx=529/600, rely=0.39)

        self.fuelrhooptmenu = ctk.CTkOptionMenu(self)
        self.fuelrhouom = tk.StringVar(value="kg/m3")
        self.fuelrhooptmenu.configure(
            values=["kg/m3", "g/ml", "g/cm3", "lb/in3", "lb/ft3", "lb/gal"], variable=self.fuelrhouom, width=60
        )
        self.fuelrhooptmenu.place(anchor="e", relx=0.98, rely=0.39)

        self.fuelrentry = CTkEntry(self, placeholder_text="0", width=59)
        self.fuelrentry.place(anchor="e", relx=529/600, rely=0.46)

        self.fuelroptmenu = ctk.CTkOptionMenu(self)
        self.fuelruom = tk.StringVar(value="m")
        self.fuelroptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.fuelruom, width=60
        )
        self.fuelroptmenu.place(anchor="e", relx=0.98, rely=0.46)

        self.fuelhentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.fuelhentry.place(anchor="e", relx=529/600, rely=0.53)

        self.fuelhoptmenu = ctk.CTkOptionMenu(self)
        self.fuelhuom = tk.StringVar(value="m")
        self.fuelhoptmenu.configure(
            values=[], variable=self.fuelhuom, width=60
        )
        self.fuelhoptmenu.place(anchor="e", relx=0.98, rely=0.53)

        self.fuelexcentry = CTkEntry(self, placeholder_text="0", width=118)
        self.fuelexcentry.place(anchor="e", relx=0.98, rely=0.6)

        self.fuelxentry = CTkEntry(self, placeholder_text="0", width=59)
        self.fuelxentry.place(anchor="e", relx=529/600, rely=0.67)

        self.fuelxoptmenu = ctk.CTkOptionMenu(self)
        self.fuelxuom = tk.StringVar(value="m")
        self.fuelxoptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.fuelxuom, width=60
        )
        self.fuelxoptmenu.place(anchor="e", relx=0.98, rely=0.67)

        self.fuelmdotentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.fuelmdotentry.place(anchor="e", relx=529/600, rely=0.74)

        self.fuelmdotoptmenu = ctk.CTkOptionMenu(self)
        self.fuelmdotuom = tk.StringVar(value="kg/s")
        self.fuelmdotoptmenu.configure(
            values=[], variable=self.fuelmdotuom, width=60
        )
        self.fuelmdotoptmenu.place(anchor="e", relx=0.98, rely=0.74)

        self.fuelmentry = CTkEntry(self, placeholder_text="0", width=59, state="disabled")
        self.fuelmentry.place(anchor="e", relx=529/600, rely=0.81)

        self.fuelmoptmenu = ctk.CTkOptionMenu(self)
        self.fuelmuom = tk.StringVar(value="kg")
        self.fuelmoptmenu.configure(
            values=[], variable=self.fuelmuom, width=60
        )
        self.fuelmoptmenu.place(anchor="e", relx=0.98, rely=0.81)

        self.button = CTkButton(self, text="Compute", width=118, command=self.compute)
        self.button.place(anchor="center", relx=0.5, rely=0.9)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def compute(self):
        try:
            if self.mdotentry.get() == "":
                update_entry(self.mdotentry, (pconf.m_f_d + pconf.m_ox_d) /  mdot_uom(self.mdotuom.get()))
            if self.mrentry.get() == "":
                if tconf.film:
                    update_entry(self.mrentry, pconf.mr * (100 + tconf.oxfilm) / (100 + tconf.fuelfilm))
                else:
                    update_entry(self.mrentry, pconf.mr)
        except Exception:
            pass

        try:
            config.mdot = float(self.mdotentry.get()) * mdot_uom(self.mdotuom.get())
            config.MR = float(self.mrentry.get())
            config.prop_mass = float(self.mpentry.get()) * mass_uom(self.mpuom.get())
            k0 = float(self.k0entry.get()) * mass_uom(self.k0uom.get())
            config.tanks_mass = k0 + float(self.ktentry.get()) * config.prop_mass
            config.ox_rho = float(self.oxrhoentry.get()) * density_uom(self.oxrhouom.get())
            config.fuel_rho = float(self.fuelrhoentry.get()) * density_uom(self.fuelrhouom.get())
            config.r_ox = float(self.oxrentry.get()) * length_uom(self.oxruom.get())
            config.r_fuel = float(self.fuelrentry.get()) * length_uom(self.fuelruom.get())
            config.exc_ox = float(self.oxexcentry.get())
            config.exc_fuel = float(self.fuelexcentry.get())
            config.ox_tank_pos = float(self.oxxentry.get()) * length_uom(self.oxxuom.get())
            config.fuel_tank_pos = float(self.fuelxentry.get()) * length_uom(self.fuelxuom.get())

            m_ox = config.prop_mass * config.MR / (1 + config.MR)
            m_fuel = config.prop_mass / (1 + config.MR)
            mdot_ox = config.mdot * config.MR / (1 + config.MR)
            mdot_fuel = config.mdot / (1 + config.MR)
            h_ox = config.exc_ox * m_ox / config.ox_rho / (pi * config.r_ox**2)
            h_fuel = config.exc_fuel * m_fuel / config.fuel_rho / (pi * config.r_fuel**2)

            update_entry(self.mtentry, config.tanks_mass, True)
            update_entry(self.tbentry, config.prop_mass / config.mdot, True)
            update_entry(self.oxhentry, h_ox, True)
            update_entry(self.fuelhentry, h_fuel, True)
            update_entry(self.oxmdotentry, mdot_ox, True)
            update_entry(self.fuelmdotentry, mdot_fuel, True)
            update_entry(self.oxmentry, m_ox, True)
            update_entry(self.fuelmentry, m_fuel, True)

            msa.set_engine()
        except Exception:
            pass