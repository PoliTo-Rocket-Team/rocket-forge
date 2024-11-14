import tkinter as tk
import customtkinter as ctk
import rocketforge.mission.config as config
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel
from rocketforge.utils.conversions import pressure_uom
from rocketforge.utils.helpers import updateentry, updatetextbox


class NestedFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(NestedFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(text="Nested Analysis")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        self.configure(border_width=1, corner_radius=0, height=480, width=600)