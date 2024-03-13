import tkinter as tk
from tkinter.messagebox import showwarning
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu, CTkButton
import rocketforge.geometry.top as top
from rocketforge.utils.conversions import angle_uom, area_uom, length_uom
from rocketforge.utils.helpers import updateentry
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.throatareaentry.place(anchor="w", relx=0.2, rely=0.22, x=0, y=0)

        self.throatareaoptmenu = CTkOptionMenu(self)
        self.throatareauom = tk.StringVar(value="m2")
        self.throatareaoptmenu.configure(
            values=["m2", "cm2", "mm2", "sq in", "sq ft"], variable=self.throatareauom, width=100
        )
        self.throatareaoptmenu.place(anchor="w", relx=0.3, rely=0.22, x=0, y=0)

        self.rnovrtlabel = CTkLabel(self)
        self.rnovrtlabel.configure(text="Rn/Rt:")
        self.rnovrtlabel.place(anchor="w", relx=0.05, rely=0.27, x=0, y=0)

        self.rnovrtentry = CTkEntry(self)
        self.rnovrtentry.configure(placeholder_text="0", width=200)
        self.rnovrtentry.place(anchor="w", relx=0.2, rely=0.27, x=0, y=0)
        updateentry(self.rnovrtentry, "0.382")

        self.divergentlengthlabel = CTkLabel(self)
        self.divergentlengthlabel.configure(text="Divergent length:")
        self.divergentlengthlabel.place(anchor="w", relx=0.05, rely=0.32, x=0, y=0)

        self.customle = ctk.IntVar(value=0)

        self.customleCB = ctk.CTkCheckBox(
            self,
            text = "",
            variable=self.customle,
            onvalue=1,
            offvalue=0,
            width=25
        )
        self.customleCB.place(anchor="e", relx=0.205, rely=0.32)

        self.divergentlengthentry = CTkEntry(self)
        self.divergentlengthentry.configure(placeholder_text="0", width=100)
        self.divergentlengthentry.place(anchor="w", relx=0.2, rely=0.32, x=0, y=0)
        updateentry(self.divergentlengthentry, "0.8")

        self.divergentlengthoptmenu = CTkOptionMenu(self)
        self.divergentlengthuom = tk.StringVar(value="m")
        self.divergentlengthoptmenu.configure(
            values=["Le/Lc15", "m", "cm", "mm", "in", "ft"], variable=self.divergentlengthuom, width=100
        )
        self.divergentlengthoptmenu.place(anchor="w", relx=0.3, rely=0.32, x=0, y=0)

        self.thetanlabel = CTkLabel(self)
        self.thetanlabel.configure(text="Initial parabola angle:")
        self.thetanlabel.place(anchor="w", relx=0.05, rely=0.37, x=0, y=0)

        self.customthetan = ctk.IntVar(value=0)

        self.customthetanCB = ctk.CTkCheckBox(
            self,
            text = "",
            variable=self.customthetan,
            onvalue=1,
            offvalue=0,
            width=25
        )
        self.customthetanCB.place(anchor="e", relx=0.205, rely=0.37)

        self.thetanentry = CTkEntry(self)
        self.thetanentry.configure(placeholder_text="0", width=100)
        self.thetanentry.place(anchor="w", relx=0.2, rely=0.37, x=0, y=0)

        self.thetanoptmenu = CTkOptionMenu(self)
        self.thetanuom = tk.StringVar(value="deg")
        self.thetanoptmenu.configure(
            values=["deg", "rad"], variable=self.thetanuom, width=100
        )
        self.thetanoptmenu.place(anchor="w", relx=0.3, rely=0.37, x=0, y=0)

        self.thetaexlabel = CTkLabel(self)
        self.thetaexlabel.configure(text="Final parabola angle:")
        self.thetaexlabel.place(anchor="w", relx=0.05, rely=0.42, x=0, y=0)

        self.customthetaex = ctk.IntVar(value=0)

        self.thetaexCB = ctk.CTkCheckBox(
            self,
            text = "",
            variable=self.customthetaex,
            onvalue=1,
            offvalue=0,
            width=25
        )
        self.thetaexCB.place(anchor="e", relx=0.205, rely=0.42)

        self.thetaexentry = CTkEntry(self)
        self.thetaexentry.configure(placeholder_text="0", width=100)
        self.thetaexentry.place(anchor="w", relx=0.2, rely=0.42, x=0, y=0)

        self.thetaexoptmenu = CTkOptionMenu(self)
        self.thetaexuom = tk.StringVar(value="deg")
        self.thetaexoptmenu.configure(
            values=["deg", "rad"], variable=self.thetaexuom, width=100
        )
        self.thetaexoptmenu.place(anchor="w", relx=0.3, rely=0.42, x=0, y=0)

        self.epslabel = CTkLabel(self)
        self.epslabel.configure(text="Expansion Area Ratio:")
        self.epslabel.place(anchor="w", relx=0.05, rely=0.47, x=0, y=0)

        self.epsentry = CTkEntry(self)
        self.epsentry.configure(width=200, state="disabled")
        self.epsentry.place(anchor="w", relx=0.2, rely=0.47, x=0, y=0)
        updateentry(self.epsentry, "Undefined", True)

        self.plotbutton = CTkButton(self)
        self.plotbutton.configure(text="Update plot", command=self.plot)
        self.plotbutton.place(anchor="center", relx=0.5, rely=0.53)

        self.plotframe = CTkFrame(self)
        self.plotframe.configure(border_width=5, height=300, width=950)
        self.plotframe.place(anchor="center", relx=0.5, rely=0.77, x=0, y=0)

        self.fig = Figure(figsize = (11.875, 3.75), dpi=80)
        self.fig.set_facecolor("#c1c1c1")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotframe)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis([-1, 1, 0, 2/3])
        self.ax.grid()
        self.ax.set_facecolor("#ebebeb")
        self.canvas.get_tk_widget().pack()

        self.eps = None

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)

    def plot(self):
        try:
            At = float(self.throatareaentry.get()) * area_uom(self.throatareauom.get())
            RnOvRt = float(self.rnovrtentry.get())

            if not (self.customle.get() == 0 and self.customthetaex.get() == 1 and self.customthetan.get() == 1):
                if self.divergentlengthuom.get() == "Le/Lc15":
                    if self.eps != None:
                        Le = float(self.divergentlengthentry.get()) * top.lc15(At, RnOvRt, self.eps)
                    else:
                        showwarning(title="Warning", message="Please define the area ratio and run the simulation first.")
                        raise Exception
                else:
                    Le = float(self.divergentlengthentry.get()) * length_uom(self.divergentlengthuom.get())

            if self.customthetaex.get() == 0 and self.customthetan.get() == 0 and self.eps != None:
                showwarning(title="Warning", message="Please define at least one angle")

            elif self.customthetaex.get() == 1 and self.customthetan.get() == 0 and self.eps != None:
                thetae = float(self.thetaexentry.get()) * angle_uom(self.thetaexuom.get())
                x, y, thetan = top.get_geometry01(self.eps, thetae, Le, At, RnOvRt)
                updateentry(self.thetanentry, thetan / angle_uom(self.thetanuom.get()))
                updateentry(self.epsentry, self.eps, True)

            elif self.customthetaex.get() == 0 and self.customthetan.get() == 1 and self.eps != None:
                thetan = float(self.thetanentry.get()) * angle_uom(self.thetanuom.get())
                x, y, thetae = top.get_geometry10(self.eps, thetan, Le, At, RnOvRt)
                updateentry(self.thetaexentry, thetae / angle_uom(self.thetaexuom.get()))
                updateentry(self.epsentry, self.eps, True)

            elif self.customthetaex.get() == 1 and self.customthetan.get() == 1:
                thetae = float(self.thetaexentry.get()) * angle_uom(self.thetaexuom.get())
                thetan = float(self.thetanentry.get()) * angle_uom(self.thetanuom.get())
                if self.customle.get() == 1 and self.divergentlengthuom.get() != "Le/Lc15":
                    x, y, eps = top.get_geometry11(thetae, thetan, Le, At, RnOvRt)
                    updateentry(self.epsentry, eps, True)
                else:
                    x, y, Le = top.get_geometry111(thetae, thetan, self.eps, At, RnOvRt)
                    if self.divergentlengthuom.get() == "Le/Lc15":
                        updateentry(self.divergentlengthentry, Le / top.lc15(At, RnOvRt, self.eps))
                    else:
                        updateentry(self.divergentlengthentry, Le / length_uom(self.divergentlengthuom.get()))
                    updateentry(self.epsentry, self.eps, True)

            else:
                showwarning(title="Warning", message="Please define the area ratio and run the simulation first.")

            self.ax.clear()
            self.ax.plot(x, y, 'black')
            # self.ax.axis([-Lc, Le, 0, max(1.1 * Re, 1.1 * Rc, (Le + Lc) / 3)])
            self.ax.axis([-Le, Le, 0, 2 * Le / 3])
            self.ax.grid()
            self.canvas.draw()

            return At, Le, thetae
        
        except Exception:
            pass

    def loadgeometry(self, eps):
        self.eps = eps
        At, Le, thetae = self.plot()
        geometry = [At, Le, thetae]
        return geometry