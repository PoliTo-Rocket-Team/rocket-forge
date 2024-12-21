import os
import re
import tkinter as tk
import numpy as np
from tabulate import tabulate
from contextlib import contextmanager
from tkinter.messagebox import showwarning
import customtkinter as ctk
from customtkinter import CTkEntry, CTkFrame, CTkLabel, CTkCheckBox, CTkOptionMenu, CTkTextbox, CTkProgressBar
from rocketcea.cea_obj_w_units import CEA_Obj
import rocketforge.performance.config as config
from rocketforge.utils.conversions import pressure_uom
from rocketforge.utils.helpers import updateentry, updatetextbox
from rocketforge.performance.theoreticalperf import theoretical


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
        self.textbox = CTkTextbox(self, height=235, state="disabled", wrap="none", font=(font_name, 12))
        self.textbox.place(relwidth=59/60, relx=0.5, rely=0.965, anchor="s")

        # Create a progress bar
        self.progressbar = CTkProgressBar(self)
        self.progressbar.place(relwidth=59/60, relx=0.5, rely=0.99, anchor="s")
        self.progressbar.set(0)

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

    # TODO: Unfortunately the analyses cannot be multithreaded as they rely on the same config variables, in the future we could try fixing this
    def run(self) -> None:
        """
        Executes the nested parameter configuration and performance calculation.
        This method performs the following steps:
        1. Retrieves nested input parameters.
        2. Generates the Cartesian product of the input parameters using `numpy.meshgrid`.
        3. Initializes a results array to store the output for each combination of parameters.
        4. Iterates over all combinations of parameters and runs an analysis.
        5. Stores the results in a dictionary and updates the results array.
        6. Formats the results into a table and updates the GUI textbox with the table.

        The `inputs` dictionary is expected to have the following structure:
        {
            "mr": numpy.ndarray,   # Mixture ratio values
            "pc": numpy.ndarray,   # Chamber pressure values
            "epsc": numpy.ndarray, # Inlet condition values
            "eps": numpy.ndarray   # Exit condition values
        }

        Returns:
            None
        """
        with self._cache_config():
            inputs = self.get_nested_inputs()
            # Generate Cartesian product using meshgrid
            mr, pc, epsc, eps = np.meshgrid(
                inputs["mr"],
                inputs["pc"],
                inputs["epsc"],
                inputs["eps"],
                indexing='ij'
            )
            # Initialize results array with the appropriate shape
            results = np.empty(mr.shape, dtype=object)
            # Iterate over all combinations using a multidimensional index
            for idx,index in enumerate(np.ndindex(mr.shape)):
                self.progressbar.set((idx+1) / mr.size)
                self.progressbar.update_idletasks()

                # Apply the current nested parameters
                config.mr = mr[index]
                config.pc = pc[index]
                config.epsc = epsc[index]

                C = CEA_Obj(
                    oxName=config.ox,
                    fuelName=config.fuel,
                    fac_CR=config.epsc,
                    cstar_units="m/s",
                    pressure_units="Pa",
                    temperature_units="K",
                    sonic_velocity_units="m/s",
                    enthalpy_units="kJ/kg",
                    density_units="kg/m^3",
                    specific_heat_units="J/kg-K",
                )         
                # Manage exit condition
                eps_row = self.rows[3]
                if eps_row["checkbox"].get():
                    eps_dropdown = eps_row["unit_dropdown"].get()
                    if eps_dropdown == "Expansion Area Ratio (Ae/At)":
                        eps_tmp = eps[index]
                    else:
                        if eps_dropdown == "Pressure Ratio (pc/pe)":
                            pe = config.pc / eps[index]
                        else: # Exit pressure
                            # Capture content in parentheses
                            match = re.search(r'\((.*?)\)', eps_dropdown)
                            unit = match.group(1)
                            pe = eps[index] * pressure_uom(unit)
                        eps_tmp = C.get_eps_at_PcOvPe(Pc=config.pc, MR=config.mr, PcOvPe=config.pc / pe)
                else:
                    eps_tmp = eps[index]
                config.eps = eps_tmp

                # Calculate the theoretical performance
                theoretical()
                result_dict = {
                    "mr": config.mr,
                    "pc": config.pc,
                    "epsc": config.epsc,
                    "eps": config.eps,
                    "cstar": config.cstar,
                    "Isp_vac": config.Isp_vac,
                    "Isp_vac_eq": config.Isp_vac_eq,
                    "Isp_vac_fr": config.Isp_vac_fr,
                    "Isp_sl": config.Isp_sl,
                    "Isp_opt": config.Isp_opt,
                    "td_props": config.td_props,
                    "gammae": config.gammae,
                    "Me": config.Me
                }
                results[index] = result_dict
            headers = ["mr", "pc [Pa]", "epsc", "eps", "c* [m/s]", "Isp (SL) [s]", "Isp (opt) [s]", "Isp (vac) [s]", "gamma_e", "M_e"]
            table_data = [
                [result["mr"], result["pc"], result["epsc"], result["eps"], result["cstar"], result["Isp_sl"], result["Isp_opt"], result["Isp_vac"], result["gammae"], result["Me"]]
                for result in results.flatten()
            ]
            
            table = tabulate(table_data, headers, numalign="right")
            updatetextbox(self.textbox, table, disabled=True)
                
    def generate_range(self, step_mode, start, end, step) -> np.ndarray:
        """
        Generate a range of values based on the specified step mode.

        If the step mode is "Step Size", the range will be generated using
        the specified step size, if the step doesn't divide the range evenly,
        the last value will be the first value that is greater than the end
        value.
        If the step mode is "Step No.", the range will be generated using
        the specified number of steps.

        Args:
            step_mode (str): The mode to be used to generate values, either "Step Size" or "Step No.".
            start (float): The starting value of the range.
            end (float): The ending value of the range.
            step (float): The step size or the number of steps, depending on the step mode.
        Returns:
            numpy.ndarray: An array of values generated based on the specified step mode.
        """
        if step_mode == "Step Size":
            if step <= 0:
                showwarning("Invalid Step Size", "Step size must be a positive number.")
                raise ValueError("Invalid Step Size")
            values = np.arange(start, end + step, step)
        elif step_mode == "Step No.":
            if step % 1 != 0:
                showwarning("Invalid Step Count", "Step count must be an integer.")
                raise ValueError("Invalid Step Count")
            if step < 2:
                showwarning("Invalid Step Count", "Step count must be greater than one.")
                raise ValueError("Invalid Step Count")
            values = np.linspace(start, end, int(step))
        return values

    def get_nested_inputs(self) -> dict:
        """
        Get the ranges of nested analysis input values from the GUI fields.

        Returns:
            dict: A dictionary containing the input values for the nested analysis as numpy arrays.
        """
        step_mode = self.inputgrid.grid_slaves(row=0, column=3)[0].get() #TODO: implement choice for each entry
        inputs = {
            "mr":   self.get_nested_mr(step_mode),
            "pc":   self.get_nested_pc(step_mode),
            "epsc": self.get_nested_epsc(step_mode),
            "eps":  self.get_nested_eps(step_mode)
        }
        return inputs

    def get_nested_mr(self, step_mode) -> np.ndarray:
        """
        Get the mixture ratio values for the nested analysis.

        Args:
            step_mode (str): The mode to be used to generate values, either "Step Size" or "Step No.".

        Returns:
            numpy.ndarray: An array of mixture ratio values.
            If the checkbox is not selected, the value from the initial frame (config.mr) is returned.
            If the checkbox is selected, a range of values is generated based on the step_mode, start,
            end, and step inputs.
        """
        row = self.rows[0]
        if row["checkbox"].get(): 
            start, end, step = self.get_inputs(row)
            if row["unit_dropdown"].get() == "alpha":
                start, end = start * config.mr_s, end * config.mr_s
                if step_mode == "Step Size": step *= config.mr_s
            return self.generate_range(step_mode, start, end, step)
        else:
            return np.array([config.mr])
        
    def get_nested_pc(self, step_mode) -> np.ndarray:
        """
        Get the chamber pressure values for the nested analysis.

        Args:
            step_mode (str): The mode to be used to generate values, either "Step Size" or "Step No.".

        Returns:
            numpy.ndarray: An array of chamber pressure values.
            If the checkbox is not selected, the value from the initial frame (config.pc) is returned.
            If the checkbox is selected, a range of values in Pascals is generated based on the
            step_mode, start, end, and step inputs.
        """
        row = self.rows[1]
        if row["checkbox"].get():
            conversion_factor = pressure_uom(row["unit_dropdown"].get())
            start, end, step = self.get_inputs(row)
            start *= conversion_factor
            end *= conversion_factor
            if step_mode == "Step Size": step *= conversion_factor
            return self.generate_range(step_mode, start, end, step)
        else:
            return np.array([config.pc])

    def get_nested_epsc(self, step_mode) -> np.ndarray:
        """
        Get the nozzle inlet conditions for the nested analysis.

        Args:
            step_mode (str): The mode to be used to generate values, either "Step Size" or "Step No.".

        Returns:
            numpy.ndarray: An array of nozzle inlet condition values.
            If the checkbox is not selected, the value from the initial frame (config.epsc) is returned. 
            If "Contraction Area Ratio (Ac/At)" is selected, a range of values is generated based on the
            step_mode, start, end, and step inputs.
            If "Infinite Area Combustor" is selected, an array containing None is returned.
        """
        row = self.rows[2]
        if row["checkbox"].get():
            if row["unit_dropdown"].get() == "Contraction Area Ratio (Ac/At)":
                start, end, step = self.get_inputs(row)
                return self.generate_range(step_mode, start, end, step)
            elif row["unit_dropdown"].get() == "Infinite Area Combustor":
                return np.array([None])
        else:
            return np.array([config.epsc])

    def get_nested_eps(self, step_mode) -> np.ndarray:
        """
        Get the nozzle exit conditions for the nested analysis.

        Args:
            step_mode (str): The mode to be used to generate values, either "Step Size" or "Step No.".

        Returns:
            numpy.ndarray: An array of nozzle exit condition values.
            If the checkbox is not selected, the value from the initial frame (config.eps) is returned. 
            If the checkbox is selected, a range of values is generated based on the step_mode, start,
            end, and step inputs. Note that these values do not necessarily correspond to the contraction
            area ratio.
        """
        row = self.rows[3]
        if row["checkbox"].get():
            start, end, step = self.get_inputs(row)
            return self.generate_range(step_mode, start, end, step)
        else:
            return np.array([config.eps])

    def get_inputs(self, row) -> tuple:
        """
        Extracts and returns the start, end, and step values from the given row.

        Args:
            row (dict): A dictionary containing the entries 'start_entry', 'end_entry', and 'step_entry'.

        Returns:
            tuple: A tuple containing the start, end, and step values as floats.
        """
        start = float(row["start_entry"].get())
        end = float(row["end_entry"].get())
        step = float(row["step_entry"].get())
        return start, end, step
