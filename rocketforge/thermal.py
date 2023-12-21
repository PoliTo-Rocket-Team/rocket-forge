#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel


class ThermalFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(ThermalFrame, self).__init__(master, **kw)
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=5, height=100, width=950)
        self.toplabel = CTkLabel(self.topframe)
        self.toplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Thermal Analysis"
        )
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.topframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)


if __name__ == "__main__":
    root = tk.Tk()
    widget = ThermalFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
