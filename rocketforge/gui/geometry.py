import tkinter as tk
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton, CTkImage
import rocketforge.performance.config as config
import rocketforge.thermal.config as tconf
import rocketforge.geometry.top as top
import rocketforge.geometry.tic as tic
import rocketforge.geometry.conical as conical
import rocketforge.geometry.convergent as convergent
from rocketforge.utils.conversions import angle_uom, area_uom, length_uom
from rocketforge.utils.helpers import update_entry, update_textbox
from rocketforge.utils.resources import resource_path
from rocketforge.utils.fonts import get_font
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from numpy import *
from tabulate import tabulate
import pyvista as pv


class GeometryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(GeometryFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        CTkLabel(self.topframe, text="Chamber Geometry").place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        CTkLabel(self, text="Throat area").place(anchor="w", relx=0.02, rely=0.11, x=0, y=0)
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
        CTkLabel(self, text="R1/Rt").place(anchor="w", relx=0.02, rely=0.18, x=0, y=0)
        self.r1ovrtentry = CTkEntry(self)
        self.r1ovrtentry.configure(placeholder_text="0", width=118)
        self.r1ovrtentry.place(anchor="e", relx=0.48, rely=0.18, x=0, y=0)
        update_entry(self.r1ovrtentry, "1.5")

        CTkLabel(self, text="Chamber length").place(anchor="w", relx=0.02, rely=0.25, x=0, y=0)
        self.chamberlengthentry = CTkEntry(self)
        self.chamberlengthentry.configure(placeholder_text="0", width=59)
        self.chamberlengthentry.place(anchor="e", relx=229/600, rely=0.25, x=0, y=0)
        update_entry(self.chamberlengthentry, "1.0")

        self.chamberlengthoptmenu = CTkOptionMenu(self)
        self.chamberlengthuom = tk.StringVar(value="L* [m]")
        self.chamberlengthoptmenu.configure(
            values=["L* [m]", "m", "cm", "mm", "in", "ft"], variable=self.chamberlengthuom, width=59
        )
        self.chamberlengthoptmenu.place(anchor="e", relx=0.48, rely=0.25, x=0, y=0)

        CTkLabel(self, text="Contraction angle").place(anchor="w", relx=0.02, rely=0.32, x=0, y=0)
        self.bentry = CTkEntry(self)
        self.bentry.configure(placeholder_text="0", width=59)
        self.bentry.place(anchor="e", relx=229/600, rely=0.32, x=0, y=0)
        update_entry(self.bentry, "30")

        self.boptmenu = CTkOptionMenu(self)
        self.buom = tk.StringVar(value="deg")
        self.boptmenu.configure(
            values=["deg", "rad"], variable=self.buom, width=59
        )
        self.boptmenu.place(anchor="e", relx=0.48, rely=0.32, x=0, y=0)

        CTkLabel(self, text="R2/R2max").place(anchor="w", relx=0.02, rely=0.39, x=0, y=0)
        self.r2ovr2maxentry = CTkEntry(self)
        self.r2ovr2maxentry.configure(placeholder_text="0", width=118)
        self.r2ovr2maxentry.place(anchor="e", relx=0.48, rely=0.39, x=0, y=0)
        update_entry(self.r2ovr2maxentry, "0.5")

        CTkLabel(self, text="Contraction Area Ratio").place(anchor="w", relx=0.02, rely=0.46, x=0, y=0)
        self.epscentry = CTkEntry(self)
        self.epscentry.configure(width=118, state="disabled")
        self.epscentry.place(anchor="e", relx=0.48, rely=0.46, x=0, y=0)
        update_entry(self.epscentry, "Undefined", True)

        # Divergent Section
        CTkLabel(self, text="Nozzle shape").place(anchor="w", relx=0.52, rely=0.11, x=0, y=0)

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
        update_entry(self.rnovrtentry, "0.382")

        CTkLabel(self, text="Expansion Area Ratio").place(anchor="w", relx=0.52, rely=0.46, x=0, y=0)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(width=118, state="disabled")
        self.epsentry.place(anchor="e", relx=0.98, rely=0.46, x=0, y=0)
        update_entry(self.epsentry, "Undefined", True)

        # Thrust-optimized parabolic (TOP)
        self.divergentlengthlabel = CTkLabel(self)
        self.divergentlengthlabel.configure(text="Divergent length")
        self.divergentlengthlabel.place(anchor="w", relx=0.52, rely=0.25, x=0, y=0)

        self.divergentlengthentry = CTkEntry(self)
        self.divergentlengthentry.configure(placeholder_text="0", width=59)
        self.divergentlengthentry.place(anchor="e", relx=529/600, rely=0.25, x=0, y=0)
        update_entry(self.divergentlengthentry, "0.8")

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
        update_entry(self.thetaexentry, "8")

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
        CTkButton(
            self, text="Update plot", command=self.plot, width=100
        ).place(anchor="center", relx=0.12, rely=0.53)

        CTkButton(
            self, text="Advanced...", command=self.advanced, width=100
        ).place(anchor="center", relx=0.31, rely=0.53)

        CTkButton(
            self, text="Export plot...", command=self.export_plot, width=100
        ).place(anchor="center", relx=0.5, rely=0.53)

        CTkButton(
            self, text="Details", command=self.details, width=100
        ).place(anchor="center", relx=0.69, rely=0.53)

        CTkButton(
            self, text="Toggle 3D", command=self.toggle_3d, width=100
        ).place(anchor="center", relx=0.88, rely=0.53)

        # Plot
        self.plot3dframe = CTkFrame(self)
        self.plot3dframe.configure(border_width=1, height=200, width=590)

        self.plot3dlabel = ctk.CTkLabel(self.plot3dframe, text="")
        self.plot3dlabel.place(anchor="center", relx=0.5, rely=0.5)
        self.view_angle = 0.0
        self.distance = 4.0
        self.enable_3d = False

        self.plotter = pv.Plotter(off_screen=True)
        self.plotter.window_size = [588, 198]
        self.plotter.set_background('#c1c1c1')

        CTkButton(
            self.plot3dframe, text="↑", command=self.decrease_distance,
            width=35, height=35, font=("Arial", 20, "bold")
        ).place(anchor="center", relx=0.88, rely=0.65)
    
        CTkButton(
            self.plot3dframe, text="↓", command=self.increase_distance,
            width=35, height=35, font=("Arial", 20, "bold")
        ).place(anchor="center", relx=0.88, rely=0.85)

        CTkButton(
            self.plot3dframe, text="↺", command=self.decrease_view_angle,
            width=35, height=35, font=("Arial", 20, "bold")
        ).place(anchor="center", relx=0.95, rely=0.75)
    
        CTkButton(
            self.plot3dframe, text="↻", command=self.increase_view_angle,
            width=35, height=35, font=("Arial", 20, "bold")
        ).place(anchor="center", relx=0.81, rely=0.75)

        CTkButton(
            self.plot3dframe, text="↻", command=self.increase_view_angle,
            width=35, height=35, font=("Arial", 20, "bold")
        ).place(anchor="center", relx=0.81, rely=0.75)

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

        self.x = []
        self.y = []
        self.advancedwindow = None
        self.details_window = None
        self.details_output = ""
        self.help_window = None
        self.ptscirc = 360
        self.ptspar = 100

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def toggle_3d(self):
        if self.enable_3d:
            self.plot3dframe.place_forget()
            self.plotframe.place(anchor="s", relx=0.5, rely=0.99)
        else:
            self.plotframe.place_forget()
            self.plot3dframe.place(anchor="s", relx=0.5, rely=0.99)
        self.enable_3d = not self.enable_3d
    
    def increase_distance(self):
        self.distance *= 1.1
        self.update_3d_plot()
    
    def decrease_distance(self):
        self.distance /= 1.1
        self.update_3d_plot()

    def increase_view_angle(self):
        self.view_angle += radians(15)
        self.update_3d_plot()
    
    def decrease_view_angle(self):
        self.view_angle -= radians(15)
        self.update_3d_plot()

    def plot(self):
        if config.thrust != None:
            if config.At > 0.01:
                update_entry(self.throatareaentry, config.At)
                self.throatareauom.set("m2")
            else:
                update_entry(self.throatareaentry, config.At * 10000)
                self.throatareauom.set("cm2")

        # Compute divergent section
        try:
            if config.eps == None:
                showwarning(title="Warning", message="Please define the area ratio and run the simulation first.")
                raise Exception
            eps = config.eps
            update_entry(self.epsentry, eps, True)

            At = float(self.throatareaentry.get()) * area_uom(self.throatareauom.get())
            RnOvRt = float(self.rnovrtentry.get())

            # Thrust-optimized parabolic (TOP)
            if self.shape.get() == "Thrust-optimized parabolic":
                tconf.shape = 1

                if self.divergentlengthuom.get() == "Le/Lc15":
                    Le = float(self.divergentlengthentry.get()) * conical.lc15(At, RnOvRt, eps)
                else:
                    Le = float(self.divergentlengthentry.get()) * length_uom(self.divergentlengthuom.get())

                thetan = float(self.thetanentry.get()) * angle_uom(self.thetanuom.get())
                thetae = float(self.thetaexentry.get()) * angle_uom(self.thetaexuom.get())

                if thetan <= thetae:
                    showwarning(title="Warning", message="Final parabola angle must be greater than initial parabola angle")
                    raise Exception
            
                xD, yD = top.get(At, RnOvRt, Le, thetan, thetae, eps, self.ptscirc, self.ptspar)
            
            # Truncated ideal contour (TIC)
            if self.shape.get() == "Truncated ideal contour":
                ...

            # Conical nozzle
            if self.shape.get() == "Conical":
                tconf.shape = 0

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
                
                update_entry(self.cleentry, Le / length_uom(self.cleuom.get()))
                update_entry(self.clfentry, Lf)
                update_entry(self.cthetaentry, thetae / angle_uom(self.cthetauom.get()))
                thetan = thetae

                xD, yD = conical.get(At, RnOvRt, eps, Le, thetae, self.ptscirc)

        except Exception:
            xD = []
            yD = []

        # Compute convergent section
        try:
            if config.epsc == None:
                raise Exception
            epsc = float(config.epsc)
            update_entry(self.epscentry, epsc, True)
            
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

            xC, yC = convergent.get(At, R1OvRt, Lc, b, R2OvR2max, epsc, self.ptscirc)
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
                if self.details_window is not None:
                    update_textbox(self.detailstextbox, self.details_output, True)
            except Exception:
                pass

            config.At = At
            config.Le = Le
            config.theta_e = thetae

            Rt = sqrt(At/pi)
            Re = Rt * sqrt(eps)
            Rc = Rt * sqrt(epsc)
            R1 = R1OvRt * Rt
            R2max = (Rc - Rt)/(1-cos(b)) - R1
            R2 = R2OvR2max * R2max
            m = - tan(b)
            q = Rt + R1 * (1 - cos(b) - tan(b) * sin(b))
            xB = (Rc - R2*(1-cos(b)) - q)/m - R2 * sin(b)
            tconf.L_cyl = xB + Lc
            tconf.L_c = Lc
            tconf.L_e = Le
            tconf.RnOvRt = RnOvRt
            tconf.R1OvRt = R1OvRt
            tconf.R2OvR2max = R2OvR2max
            tconf.b = degrees(b)
            tconf.theta = degrees(thetan)
            tconf.thetan = degrees(thetan)
            tconf.thetae = degrees(thetae)

            self.update_3d_plot()

        except Exception:
            pass

    def update_3d_plot(self):
        try:
            Le = tconf.L_e
            Lc = tconf.L_c
            Re = sqrt(config.At * config.eps)
            Rc = sqrt(config.At * config.epsc)
            chamber = self.get_chamber()
            self.plotter.camera_position = [
                ((Le - Lc) / 2 + self.distance * max((Re, Rc)) * sin(self.view_angle), 0, self.distance * max((Re, Rc)) * cos(self.view_angle)),
                ((Le - Lc) / 2, 0, 0),
                (0, 1, 0)
            ]
            self.plotter.add_mesh(chamber, color="#727472")
            image_array = self.plotter.screenshot(return_img=True)
            photo = CTkImage(Image.fromarray(uint8(image_array)), size=(588, 198))
            self.plot3dlabel.configure(image=photo)
        except Exception:
            pass

    def get_chamber(self):
        ntheta = 180
        theta = linspace(0, 2*pi, ntheta)
        X = outer(self.x, ones((1, ntheta)))
        Y = outer(self.y, cos(theta))
        Z = outer(self.y, sin(theta))
        return pv.StructuredGrid(X, Y, Z)

    def estimate_Tn(self):
        gamma = config.gammae
        Me = config.Me
        if self.thetanentry.get() == "":
            thetan = (sqrt((gamma+1)/(gamma-1))*arctan(sqrt((gamma-1)*(Me**2-1)/(gamma+1)))-arctan(sqrt(Me**2-1)))/2
            update_entry(self.thetanentry, thetan / angle_uom(self.thetanuom.get()))
    
    def advanced(self):
        if self.advancedwindow is None or not self.advancedwindow.winfo_exists():
            self.advancedwindow = ctk.CTkToplevel()
            self.advancedwindow.title("Advanced settings")
            self.advancedwindow.configure(width=280, height=200)
            self.advancedwindow.resizable(False, False)
            self.advancedwindow.after(
                201,
                lambda: self.advancedwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
                ),
            )

            self.advanced_frame = CTkFrame(
                self.advancedwindow, border_width=3, corner_radius=0, width=280, height=200,
            )
            self.advanced_frame.grid(column=0, row=0)

            CTkLabel(self.advanced_frame, text="Pts/circle").place(anchor="w", relx=0.1, rely=1/6)
            self.ptscircentry = CTkEntry(self.advanced_frame, placeholder_text="0", width=80)
            self.ptscircentry.place(anchor="e", relx=0.9, rely=1/6)
            update_entry(self.ptscircentry, self.ptscirc)

            CTkLabel(self.advanced_frame, text="Points per parabola").place(anchor="w", relx=0.1, rely=2/6)
            self.ptsparentry = CTkEntry(self.advanced_frame, placeholder_text="0", width=80)
            self.ptsparentry.place(anchor="e", relx=0.9, rely=2/6)
            update_entry(self.ptsparentry, self.ptspar)

            CTkLabel(self.advanced_frame, text="3D plot view angle [°]").place(anchor="w", relx=0.1, rely=3/6)
            self.viewangleentry = CTkEntry(self.advanced_frame, placeholder_text="0", width=80)
            self.viewangleentry.place(anchor="e", relx=0.9, rely=3/6)
            update_entry(self.viewangleentry, degrees(self.view_angle))

            CTkLabel(self.advanced_frame, text="3D plot distance factor").place(anchor="w", relx=0.1, rely=4/6)
            self.distanceentry = CTkEntry(self.advanced_frame, placeholder_text="0", width=80)
            self.distanceentry.place(anchor="e", relx=0.9, rely=4/6)
            update_entry(self.distanceentry, self.distance)

            CTkButton(
                self.advanced_frame, text="Set", command=self.set_advanced, width=90
            ).place(anchor="center", relx=0.5, rely=5.2/6)

            self.advancedwindow.after(50, self.advancedwindow.lift)
            self.advancedwindow.after(50, self.advancedwindow.focus)

        else:
            self.advancedwindow.lift()
            self.advancedwindow.focus()

    def set_advanced(self):
        try:
            self.ptscirc = int(float(self.ptscircentry.get()))
            self.ptspar = int(float(self.ptsparentry.get()))
            self.view_angle = radians(float(self.viewangleentry.get()))
            self.distance = float(self.distanceentry.get())
            self.advancedwindow.destroy()
            self.plot()
        except Exception:
            pass

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
            self.details_window.protocol("WM_DELETE_WINDOW", self.details_window.withdraw)
            self.details_window.after(
                201,
                lambda: self.details_window.iconphoto(
                    False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
                ),
            )

            self.details_frame = CTkFrame(
                self.details_window, border_width=3, corner_radius=0, width=450, height=480,
            )
            self.details_frame.grid(column=0, row=0)

            self.detailstextbox = ctk.CTkTextbox(
                self.details_frame, state="disabled", wrap="none", font=get_font()
            )
            self.detailstextbox.place(relwidth=0.95, relheight=13/15, relx=0.5, rely=0.025, anchor="n")

            CTkButton(
                self.details_frame, text="Save...", command=self.save_details
            ).place(anchor="center", relx=0.5, rely=0.95)

            CTkButton(
                self.details_frame, text="Help", command=self.help, width=59
            ).place(anchor="center", relx=0.85, rely=0.95)

            update_textbox(self.detailstextbox, self.details_output, True)

            self.details_window.after(50, self.details_window.lift)
            self.details_window.after(50, self.details_window.focus)

        else:
            update_textbox(self.detailstextbox, self.details_output, True)
            self.details_window.deiconify()
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
            ["Characteristic chamber length", "L*", f"{1000*Lstar:.2f}", "mm"],
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
                    False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
                ),
            )

            self.help_frame = CTkFrame(
                self.help_window, border_width=3, corner_radius=0, width=610, height=310,
            )
            self.help_frame.grid(column=0, row=0)

            image = CTkImage(Image.open(resource_path("rocketforge/resources/help.png")), size=(600, 300))
            CTkLabel(
                self.help_frame, text="", image=image
            ).place(anchor="center", relx = 0.5, rely = 0.5)

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
