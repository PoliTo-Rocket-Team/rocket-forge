#!/usr/bin/python3
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFont, CTkFrame, CTkLabel, CTkOptionMenu


class InitialFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kw):
        super(InitialFrame, self).__init__(master, **kw)
        self.initialtopframe = CTkFrame(self)
        self.initialtopframe.configure(border_width=5, height=100, width=950)
        self.initialtoplabel = CTkLabel(self.initialtopframe)
        self.initialtoplabel.configure(
            font=CTkFont("Sans", 36, None, "roman", False, False), text="Initial Data"
        )
        self.initialtoplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.initialtopframe.place(anchor="n", relx=0.5, rely=0.02, x=0, y=0)

        self.enginenamelabel = CTkLabel(self)
        self.enginenamelabel.configure(text="Engine name:")
        self.enginenamelabel.place(anchor="w", relx=0.05, rely=0.25, x=0, y=0)

        self.enginenameentry = CTkEntry(self)
        self.enginenameentry.configure(placeholder_text="Engine name...", width=200)
        self.enginenameentry.place(anchor="w", relx=0.2, rely=0.25, x=0, y=0)

        self.enginedescriptionlabel = CTkLabel(self)
        self.enginedescriptionlabel.configure(text="Engine description:")
        self.enginedescriptionlabel.place(anchor="w", relx=0.05, rely=0.3, x=0, y=0)

        self.enginedescriptionentry = CTkEntry(self)
        self.enginedescriptionentry.configure(
            placeholder_text="Engine description...", width=700
        )
        self.enginedescriptionentry.place(anchor="w", relx=0.2, rely=0.3, x=0, y=0)

        self.enginedefinitionlabel = CTkLabel(self)
        self.enginedefinitionlabel.configure(text="Engine Definition")
        self.enginedefinitionlabel.place(anchor="w", relx=0.05, rely=0.2, x=0, y=0)

        self.pclabel = CTkLabel(self)
        self.pclabel.configure(text="Chamber Pressure:")
        self.pclabel.place(anchor="w", relx=0.05, rely=0.35, x=0, y=0)

        self.pcentry = CTkEntry(self)
        self.pcentry.configure(placeholder_text=0, width=100)
        self.pcentry.place(anchor="w", relx=0.2, rely=0.35, x=0, y=0)
        
        self.pcoptmenu = CTkOptionMenu(self)
        self.pcuom = tk.StringVar(value="bar")
        self.pcoptmenu.configure(
            values=["MPa", "bar", "Pa", "psia", "atm"], variable=self.pcuom, width=100
        )
        self.pcoptmenu.place(anchor="w", relx=0.3, rely=0.35, x=0, y=0)

        self.configure(border_width=5, corner_radius=0, height=750, width=1000)


if __name__ == "__main__":
    root = tk.Tk()
    widget = InitialFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
