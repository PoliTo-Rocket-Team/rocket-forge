#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu


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

        areauoms = {
            "m2": 1,
            "cm2": 10**(-4),
            "mm2": 10**(-6),
            "sq in": 0.00064516,
            "sq ft": 0.09290304,
        }

        lengthuoms = {
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "in": 0.0254,
            "ft": 0.3048,
        }

        angleuoms = {
            "deg": 0.01745329,
            "rad": 1,
        }

        geometry = []
        geometry.append(float(self.throatareaentry.get()) * areauoms[self.throatareauom.get()])
        geometry.append(float(self.divergentlengthentry.get()) * lengthuoms[self.divergentlengthuom.get()])
        geometry.append(float(self.thetaexentry.get()) * angleuoms[self.thetaexuom.get()])
        return geometry


if __name__ == "__main__":
    root = tk.Tk()
    widget = GeometryFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
