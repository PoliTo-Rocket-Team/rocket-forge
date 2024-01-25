import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu
from rocketforge.utils.conversions import angle_uom, area_uom, length_uom


class GeometryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(GeometryFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Geometry (TODO)"
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.throatarealabel = CTkLabel(self)
        self.throatarealabel.configure(text="Throat area:")
        self.throatarealabel.place(anchor="w", relx=0.05, rely=0.24, x=0, y=0)

        self.throatareaentry = CTkEntry(self)
        self.throatareaentry.configure(placeholder_text="0", width=100)
        self.throatareaentry.place(anchor="w", relx=0.2, rely=0.24, x=0, y=0)

        self.throatareaoptmenu = CTkOptionMenu(self)
        self.throatareauom = tk.StringVar(value="m2")
        self.throatareaoptmenu.configure(
            values=["m2", "cm2", "mm2", "sq in", "sq ft"], variable=self.throatareauom, width=100
        )
        self.throatareaoptmenu.place(anchor="w", relx=0.3, rely=0.24, x=0, y=0)

        self.divergentlengthlabel = CTkLabel(self)
        self.divergentlengthlabel.configure(text="Divergent length:")
        self.divergentlengthlabel.place(anchor="w", relx=0.05, rely=0.29, x=0, y=0)

        self.divergentlengthentry = CTkEntry(self)
        self.divergentlengthentry.configure(placeholder_text="0", width=100)
        self.divergentlengthentry.place(anchor="w", relx=0.2, rely=0.29, x=0, y=0)

        self.divergentlengthoptmenu = CTkOptionMenu(self)
        self.divergentlengthuom = tk.StringVar(value="m")
        self.divergentlengthoptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.divergentlengthuom, width=100
        )
        self.divergentlengthoptmenu.place(anchor="w", relx=0.3, rely=0.29, x=0, y=0)

        self.thetaexlabel = CTkLabel(self)
        self.thetaexlabel.configure(text="Final parabola angle:")
        self.thetaexlabel.place(anchor="w", relx=0.05, rely=0.34, x=0, y=0)

        self.thetaexentry = CTkEntry(self)
        self.thetaexentry.configure(placeholder_text="0", width=100)
        self.thetaexentry.place(anchor="w", relx=0.2, rely=0.34, x=0, y=0)

        self.thetaexoptmenu = CTkOptionMenu(self)
        self.thetaexuom = tk.StringVar(value="deg")
        self.thetaexoptmenu.configure(
            values=["deg", "rad"], variable=self.thetaexuom, width=100
        )
        self.thetaexoptmenu.place(anchor="w", relx=0.3, rely=0.34, x=0, y=0)

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def loadgeometry(self):
        geometry = []
        geometry.append(float(self.throatareaentry.get()) * area_uom(self.throatareauom.get()))
        geometry.append(float(self.divergentlengthentry.get()) * length_uom(self.divergentlengthuom.get()))
        geometry.append(float(self.thetaexentry.get()) * angle_uom(self.thetaexuom.get()))
        return geometry