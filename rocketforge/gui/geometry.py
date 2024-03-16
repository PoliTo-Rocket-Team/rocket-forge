import tkinter as tk
from tkinter.messagebox import showwarning
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton
import rocketforge.geometry.top as top
import rocketforge.geometry.tic as tic
import rocketforge.geometry.conical as conical
import rocketforge.geometry.convergent as convergent
from rocketforge.utils.conversions import angle_uom, area_uom, length_uom
from rocketforge.utils.helpers import updateentry
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import concatenate


class GeometryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(GeometryFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Geometry"
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.throatarealabel = CTkLabel(self)
        self.throatarealabel.configure(text="Throat area:")
        self.throatarealabel.place(anchor="w", relx=0.05, rely=0.22, x=0, y=0)

        self.throatareaentry = CTkEntry(self)
        self.throatareaentry.configure(placeholder_text="0", width=100)
        self.throatareaentry.place(anchor="e", relx=0.35, rely=0.22, x=0, y=0)

        self.throatareaoptmenu = CTkOptionMenu(self)
        self.throatareauom = tk.StringVar(value="m2")
        self.throatareaoptmenu.configure(
            values=["m2", "cm2", "mm2", "sq in", "sq ft"], variable=self.throatareauom, width=100
        )
        self.throatareaoptmenu.place(anchor="e", relx=0.45, rely=0.22, x=0, y=0)

        # Convergent section
        self.r1ovrtlabel = CTkLabel(self)
        self.r1ovrtlabel.configure(text="R1/Rt:")
        self.r1ovrtlabel.place(anchor="w", relx=0.05, rely=0.27, x=0, y=0)

        self.r1ovrtentry = CTkEntry(self)
        self.r1ovrtentry.configure(placeholder_text="0", width=200)
        self.r1ovrtentry.place(anchor="e", relx=0.45, rely=0.27, x=0, y=0)
        updateentry(self.r1ovrtentry, "1.5")

        self.chamberlengthlabel = CTkLabel(self)
        self.chamberlengthlabel.configure(text="Chamber length:")
        self.chamberlengthlabel.place(anchor="w", relx=0.05, rely=0.32, x=0, y=0)

        self.chamberlengthentry = CTkEntry(self)
        self.chamberlengthentry.configure(placeholder_text="0", width=100)
        self.chamberlengthentry.place(anchor="e", relx=0.35, rely=0.32, x=0, y=0)
        updateentry(self.chamberlengthentry, "1.0")

        self.chamberlengthoptmenu = CTkOptionMenu(self)
        self.chamberlengthuom = tk.StringVar(value="L* [m]")
        self.chamberlengthoptmenu.configure(
            values=["L* [m]", "m", "cm", "mm", "in", "ft"], variable=self.chamberlengthuom, width=100
        )
        self.chamberlengthoptmenu.place(anchor="e", relx=0.45, rely=0.32, x=0, y=0)

        self.blabel = CTkLabel(self)
        self.blabel.configure(text="Contraction angle:")
        self.blabel.place(anchor="w", relx=0.05, rely=0.37, x=0, y=0)

        self.bentry = CTkEntry(self)
        self.bentry.configure(placeholder_text="0", width=100)
        self.bentry.place(anchor="e", relx=0.35, rely=0.37, x=0, y=0)
        updateentry(self.bentry, "30")

        self.boptmenu = CTkOptionMenu(self)
        self.buom = tk.StringVar(value="deg")
        self.boptmenu.configure(
            values=["deg", "rad"], variable=self.buom, width=100
        )
        self.boptmenu.place(anchor="e", relx=0.45, rely=0.37, x=0, y=0)

        self.r2ovr2maxlabel = CTkLabel(self)
        self.r2ovr2maxlabel.configure(text="R2/R2max:")
        self.r2ovr2maxlabel.place(anchor="w", relx=0.05, rely=0.42, x=0, y=0)

        self.r2ovr2maxentry = CTkEntry(self)
        self.r2ovr2maxentry.configure(placeholder_text="0", width=200)
        self.r2ovr2maxentry.place(anchor="e", relx=0.45, rely=0.42, x=0, y=0)
        updateentry(self.r2ovr2maxentry, "0.5")

        self.epsclabel = CTkLabel(self)
        self.epsclabel.configure(text="Contraction Area Ratio:")
        self.epsclabel.place(anchor="w", relx=0.05, rely=0.47, x=0, y=0)

        self.epscentry = CTkEntry(self)
        self.epscentry.configure(width=200, state="disabled")
        self.epscentry.place(anchor="e", relx=0.45, rely=0.47, x=0, y=0)
        updateentry(self.epscentry, "Undefined", True)

        # Divergent Section
        self.shapelabel = CTkLabel(self)
        self.shapelabel.configure(text="Nozzle shape:")
        self.shapelabel.place(anchor="w", relx=0.55, rely=0.22, x=0, y=0)

        self.shapeoptmenu = CTkOptionMenu(self)
        self.shape = tk.StringVar(value="Thrust-optimized parabolic")
        self.shapeoptmenu.configure(
            values=["Thrust-optimized parabolic", "Truncated ideal contour", "Conical"],
            variable=self.shape, command=self.change_shape, width=200
        )
        self.shapeoptmenu.place(anchor="e", relx=0.95, rely=0.22, x=0, y=0)

        self.rnovrtlabel = CTkLabel(self)
        self.rnovrtlabel.configure(text="Rn/Rt:")
        self.rnovrtlabel.place(anchor="w", relx=0.55, rely=0.27, x=0, y=0)

        self.rnovrtentry = CTkEntry(self)
        self.rnovrtentry.configure(placeholder_text="0", width=200)
        self.rnovrtentry.place(anchor="e", relx=0.95, rely=0.27, x=0, y=0)
        updateentry(self.rnovrtentry, "0.382")

        self.epslabel = CTkLabel(self)
        self.epslabel.configure(text="Expansion Area Ratio:")
        self.epslabel.place(anchor="w", relx=0.55, rely=0.47, x=0, y=0)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(width=200, state="disabled")
        self.epsentry.place(anchor="e", relx=0.95, rely=0.47, x=0, y=0)
        updateentry(self.epsentry, "Undefined", True)

        # Thrust-optimized parabolic (TOP)
        self.divergentlengthlabel = CTkLabel(self)
        self.divergentlengthlabel.configure(text="Divergent length:")
        self.divergentlengthlabel.place(anchor="w", relx=0.55, rely=0.32, x=0, y=0)

        self.divergentlengthentry = CTkEntry(self)
        self.divergentlengthentry.configure(placeholder_text="0", width=100)
        self.divergentlengthentry.place(anchor="e", relx=0.85, rely=0.32, x=0, y=0)
        updateentry(self.divergentlengthentry, "0.8")

        self.divergentlengthoptmenu = CTkOptionMenu(self)
        self.divergentlengthuom = tk.StringVar(value="Le/Lc15")
        self.divergentlengthoptmenu.configure(
            values=["Le/Lc15", "m", "cm", "mm", "in", "ft"], variable=self.divergentlengthuom, width=100
        )
        self.divergentlengthoptmenu.place(anchor="e", relx=0.95, rely=0.32, x=0, y=0)

        self.thetanlabel = CTkLabel(self)
        self.thetanlabel.configure(text="Initial parabola angle:")
        self.thetanlabel.place(anchor="w", relx=0.55, rely=0.37, x=0, y=0)

        self.thetanentry = CTkEntry(self)
        self.thetanentry.configure(placeholder_text="0", width=100)
        self.thetanentry.place(anchor="e", relx=0.85, rely=0.37, x=0, y=0)

        self.thetanoptmenu = CTkOptionMenu(self)
        self.thetanuom = tk.StringVar(value="deg")
        self.thetanoptmenu.configure(
            values=["deg", "rad"], variable=self.thetanuom, width=100
        )
        self.thetanoptmenu.place(anchor="e", relx=0.95, rely=0.37, x=0, y=0)

        self.thetaexlabel = CTkLabel(self)
        self.thetaexlabel.configure(text="Final parabola angle:")
        self.thetaexlabel.place(anchor="w", relx=0.55, rely=0.42, x=0, y=0)

        self.thetaexentry = CTkEntry(self)
        self.thetaexentry.configure(placeholder_text="0", width=100)
        self.thetaexentry.place(anchor="e", relx=0.85, rely=0.42, x=0, y=0)

        self.thetaexoptmenu = CTkOptionMenu(self)
        self.thetaexuom = tk.StringVar(value="deg")
        self.thetaexoptmenu.configure(
            values=["deg", "rad"], variable=self.thetaexuom, width=100
        )
        self.thetaexoptmenu.place(anchor="e", relx=0.95, rely=0.42, x=0, y=0)

        # Conical Nozzle
        self.cselected = ctk.IntVar(value=0)

        self.cleRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=0
        )

        self.clelabel = CTkLabel(self)
        self.clelabel.configure(text="Divergent length:")

        self.cleentry = CTkEntry(self)
        self.cleentry.configure(placeholder_text="0", width=100)

        self.cleoptmenu = CTkOptionMenu(self)
        self.cleuom = tk.StringVar(value="m")
        self.cleoptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.cleuom, width=100
        )

        self.clfRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=1
        )

        self.clflabel = CTkLabel(self)
        self.clflabel.configure(text="Relative length Le/Lc15:")

        self.clfentry = CTkEntry(self)
        self.clfentry.configure(placeholder_text="0", width=200)

        self.cthetaRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=2
        )

        self.cthetalabel= CTkLabel(self)
        self.cthetalabel.configure(text="Divergent angle:")

        self.cthetaentry = CTkEntry(self)
        self.cthetaentry.configure(placeholder_text="0", width=100)

        self.cthetaoptmenu = CTkOptionMenu(self)
        self.cthetauom = tk.StringVar(value="deg")
        self.cthetaoptmenu.configure(
            values=["deg", "rad"], variable=self.cthetauom, width=100
        )

        # Plot
        self.plotbutton = CTkButton(self)
        self.plotbutton.configure(text="Update plot", command=self.plot)
        self.plotbutton.place(anchor="center", relx=0.5, rely=0.53)

        self.plotframe = CTkFrame(self)
        self.plotframe.configure(border_width=5, height=300, width=950)
        self.plotframe.place(anchor="center", relx=0.5, rely=0.77, x=0, y=0)

        self.fig = Figure(figsize = (11.75, 3.625), dpi=80)
        self.fig.set_facecolor("#c1c1c1")
        self.fig.subplots_adjust(top=0.92, bottom=0.14, left=0.08, right=0.92)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotframe)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel("Radius [m]")
        self.ax.set_xlabel("Axis [m]")
        self.ax.grid()
        self.ax.set_facecolor("#ebebeb")

        self.canvas.get_tk_widget().place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)

        self.eps = None
        self.epsc = None

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def plot(self):
        # Compute divergent section
        try:
            if self.eps == None:
                showwarning(title="Warning", message="Please define the area ratio and run the simulation first.")
                raise Exception
            eps = self.eps
            updateentry(self.epsentry, eps, True)

            At = float(self.throatareaentry.get()) * area_uom(self.throatareauom.get())
            RnOvRt = float(self.rnovrtentry.get())

            # Thrust-optimized parabolic (TOP)
            if self.shape.get() == "Thrust-optimized parabolic":
                if self.divergentlengthuom.get() == "Le/Lc15":
                    Le = float(self.divergentlengthentry.get()) * conical.lc15(At, RnOvRt, eps)
                else:
                    Le = float(self.divergentlengthentry.get()) * length_uom(self.divergentlengthuom.get())

                thetan = float(self.thetanentry.get()) * angle_uom(self.thetanuom.get())
                thetae = float(self.thetaexentry.get()) * angle_uom(self.thetaexuom.get())

                if thetan <= thetae:
                    showwarning(title="Warning", message="Final parabola angle must be greater than initial parabola angle")
                    raise Exception
            
                xD, yD = top.get(At, RnOvRt, Le, thetan, thetae, eps)
            
            # Truncated ideal contour (TIC)
            if self.shape.get() == "Truncated ideal contour":
                ...

            # Conical nozzle
            if self.shape.get() == "Conical":

                selected = self.cselected.get()
                
                if selected == 0:
                    Le = float(self.cleentry.get()) * length_uom(self.cleuom.get())
                    Lf = Le / conical.lc15(At, RnOvRt, eps)
                    thetae = conical.get_theta(At, RnOvRt, eps, Le)

                if selected == 1:
                    Lf = float(self.clfentry.get())
                    Le = Lf * conical.lc15(At, RnOvRt, eps)
                    thetae = conical.get_theta(At, RnOvRt, eps, Le)

                if selected == 2:
                    thetae = float(self.cthetaentry.get()) * angle_uom(self.cthetauom.get())
                    if thetae <= 0:
                        showwarning(title="Warning", message="Divergent angle must be positive")
                        raise Exception
                    Le = conical.le(At, RnOvRt, eps, thetae)
                    Lf = Le / conical.lc15(At, RnOvRt, eps)
                
                updateentry(self.cleentry, Le / length_uom(self.cleuom.get()))
                updateentry(self.clfentry, Lf)
                updateentry(self.cthetaentry, thetae / angle_uom(self.cthetauom.get()))

                xD, yD = conical.get(At, RnOvRt, eps, Le, thetae)

        except Exception:
            xD = []
            yD = []

        # Compute convergent section
        try:
            if self.epsc == None:
                raise Exception
            epsc = float(self.epsc)
            updateentry(self.epscentry, epsc, True)
            
            At = float(self.throatareaentry.get()) * area_uom(self.throatareauom.get())
            R1OvRt = float(self.r1ovrtentry.get())
            b = float(self.bentry.get()) * angle_uom(self.buom.get())
            R2OvR2max = float(self.r2ovr2maxentry.get())

            if self.chamberlengthuom.get() == "L* [m]":
                Lstar = float(self.chamberlengthentry.get())
                Lc = convergent.get_Lc(At, R1OvRt, Lstar, b, R2OvR2max, epsc)
            else:
                Lc = float(self.chamberlengthentry.get()) * length_uom(self.chamberlengthuom.get())
                Lstar = convergent.get_Lstar(At, R1OvRt, Lc, b, R2OvR2max, epsc)

            xC, yC = convergent.get(At, R1OvRt, Lc, b, R2OvR2max, epsc)
        except Exception:
            xC = []
            yC = []

        try:
            # Concatenate coordinates
            x = concatenate((xC, xD))
            y = concatenate((yC, yD))

            # Plot geometry
            self.ax.clear()
            self.ax.plot(x, y, "black")
            try:
                self.ax.axis([-1.05*Lc, 1.05*Le, 0, 1.05*(Le + Lc) * 226.2/789.6])
            except Exception:
                pass
            self.ax.grid()
            self.ax.set_ylabel("Radius [m]")
            self.ax.set_xlabel("Axis [m]")
            self.canvas.draw()

            # Return values for performance estimation
            return At, Le, thetae
        except Exception:
            pass

    def change_shape(self, shape):

        self.remove_elements()

        if shape == "Thrust-optimized parabolic":
            self.divergentlengthlabel.place(anchor="w", relx=0.55, rely=0.32, x=0, y=0)
            self.divergentlengthentry.place(anchor="e", relx=0.85, rely=0.32, x=0, y=0)
            self.divergentlengthoptmenu.place(anchor="e", relx=0.95, rely=0.32, x=0, y=0)
            self.thetanlabel.place(anchor="w", relx=0.55, rely=0.37, x=0, y=0)
            self.thetanentry.place(anchor="e", relx=0.85, rely=0.37, x=0, y=0)
            self.thetanoptmenu.place(anchor="e", relx=0.95, rely=0.37, x=0, y=0)
            self.thetaexlabel.place(anchor="w", relx=0.55, rely=0.42, x=0, y=0)
            self.thetaexentry.place(anchor="e", relx=0.85, rely=0.42, x=0, y=0)
            self.thetaexoptmenu.place(anchor="e", relx=0.95, rely=0.42, x=0, y=0)

        if shape == "Truncated ideal contour":
            ...

        if shape == "Conical":
            self.cleRB.place(anchor="e", relx=0.82, rely=0.32, x=0, y=0)
            self.clelabel.place(anchor="w", relx=0.55, rely=0.32, x=0, y=0)
            self.cleentry.place(anchor="e", relx=0.85, rely=0.32, x=0, y=0)
            self.cleoptmenu.place(anchor="e", relx=0.95, rely=0.32, x=0, y=0)
            self.clfRB.place(anchor="e", relx=0.82, rely=0.37, x=0, y=0)
            self.clflabel.place(anchor="w", relx=0.55, rely=0.37, x=0, y=0)
            self.clfentry.place(anchor="e", relx=0.95, rely=0.37, x=0, y=0)
            self.cthetaRB.place(anchor="e", relx=0.82, rely=0.42, x=0, y=0)
            self.cthetalabel.place(anchor="w", relx=0.55, rely=0.42, x=0, y=0)
            self.cthetaentry.place(anchor="e", relx=0.85, rely=0.42, x=0, y=0)
            self.cthetaoptmenu.place(anchor="e", relx=0.95, rely=0.42, x=0, y=0)

    def remove_elements(self):
        self.divergentlengthlabel.place_forget()
        self.divergentlengthentry.place_forget()
        self.divergentlengthoptmenu.place_forget()
        self.thetanlabel.place_forget()
        self.thetanentry.place_forget()
        self.thetanoptmenu.place_forget()
        self.thetaexlabel.place_forget()
        self.thetaexentry.place_forget()
        self.thetaexoptmenu.place_forget()
        self.cleRB.place_forget()
        self.clelabel.place_forget()
        self.cleentry.place_forget()
        self.cleoptmenu.place_forget()
        self.clfRB.place_forget()
        self.clflabel.place_forget()
        self.clfentry.place_forget()
        self.cthetaRB.place_forget()
        self.cthetalabel.place_forget()
        self.cthetaentry.place_forget()
        self.cthetaoptmenu.place_forget()

    def loadgeometry(self, eps, epsc):
        self.eps = eps
        self.epsc = epsc
        At, Le, thetae = self.plot()
        geometry = [At, Le, thetae]
        return geometry