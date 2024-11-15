import tkinter as tk
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkImage
import rocketforge.performance.config as config
import rocketforge.geometry.top as top
import rocketforge.geometry.tic as tic
import rocketforge.geometry.conical as conical
import rocketforge.geometry.convergent as convergent
from rocketforge.utils.conversions import angle_uom, area_uom, length_uom
from rocketforge.utils.helpers import updateentry, updatetextbox
from rocketforge.utils.resources import resource_path
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from numpy import *
import os
from tabulate import tabulate


class GeometryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(GeometryFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Chamber Geometry")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.throatarealabel = CTkLabel(self)
        self.throatarealabel.configure(text="Throat area")
        self.throatarealabel.place(anchor="w", relx=0.02, rely=0.11, x=0, y=0)

        self.throatareaentry = CTkEntry(self)
        self.throatareaentry.configure(placeholder_text="0", width=59)
        self.throatareaentry.place(anchor="e", relx=229/600, rely=0.11, x=0, y=0)

        self.throatareaoptmenu = CTkOptionMenu(self)
        self.throatareauom = tk.StringVar(value="m2")
        self.throatareaoptmenu.configure(
            values=["m2", "cm2", "mm2", "sq in", "sq ft"], variable=self.throatareauom, width=59
        )
        self.throatareaoptmenu.place(anchor="e", relx=0.48, rely=0.11, x=0, y=0)

        # Convergent section
        self.r1ovrtlabel = CTkLabel(self)
        self.r1ovrtlabel.configure(text="R1/Rt")
        self.r1ovrtlabel.place(anchor="w", relx=0.02, rely=0.18, x=0, y=0)

        self.r1ovrtentry = CTkEntry(self)
        self.r1ovrtentry.configure(placeholder_text="0", width=118)
        self.r1ovrtentry.place(anchor="e", relx=0.48, rely=0.18, x=0, y=0)
        updateentry(self.r1ovrtentry, "1.5")

        self.chamberlengthlabel = CTkLabel(self)
        self.chamberlengthlabel.configure(text="Chamber length")
        self.chamberlengthlabel.place(anchor="w", relx=0.02, rely=0.25, x=0, y=0)

        self.chamberlengthentry = CTkEntry(self)
        self.chamberlengthentry.configure(placeholder_text="0", width=59)
        self.chamberlengthentry.place(anchor="e", relx=229/600, rely=0.25, x=0, y=0)
        updateentry(self.chamberlengthentry, "1.0")

        self.chamberlengthoptmenu = CTkOptionMenu(self)
        self.chamberlengthuom = tk.StringVar(value="L* [m]")
        self.chamberlengthoptmenu.configure(
            values=["L* [m]", "m", "cm", "mm", "in", "ft"], variable=self.chamberlengthuom, width=59
        )
        self.chamberlengthoptmenu.place(anchor="e", relx=0.48, rely=0.25, x=0, y=0)

        self.blabel = CTkLabel(self)
        self.blabel.configure(text="Contraction angle")
        self.blabel.place(anchor="w", relx=0.02, rely=0.32, x=0, y=0)

        self.bentry = CTkEntry(self)
        self.bentry.configure(placeholder_text="0", width=59)
        self.bentry.place(anchor="e", relx=229/600, rely=0.32, x=0, y=0)
        updateentry(self.bentry, "30")

        self.boptmenu = CTkOptionMenu(self)
        self.buom = tk.StringVar(value="deg")
        self.boptmenu.configure(
            values=["deg", "rad"], variable=self.buom, width=59
        )
        self.boptmenu.place(anchor="e", relx=0.48, rely=0.32, x=0, y=0)

        self.r2ovr2maxlabel = CTkLabel(self)
        self.r2ovr2maxlabel.configure(text="R2/R2max")
        self.r2ovr2maxlabel.place(anchor="w", relx=0.02, rely=0.39, x=0, y=0)

        self.r2ovr2maxentry = CTkEntry(self)
        self.r2ovr2maxentry.configure(placeholder_text="0", width=118)
        self.r2ovr2maxentry.place(anchor="e", relx=0.48, rely=0.39, x=0, y=0)
        updateentry(self.r2ovr2maxentry, "0.5")

        self.epsclabel = CTkLabel(self)
        self.epsclabel.configure(text="Contraction Area Ratio")
        self.epsclabel.place(anchor="w", relx=0.02, rely=0.46, x=0, y=0)

        self.epscentry = CTkEntry(self)
        self.epscentry.configure(width=118, state="disabled")
        self.epscentry.place(anchor="e", relx=0.48, rely=0.46, x=0, y=0)
        updateentry(self.epscentry, "Undefined", True)

        # Divergent Section
        self.shapelabel = CTkLabel(self)
        self.shapelabel.configure(text="Nozzle shape")
        self.shapelabel.place(anchor="w", relx=0.52, rely=0.11, x=0, y=0)

        self.shapeoptmenu = CTkOptionMenu(self)
        self.shape = tk.StringVar(value="Thrust-optimized parabolic")
        self.shapeoptmenu.configure(
            values=["Thrust-optimized parabolic", "Truncated ideal contour", "Conical"],
            variable=self.shape, command=self.change_shape, width=180
        )
        self.shapeoptmenu.place(anchor="e", relx=0.98, rely=0.11, x=0, y=0)

        self.rnovrtlabel = CTkLabel(self)
        self.rnovrtlabel.configure(text="Rn/Rt")
        self.rnovrtlabel.place(anchor="w", relx=0.52, rely=0.18, x=0, y=0)

        self.rnovrtentry = CTkEntry(self)
        self.rnovrtentry.configure(placeholder_text="0", width=118)
        self.rnovrtentry.place(anchor="e", relx=0.98, rely=0.18, x=0, y=0)
        updateentry(self.rnovrtentry, "0.382")

        self.epslabel = CTkLabel(self)
        self.epslabel.configure(text="Expansion Area Ratio")
        self.epslabel.place(anchor="w", relx=0.52, rely=0.46, x=0, y=0)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(width=118, state="disabled")
        self.epsentry.place(anchor="e", relx=0.98, rely=0.46, x=0, y=0)
        updateentry(self.epsentry, "Undefined", True)

        # Thrust-optimized parabolic (TOP)
        self.divergentlengthlabel = CTkLabel(self)
        self.divergentlengthlabel.configure(text="Divergent length")
        self.divergentlengthlabel.place(anchor="w", relx=0.52, rely=0.25, x=0, y=0)

        self.divergentlengthentry = CTkEntry(self)
        self.divergentlengthentry.configure(placeholder_text="0", width=59)
        self.divergentlengthentry.place(anchor="e", relx=529/600, rely=0.25, x=0, y=0)
        updateentry(self.divergentlengthentry, "0.8")

        self.divergentlengthoptmenu = CTkOptionMenu(self)
        self.divergentlengthuom = tk.StringVar(value="Le/Lc15")
        self.divergentlengthoptmenu.configure(
            values=["Le/Lc15", "m", "cm", "mm", "in", "ft"], variable=self.divergentlengthuom, width=59
        )
        self.divergentlengthoptmenu.place(anchor="e", relx=0.98, rely=0.25, x=0, y=0)

        self.thetanlabel = CTkLabel(self)
        self.thetanlabel.configure(text="Initial parabola angle")
        self.thetanlabel.place(anchor="w", relx=0.52, rely=0.32, x=0, y=0)

        self.thetanentry = CTkEntry(self)
        self.thetanentry.configure(placeholder_text="0", width=59)
        self.thetanentry.place(anchor="e", relx=529/600, rely=0.32, x=0, y=0)

        self.thetanoptmenu = CTkOptionMenu(self)
        self.thetanuom = tk.StringVar(value="deg")
        self.thetanoptmenu.configure(
            values=["deg", "rad"], variable=self.thetanuom, width=59
        )
        self.thetanoptmenu.place(anchor="e", relx=0.98, rely=0.32, x=0, y=0)

        self.thetaexlabel = CTkLabel(self)
        self.thetaexlabel.configure(text="Final parabola angle")
        self.thetaexlabel.place(anchor="w", relx=0.52, rely=0.39, x=0, y=0)

        self.thetaexentry = CTkEntry(self)
        self.thetaexentry.configure(placeholder_text="0", width=59)
        self.thetaexentry.place(anchor="e", relx=529/600, rely=0.39, x=0, y=0)
        updateentry(self.thetaexentry, "8")

        self.thetaexoptmenu = CTkOptionMenu(self)
        self.thetaexuom = tk.StringVar(value="deg")
        self.thetaexoptmenu.configure(
            values=["deg", "rad"], variable=self.thetaexuom, width=59
        )
        self.thetaexoptmenu.place(anchor="e", relx=0.98, rely=0.39, x=0, y=0)

        # Conical Nozzle
        self.cselected = ctk.IntVar(value=0)

        self.cleRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=0
        )

        self.clelabel = CTkLabel(self)
        self.clelabel.configure(text="Divergent length")

        self.cleentry = CTkEntry(self)
        self.cleentry.configure(placeholder_text="0", width=59)

        self.cleoptmenu = CTkOptionMenu(self)
        self.cleuom = tk.StringVar(value="m")
        self.cleoptmenu.configure(
            values=["m", "cm", "mm", "in", "ft"], variable=self.cleuom, width=59
        )

        self.clfRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=1
        )

        self.clflabel = CTkLabel(self)
        self.clflabel.configure(text="Relative length Le/Lc15")

        self.clfentry = CTkEntry(self)
        self.clfentry.configure(placeholder_text="0", width=118)

        self.cthetaRB = ctk.CTkRadioButton(
            self, text="", variable=self.cselected, value=2
        )

        self.cthetalabel= CTkLabel(self)
        self.cthetalabel.configure(text="Divergent angle")

        self.cthetaentry = CTkEntry(self)
        self.cthetaentry.configure(placeholder_text="0", width=59)

        self.cthetaoptmenu = CTkOptionMenu(self)
        self.cthetauom = tk.StringVar(value="deg")
        self.cthetaoptmenu.configure(
            values=["deg", "rad"], variable=self.cthetauom, width=59
        )

        # Buttons
        self.plotbutton = CTkButton(self)
        self.plotbutton.configure(text="Update plot", command=self.plot, width=100)
        self.plotbutton.place(anchor="center", relx=0.12, rely=0.53)

        self.clearplotbutton = CTkButton(self)
        self.clearplotbutton.configure(text="Clear plot", command=self.clear_plot, width=100)
        self.clearplotbutton.place(anchor="center", relx=0.31, rely=0.53)

        self.saveplotbutton = CTkButton(self)
        self.saveplotbutton.configure(text="Export plot...", command=self.export_plot, width=100)
        self.saveplotbutton.place(anchor="center", relx=0.5, rely=0.53)

        self.detailsbutton = CTkButton(self)
        self.detailsbutton.configure(text="Details", command=self.details, width=100)
        self.detailsbutton.place(anchor="center", relx=0.69, rely=0.53)

        self.savedetailsbutton = CTkButton(self)
        self.savedetailsbutton.configure(text="Help", command=self.help, width=100)
        self.savedetailsbutton.place(anchor="center", relx=0.88, rely=0.53)

        # Plot
        self.plotframe = CTkFrame(self)
        self.plotframe.configure(border_width=1, height=200, width=590)
        self.plotframe.place(anchor="s", relx=0.5, rely=0.99, x=0, y=0)

        self.fig = Figure(figsize = (7.375, 2.5), dpi=80)
        self.fig.set_facecolor("#c1c1c1")
        self.fig.subplots_adjust(top=0.94, bottom=0.18, left=0.1, right=0.96)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotframe)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel("Radius [m]")
        self.ax.set_xlabel("Axis [m]")
        self.ax.grid()
        self.ax.set_facecolor("#ebebeb")

        self.canvas.get_tk_widget().place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)

        self.eps = None
        self.epsc = None
        self.x = []
        self.y = []
        self.details_window = None
        self.details_output = ""
        self.help_window = None

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

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
                thetan = thetae

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
            self.x = concatenate((xC, xD))
            self.y = concatenate((yC, yD))

            # Plot geometry
            self.ax.clear()
            self.ax.plot(self.x, self.y, "black")
            try:
                AR = 2.95        # Aspect ratio
                Rt = sqrt(At/pi)        # Throat radius
                Re = Rt * sqrt(eps)     # Exit radius
                Rc = Rt * sqrt(epsc)    # Chamber radius
                marg = 0.05             # Axis margin

                if ((Le+Lc) / max([Rc, Re]) > AR):
                    xmin = -(marg/2 * (Le + Lc) + Lc)
                    xmax = marg/2 * (Le + Lc) + Le
                    ymax = (1+marg) * (Le + Lc) / AR
                else:
                    xmin = -((1+marg) * max([Rc, Re]) * AR - Le + Lc)/ 2
                    xmax = ((1+marg) * max([Rc, Re]) * AR - Lc + Le)/ 2
                    ymax = (1+marg) * max([Rc, Re])
                
                self.ax.axis([xmin, xmax, 0, ymax])

            except Exception:
                pass
            self.ax.grid()
            self.ax.set_ylabel("Radius [m]")
            self.ax.set_xlabel("Axis [m]")
            self.canvas.draw()

            try:
                self.load_details(At, Le, Lc, Lstar, eps, epsc, RnOvRt, b, thetan, thetae, R1OvRt, R2OvR2max)
            except Exception:
                pass

            # Return values for performance estimation
            return At, Le, thetae
        except Exception:
            pass
    
    def optimizeTn(self):
        gamma = config.gammae
        Me = config.Me
        if self.thetanentry.get() == "":
            thetan = (sqrt((gamma+1)/(gamma-1))*arctan(sqrt((gamma-1)*(Me**2-1)/(gamma+1)))-arctan(sqrt(Me**2-1)))/2
            updateentry(self.thetanentry, thetan / angle_uom(self.thetanuom.get()))
    
    def clear_plot(self):
        self.ax.clear()
        self.ax.grid()
        self.ax.set_ylabel("Radius [m]")
        self.ax.set_xlabel("Axis [m]")
        self.canvas.draw()
        self.x = []
        self.y = []
        self.details_output = ""

    def export_plot(self):
        try:
            if len(self.x) == 0:
                showwarning(title="Warning", message="There is no plot to export")
            else:
                with open(asksaveasfilename(defaultextension=".csv"), "w") as f:
                    f.write(f"{self.x[0]:.7f},{self.y[0]:.7f},0\n")
                    for i in range(1, len(self.x)):
                        if self.x[i] != self.x[i-1]:
                            f.write(f"{self.x[i]:.7f},{self.y[i]:.7f},0\n")
        except Exception:
            pass

    def details(self):
        if self.details_window is None or not self.details_window.winfo_exists():
            self.details_window = ctk.CTkToplevel()
            self.details_window.title("Geometry details")
            self.details_window.configure(width=450, height=480)
            self.details_window.resizable(False, False)
            self.details_window.after(
                201,
                lambda: self.details_window.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            if os.name == "nt":
                self.detailstextbox = ctk.CTkTextbox(
                    self.details_window,
                    height=420,
                    state="disabled",
                    wrap="none",
                    font=("Courier New", 12),
                )
            else:
                self.detailstextbox = ctk.CTkTextbox(
                    self.details_window, height=420, state="disabled", wrap="none", font=("Mono", 12)
                )
            self.detailstextbox.place(relwidth=0.95, relx=0.5, rely=0.025, anchor="n")

            self.savedetailsbutton = CTkButton(self.details_window)
            self.savedetailsbutton.configure(text="Save...", command=self.save_details)
            self.savedetailsbutton.place(anchor="center", relx=0.5, rely=0.95)

            updatetextbox(self.detailstextbox, self.details_output, True)

            self.details_window.after(50, self.details_window.lift)
            self.details_window.after(50, self.details_window.focus)

        else:
            updatetextbox(self.detailstextbox, self.details_output, True)
            self.details_window.lift()
            self.details_window.focus()

    def load_details(self, At, Le, Lc, Lstar, eps, epsc, RnOvRt, b, thetan, thetae, R1OvRt, R2OvR2max):

        Rt = sqrt(At/pi)            # Throat radius
        Re = Rt * sqrt(eps)         # Exit radius
        Rc = Rt * sqrt(epsc)        # Chamber radius
        R1 = R1OvRt * Rt            # Convex circular arc radius
        R2max = (Rc - Rt)/(1-cos(b)) - R1  # Maximum allowed R2
        R2 = R2OvR2max * R2max      # Concave circular arc radius
        m = - tan(b)
        q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
        xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)
        Lcyl = xB + Lc

        self.details_output = f"{self.shape.get()} nozzle\n" + tabulate([
            ["Throat area", "At", f"{10000*At:.2f}", "cm2"],
            [],
            ["Throat radius", "Rt", f"{1000*Rt:.2f}", "mm"],
            ["Chamber radius", "Rc", f"{1000*Rc:.2f}", "mm"],
            ["Exit radius", "Re", f"{1000*Re:.2f}", "mm"],
            [],
            ["Charachteristic chamber length", "L*", f"{1000*Lstar:.2f}", "mm"],
            ["Cylindrical section length", "Lcyl", f"{1000*Lcyl:.2f}", "mm"],
            ["Chamber length", "Lc", f"{1000*Lc:.2f}", "mm"],
            ["Divergent length", "Le", f"{1000*Le:.2f}", "mm"],
            ["Total length", "Le+Lc", f"{1000*(Le+Lc):.2f}", "mm"],
            ["Relative length", "Le/Lc15", f"{100*Le / conical.lc15(At, RnOvRt, eps):.2f}", "%"],
            [],
            ["Contraction angle", "b", f"{degrees(b):.2f}", "deg"],
            ["Initial divergent angle", "Tn", f"{degrees(thetan):.2f}", "deg"],
            ["Final divergent angle", "Te", f"{degrees(thetae):.2f}", "deg"],
            [],
            ["Expansion area ratio", "Ae/At", f"{eps:.2f}", ""],
            ["Contraction area ratio", "Ac/At", f"{epsc:.2f}", ""],
            [],
            ["Convergent convex arc radius", "R1", f"{1000*R1:.2f}", "mm"],
            ["Convergent concave arc radius", "R2", f"{1000*R2:.2f}", "mm"],
            ["Maximum concave arc radius", "R2max", f"{1000*R2max:.2f}", "mm"],
            ["Divergent circular arc radius", "Rn", f"{1000*Rt * RnOvRt:.2f}", "mm"],
        ], tablefmt="plain", floatfmt=".2f")

    def save_details(self):
        try:
            if self.details_output:
                with open(asksaveasfilename(defaultextension=".txt"), "w") as f:
                    f.write(self.details_output)
            else:
                showwarning(title="Warning", message="There are no details to save")
        except Exception:
            pass

    def help(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = ctk.CTkToplevel()
            self.help_window.title("Geometry Help")
            self.help_window.configure(width=610, height=310)
            self.help_window.resizable(False, False)
            self.help_window.after(
                201,
                lambda: self.help_window.iconphoto(
                    False, tk.PhotoImage(file=resource_path("icon.png"))
                ),
            )

            image = CTkImage(Image.open(resource_path("rocketforge/geometry/help.png")), size=(600, 300))
            self.help_image = CTkLabel(self.help_window, text="", image=image)
            self.help_image.place(anchor="center", relx = 0.5, rely = 0.5)

            self.help_window.after(50, self.help_window.lift)
            self.help_window.after(50, self.help_window.focus)

        else:
            self.help_window.lift()
            self.help_window.focus()

    def change_shape(self, shape):

        self.remove_elements()

        if shape == "Thrust-optimized parabolic":
            self.rnovrtlabel.place(anchor="w", relx=0.52, rely=0.18, x=0, y=0)
            self.rnovrtentry.place(anchor="e", relx=0.98, rely=0.18, x=0, y=0)
            self.divergentlengthlabel.place(anchor="w", relx=0.52, rely=0.25, x=0, y=0)
            self.divergentlengthentry.place(anchor="e", relx=529/600, rely=0.25, x=0, y=0)
            self.divergentlengthoptmenu.place(anchor="e", relx=0.98, rely=0.25, x=0, y=0)
            self.thetanlabel.place(anchor="w", relx=0.52, rely=0.32, x=0, y=0)
            self.thetanentry.place(anchor="e", relx=529/600, rely=0.32, x=0, y=0)
            self.thetanoptmenu.place(anchor="e", relx=0.98, rely=0.32, x=0, y=0)
            self.thetaexlabel.place(anchor="w", relx=0.52, rely=0.39, x=0, y=0)
            self.thetaexentry.place(anchor="e", relx=529/600, rely=0.39, x=0, y=0)
            self.thetaexoptmenu.place(anchor="e", relx=0.98, rely=0.39, x=0, y=0)

        if shape == "Truncated ideal contour":
            ...

        if shape == "Conical":
            self.rnovrtlabel.place(anchor="w", relx=0.52, rely=0.18, x=0, y=0)
            self.rnovrtentry.place(anchor="e", relx=0.98, rely=0.18, x=0, y=0)
            self.cleRB.place(anchor="e", relx=0.91, rely=0.25, x=0, y=0)
            self.clelabel.place(anchor="w", relx=0.52, rely=0.25, x=0, y=0)
            self.cleentry.place(anchor="e", relx=529/600, rely=0.25, x=0, y=0)
            self.cleoptmenu.place(anchor="e", relx=0.98, rely=0.25, x=0, y=0)
            self.clfRB.place(anchor="e", relx=0.91, rely=0.32, x=0, y=0)
            self.clflabel.place(anchor="w", relx=0.52, rely=0.32, x=0, y=0)
            self.clfentry.place(anchor="e", relx=0.98, rely=0.32, x=0, y=0)
            self.cthetaRB.place(anchor="e", relx=0.91, rely=0.39, x=0, y=0)
            self.cthetalabel.place(anchor="w", relx=0.52, rely=0.39, x=0, y=0)
            self.cthetaentry.place(anchor="e", relx=529/600, rely=0.39, x=0, y=0)
            self.cthetaoptmenu.place(anchor="e", relx=0.98, rely=0.39, x=0, y=0)

    def remove_elements(self):
        self.rnovrtlabel.place_forget()
        self.rnovrtentry.place_forget()
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

    def loadgeometry(self):
        self.eps = config.eps
        self.epsc = config.epsc
        At, Le, thetae = self.plot()
        geometry = [At, Le, thetae]
        return geometry