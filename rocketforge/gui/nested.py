import tkinter as tk
from contextlib import contextmanager
import customtkinter as ctk
import rocketforge.mission.config as config
from customtkinter import CTkEntry, CTkFrame, CTkLabel, CTkCheckBox, CTkOptionMenu, CTkTextbox
import rocketforge.performance.config as config
from rocketforge.utils.conversions import pressure_uom
from rocketforge.utils.helpers import updateentry, updatetextbox
import os


class NestedFrame(CTkFrame):
    # Unicode values for symbols
    unicodealpha = "\u03b1"
    unicodesquared = "\u00b2"
    unicodecdot = "\u00b7"

    def __init__(self, master=None, **kw):
        super(NestedFrame, self).__init__(master, **kw)

        # Create a top frame for the nested analysis section
        self.topframe = CTkFrame(self)
        self.topframe.configure(border_width=0, height=28, width=590)
        self.topframe.place(anchor="n", relx=0.5, rely=0.01, x=0, y=0)

        # Create a top label for the nested analysis section
        self.toplabel = CTkLabel(self.topframe, text="Nested Analysis")
        self.toplabel.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)

        # Create the input grid frame
        self.inputgrid = CTkFrame(self, border_width=1)
        self.inputgrid.place(anchor="n", relx=0.5, rely=0.03 + 28/600, relwidth=59/60) # Horrible but it works for now

        # Configure grid layout
        self.inputgrid.grid_columnconfigure(0, weight=0, minsize=100)
        for i in range(1,5):
            self.inputgrid.grid_columnconfigure(i, weight=1)

        # First row headers
        headers = ["Variable Parameter", "Start Value", "End Value", ["Step Size", "Step No."], "Unit/Mode"]
        for i, header in enumerate(headers):
            if i != 3:
                label = CTkLabel(self.inputgrid, text=header)
                label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            else:
                stepdropdown = CTkOptionMenu(self.inputgrid, values=header)
                stepdropdown.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        # Define the row data for the input grid
        self.rows = []
        row_data = [
            ("Mixture Ratio",               ["O/F", "alpha"]),
            ("Chamber Pressure",            ["MPa", "bar", "Pa", "psia", "atm"]),
            ("Nozzle Inlet Conditions",     ["Contraction Area Ratio (Ac/At)",
                                             "Infinite Area Combustor"]),
            ("Nozzle Exit Conditions",      ["Exit Pressure (MPa)",
                                             "Exit Pressure (bar)",
                                             "Exit Pressure (Pa)",
                                             "Exit Pressure (psia)",
                                             "Exit Pressure (atm)",
                                             "Expansion Area Ratio (Ae/At)",
                                             "Pressure Ratio (pc/pe)"])
        ]  # Format: ("Parameter", ["Units"])
        plotoptions = [
            "Specific Impulse (Is)",
            "Chamber Temperature (Tc)",
            "Characteristic Velocity (c*)",
            "Thrust Coefficient (Cf)"
        ]

        # Populate the input grid with rows
        for i, (label, units) in enumerate(row_data):
            row = self.create_row(i+1, label, units, plotoptions)
            self.rows.append(row)


        # Create output textbox
        font_name = "Courier New" if os.name == "nt" else "Mono"
        self.textbox = CTkTextbox(self, height=246, state="disabled", wrap="none", font=(font_name, 12))
        self.textbox.place(relwidth=59/60, relx=0.5, rely=0.99, anchor="s")

        self.configure(border_width=1, corner_radius=0, height=480, width=600)

    def create_row(self, row_num, label, units, plotoptions) -> dict:
        """
        Create a row in the input grid with the specified label and units.

        Args:
            row_num (int): The row number in the grid.
            label (str): The label for the row.
            units (list): A list of units for the unit dropdown menu.
            plotoptions (list): A list of options for the plot dropdown menu.
        Returns:
            dict: A dictionary containing the widgets in the row.
        """
        row = {}
        row["checkbox"] = CTkCheckBox(self.inputgrid, text=label, command=lambda: self.toggle_row(row))
        row["checkbox"].grid(row=row_num, column=0, padx=5, pady=5, sticky="w")

        row["start_entry"] = CTkEntry(self.inputgrid, justify="right", placeholder_text="0")
        row["start_entry"].grid(row=row_num, column=1, padx=5, pady=5, sticky="ew")

        row["end_entry"] = CTkEntry(self.inputgrid, justify="right", placeholder_text="0")
        row["end_entry"].grid(row=row_num, column=2, padx=5, pady=5, sticky="ew")

        row["step_entry"] = CTkEntry(self.inputgrid, justify="right", placeholder_text="0")
        row["step_entry"].grid(row=row_num, column=3, padx=5, pady=5, sticky="ew")

        row["unit_dropdown"] = CTkOptionMenu(self.inputgrid, values=units)
        row["unit_dropdown"].grid(row=row_num, column=4, padx=5, pady=5, sticky="ew")

        # row["plot_dropdown"] = CTkOptionMenu(self.inputgrid, values=plotoptions)
        # row["plot_dropdown"].grid(row=row_num, column=5, padx=5, pady=5, sticky="ew")

        # Initially disable all fields
        self.toggle_row(row, False)

        return row

    def toggle_row(self, row, state=None):
        """
        Toggle the state of widgets in a given row based on the state of
        a checkbox.

        Args:
            row (dict): A dictionary containing widgets, with one key being "checkbox".
            state (bool, optional): The desired state to set for the widgets. If None,
            the state is determined by the checkbox's current state.
        """
        if state is None:
            state = row["checkbox"].get()

        for key, widget in row.items():
            if key != "checkbox":
                if state:
                    widget.configure(state="normal")
                else:
                    widget.configure(state="disabled")

    @contextmanager
    def _cache_config(self):
        """
        Cache the current configuration values and restore them after the
        nested analysis, even if the nested analysis fails.

        Yields:
            None
        """
        # Setup: save the current config values
        cached_mr = config.mr
        cached_pc = config.pc
        cached_epsc = config.epsc
        cached_eps = config.eps
        cached_cstar = config.cstar
        cached_Isp_vac = config.Isp_vac
        cached_Isp_vac_eq = config.Isp_vac_eq
        cached_Isp_vac_fr = config.Isp_vac_fr
        cached_Isp_sl = config.Isp_sl
        cached_Isp_opt = config.Isp_opt
        cached_td_props = config.td_props
        cached_gammae = config.gammae
        cached_Me = config.Me
        try:
            # Give control back to the code inside the 'with' block
            yield
        finally:
            # Teardown: restore the original config values
            # this code runs even if an exception is raised within the 'with' block
            config.mr = cached_mr
            config.pc = cached_pc
            config.epsc = cached_epsc
            config.eps = cached_eps
            config.cstar = cached_cstar
            config.Isp_vac = cached_Isp_vac
            config.Isp_vac_eq = cached_Isp_vac_eq
            config.Isp_vac_fr = cached_Isp_vac_fr
            config.Isp_sl = cached_Isp_sl
            config.Isp_opt = cached_Isp_opt
            config.td_props = cached_td_props
            config.gammae = cached_gammae
            config.Me = cached_Me

