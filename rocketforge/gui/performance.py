import tkinter as tk
import customtkinter as ctk
import os
import rocketforge.performance.config as config
from customtkinter          import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkButton
from rocketforge.performance.theoreticalperf  import theoretical
from rocketforge.performance.corrfactors      import correction_factors
from rocketforge.performance.deliveredperf    import delivered
from rocketforge.utils.helpers                import updateentry, updatetextbox


class PerformanceFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(PerformanceFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Performance Analysis")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.thermodynamicframe = ThermodynamicFrame(self)
        self.thermodynamicframe.configure(height=404, width=590)
        self.thermodynamicframe.place(anchor="s", relx=0.5, rely=0.99)

        self.deliveredframe = DeliveredFrame(self)
        self.deliveredframe.configure(height=404, width=590)
        self.deliveredframe.place(anchor="s", relx=0.5, rely=0.99)

        self.thermodynamicbutton = CTkButton(self, width=295)
        self.thermodynamicbutton.configure(
            text="Thermodynamic properties", command=lambda: self.switchtab(1),
            fg_color=["gray55","gray25"], hover_color=["gray50","gray20"]
        )
        self.thermodynamicbutton.place(anchor="e", relx=0.5, rely=0.11)

        self.deliveredbutton = CTkButton(self, width=295)
        self.deliveredbutton.configure(
            text="Delivered performance", command=lambda: self.switchtab(0),
        )
        self.deliveredbutton.place(anchor="w", relx=0.5, rely=0.11)

        self.on = self.deliveredbutton.cget("fg_color")
        self.on_hover = self.deliveredbutton.cget("hover_color")
        self.off = self.thermodynamicbutton.cget("fg_color")
        self.off_hover = self.thermodynamicbutton.cget("hover_color")
        self.deliveredframe.tkraise()
        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def switchtab(self, t):
        if t == 0:
            self.deliveredframe.tkraise()
            self.deliveredbutton.configure(
                fg_color=self.on, hover_color=self.on_hover,
            )
            self.thermodynamicbutton.configure(
                fg_color=self.off, hover_color=self.off_hover,
            )
        else:
            self.thermodynamicframe.tkraise()
            self.deliveredbutton.configure(
                fg_color=self.off, hover_color=self.off_hover,
            )
            self.thermodynamicbutton.configure(
                fg_color=self.on, hover_color=self.on_hover,
            )

    def loadengine(self, geometry):
        config.At, config.Le, config.theta_e = geometry

        if self.thermodynamicframe.frozenflow.get() == 0:
            frozen = 0
            frozenatthroat = 0
        elif self.thermodynamicframe.frozenflow.get() == 1:
            frozen = 1
            frozenatthroat = 0
        elif self.thermodynamicframe.frozenflow.get() == 2:
            frozen = 1
            frozenatthroat = 1

        iter = int(self.thermodynamicframe.stationsentry.get()) + 1

        x = theoretical(iter, frozen, frozenatthroat)

        updatetextbox(self.thermodynamicframe.textbox, x[-1], True)

        correction_factors()

        updateentry(self.deliveredframe.reactioneffentry, config.z_r, True)
        updateentry(self.deliveredframe.overalleffentry, config.z_overall, True)
        updateentry(self.deliveredframe.BLeffentry, config.z_f, True)
        updateentry(self.deliveredframe.diveffentry, config.z_d, True)

        output = delivered()

        updatetextbox(self.deliveredframe.textbox, output, True)


class ThermodynamicFrame(CTkFrame):
    def __init__(self, master=None, **kw):
        super(ThermodynamicFrame, self).__init__(master, **kw)

        self.frozenflow = ctk.IntVar(value=0)

        self.flowmodellabel = CTkLabel(self)
        self.flowmodellabel.configure(text="Flow model")
        self.flowmodellabel.place(anchor="center", relx=0.5, rely=0.07)

        self.equilibriumRB = ctk.CTkRadioButton(
            self, text="Shifting equilibrium flow", variable=self.frozenflow, value=0
        )
        self.equilibriumRB.place(anchor="center", relx=0.2, rely=0.14)

        self.frozenRB = ctk.CTkRadioButton(
            self, text="Frozen equilibrium flow", variable=self.frozenflow, value=1
        )
        self.frozenRB.place(anchor="center", relx=0.5, rely=0.14)

        self.frozenatthroatRB = ctk.CTkRadioButton(
            self, text="Frozen at throat flow", variable=self.frozenflow, value=2
        )
        self.frozenatthroatRB.place(anchor="center", relx=0.8, rely=0.14)

        self.stationslabel = CTkLabel(self)
        self.stationslabel.configure(text="Number of stations")
        self.stationslabel.place(anchor="w", relx=0.02, rely=0.27)

        self.stationsentry = CTkEntry(self)
        self.stationsentry.configure(placeholder_text="1", width=118)
        self.stationsentry.insert("0", "1")
        self.stationsentry.place(anchor="e", relx=0.48, rely=0.27)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(
                self,
                height=260,
                state="disabled",
                wrap="none",
                font=("Courier New", 12),
            )
        else:
            self.textbox = ctk.CTkTextbox(
                self, height=260, state="disabled", wrap="none", font=("Mono", 12)
            )
        self.textbox.place(relwidth=0.98, relx=0.5, rely=0.99, anchor="s")


class DeliveredFrame(CTkFrame):
    def __init__(self, master=None, **kw):
        super(DeliveredFrame, self).__init__(master, **kw)

        self.reactionefflabel = CTkLabel(self)
        self.reactionefflabel.configure(text="Reaction efficiency")
        self.reactionefflabel.place(anchor="w", relx=0.52, rely=0.07)

        self.reactioneffentry = CTkEntry(self)
        self.reactioneffentry.configure(state="disabled", width=120)
        self.reactioneffentry.place(anchor="e", relx=0.98, rely=0.07)

        self.overallefflabel = CTkLabel(self)
        self.overallefflabel.configure(text="Overall efficiency")
        self.overallefflabel.place(anchor="w", relx=0.52, rely=0.16)

        self.overalleffentry = CTkEntry(self)
        self.overalleffentry.configure(state="disabled", width=120)
        self.overalleffentry.place(anchor="e", relx=0.98, rely=0.16)

        self.BLefflabel = CTkLabel(self)
        self.BLefflabel.configure(text="Boundary layer efficiency")
        self.BLefflabel.place(anchor="w", relx=0.02, rely=0.07)

        self.BLeffentry = CTkEntry(self)
        self.BLeffentry.configure(state="disabled", width=120)
        self.BLeffentry.place(anchor="e", relx=0.48, rely=0.07)

        self.divefflabel = CTkLabel(self)
        self.divefflabel.configure(text="Divergence efficiency")
        self.divefflabel.place(anchor="w", relx=0.02, rely=0.16)

        self.diveffentry = CTkEntry(self)
        self.diveffentry.configure(state="disabled", width=120)
        self.diveffentry.place(anchor="e", relx=0.48, rely=0.16)

        self.deliveredlabel = CTkLabel(self)
        self.deliveredlabel.configure(text="Estimated delivered performance")
        self.deliveredlabel.place(anchor="w", relx=0.02, rely=0.27)

        if os.name == "nt":
            self.textbox = ctk.CTkTextbox(
                self,
                height=260,
                state="disabled",
                wrap="none",
                font=("Courier New", 12),
            )
        else:
            self.textbox = ctk.CTkTextbox(
                self, height=260, state="disabled", wrap="none", font=("Mono", 12)
            )
        self.textbox.place(relwidth=0.98, relx=0.5, rely=0.99, anchor="s")