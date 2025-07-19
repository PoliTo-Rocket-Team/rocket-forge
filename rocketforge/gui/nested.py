# Standard library
import re
import threading
from contextlib import contextmanager
from operator import countOf

# Tkinter
import tkinter as tk
from tkinter.messagebox import showwarning

# Third-party
import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from rocketcea.cea_obj_w_units import CEA_Obj
from tabulate import tabulate

# CustomTkinter
from customtkinter import (
    CTkButton,
    CTkCheckBox,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkOptionMenu,
    CTkProgressBar,
    CTkTextbox
)

# Project-specific
import rocketforge.performance.config as config
from rocketforge.performance.theoreticalperf import theoretical
from rocketforge.utils.conversions import pressure_uom
from rocketforge.utils.custom.CTkScrollableFrameUpdated import CTkScrollableFrameUpdated
from rocketforge.utils.fonts import get_font
from rocketforge.utils.helpers import update_textbox
from rocketforge.utils.logger import logger
from rocketforge.utils.resources import resource_path
from rocketforge.nested.helpers import abort_plot, extract_variable
from rocketforge.nested.mapper import mapper
from rocketforge.nested.nestedplot import format_2D_plot, plot_2D, plot_3D



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

        # Create a plot button
        self.plotbutton = ctk.CTkButton(
            self, text="Plot...", command=self.plot_window, width=100, height=28
        ).place(relx=0.993, rely=0.475, anchor="ne")
        self.plotwindow = None

        # Create output textbox
        self.textbox = CTkTextbox(self, height=204, state="disabled", wrap="none", font=get_font())
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

    def run(self) -> None:
        """
        Starts the analysis thread if it is not already running.

        This method checks if the 'analysis_thread' attribute exists and if it is alive.
        If the thread does not exist or is not alive, it creates a new thread to run
        the 'run_analysis' method and starts it.

        Returns:
            None
        """
        if not hasattr(self, 'analysis_thread') or not self.analysis_thread.is_alive():
            self.analysis_thread = threading.Thread(target=self.run_analysis, daemon=True)
            self.analysis_thread.start()

    # Unfortunately the analyses cannot be multithreaded as they rely on the same config variables, in the future we could try fixing this
    def run_analysis(self) -> None:
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
            self.results = np.empty(mr.shape, dtype=object)
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
                self.results[index] = result_dict

            #    The results are stored in a 4D array, where each axis corresponds
            #    to a different variable (mr, pc, epsc, eps).
            #    Each element of the array is a dictionary containing the variables
            #    and the results of the analysis executed with those variables.
            #
            #               ,-'‾‾,-'‾‾,-'‾‾,-'|                ,-'‾‾,-'‾‾,-'‾‾,-'|  
            #           ,-'‾‾,-'‾‾,-'‾‾,-'|   |            ,-'‾‾,-'‾‾,-'‾‾,-'|   |  
            #       ,-'‾‾,-'‾‾,-'‾‾,-'|   |,-'|        ,-'‾‾,-'‾‾,-'‾‾,-'|   |,-'|  
            #      |‾‾‾‾|‾‾‾‾|‾‾‾‾|   |,-'|   |       |‾‾‾‾|‾‾‾‾|‾‾‾‾|   |,-'|   |   
            #      |____|____|____|,-'|   |,-'|       |____|____|____|,-'|   |,-'|  
            #    pc|    |    |    |   |,-'|   |     pc|    |    |    |   |,-'|   |  
            #      |____|____|____|,-'|   |,-'        |____|____|____|,-'|   |,-'   
            #      |    |    |    |   |,-' epsc       |    |    |    |   |,-' epsc  
            #      |____|____|____|,-'                |____|____|____|,-'           
            #             mr                                 mr
            #               ----------------eps---------------->

            headers = ["mr", "pc [Pa]", "epsc", "eps", "c* [m/s]", "Isp (SL) [s]", "Isp (opt) [s]", "Isp (vac) [s]", "gamma_e", "M_e"]
            table_data = [
                [result["mr"], result["pc"], result["epsc"], result["eps"], result["cstar"], result["Isp_sl"], result["Isp_opt"], result["Isp_vac"], result["gammae"], result["Me"]]
                for result in self.results.flatten()
            ]

            table = tabulate(table_data, headers, numalign="right")
            update_textbox(self.textbox, table, disabled=True)

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
            d = max(
                len(str(start).rstrip('0').split('.')[-1]),
                len(str(end).rstrip('0').split('.')[-1]),
                len(str(step).rstrip('0').split('.')[-1])
                )
            return np.round(np.arange(start, end + step, step), decimals=d)

        elif step_mode == "Step No.":
            if step % 1 != 0:
                showwarning("Invalid Step Count", "Step count must be an integer.")
                raise ValueError("Invalid Step Count")
            if step < 2:
                showwarning("Invalid Step Count", "Step count must be greater than one.")
                raise ValueError("Invalid Step Count")
            return np.linspace(start, end, int(step))

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
    
    def plot_window(self):
        if not hasattr(self, "results") or not isinstance(self.results, np.ndarray):
            logger.warning("Trying to open plot window without running the analysis.")
            showwarning("No Results", "Run the nested analysis first.")
            return
        if self.results.shape == (1,1,1,1):
            logger.warning("Trying to open plot window with insufficient data.")
            showwarning("Insufficient Data", "At least one parameter must be selected.")
            return
            
        if self.plotwindow is None or not self.plotwindow.winfo_exists():
            plot_types = ["Variable", "Constant", "Parameter"]
            uoms = ["O/F", "bar", "Ac/At", "Ae/At"]

            # Create a new window for the plot
            self.plotwindow = ctk.CTkToplevel()
            self.plotwindow.title("Nested Analysis Plot")
            self.plotwindow.geometry("1000x600")
            self.plotwindow.resizable(True, True)
            self.plotwindow.after(
                201,
                lambda: self.plotwindow.iconphoto(
                    False, tk.PhotoImage(file=resource_path("rocketforge/resources/icon.png"))
                ),
            )

            # Input Frame (left)
            self.inputframe = CTkFrame(self.plotwindow, width=340, border_width=1)
            self.inputframe.pack(side="left", fill="y", padx=5, pady=5)
            self.inputframe.grid_propagate(False)
            self.inputframe.grid_columnconfigure(0, weight=1, uniform="col")
            self.inputframe.grid_columnconfigure(1, weight=1, uniform="col")

            # Dependent Variable
            self.inputframe.dependent_label = CTkLabel(
                self.inputframe, text="Dependent Variable"
            ).grid(row=0, column=0, columnspan=2, padx=10, pady=(5,0), sticky="ew")
            self.inputframe.dependent_dropdown = CTkOptionMenu(self.inputframe, values=list(mapper.get_all_names("dependent")))
            self.inputframe.dependent_dropdown.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

            # Mixture Ratio
            CTkLabel(
                self.inputframe, text=mapper.get_name('mr') + f" [{mapper.get_uom('mr')}]"
            ).grid(row=2, column=0, padx=5, pady=(5,0), sticky="ew")
            
            self.inputframe.mixture_mode = CTkOptionMenu(
                self.inputframe,
                values=plot_types,
                command= lambda mode: self.update_selection_frame(self.inputframe.mixture_frame, mode)
            )
            self.inputframe.mixture_mode.grid(row=2, column=1, padx=5, pady=(5,0), sticky="ew")
            self.inputframe.mixture_mode.set("Constant")
            
            self.inputframe.mixture_frame = CTkScrollableFrameUpdated(self.inputframe, height=66)
            self.inputframe.mixture_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
            mr_values = extract_variable(self, "mr")
            self.inputframe.mixture_frame.checkboxes = []
            for i, val in enumerate(mr_values):
                def on_toggle(index=i):
                    cb_clicked = self.inputframe.mixture_frame.checkboxes[index]
                    is_selected = cb_clicked.get()
                    if self.inputframe.mixture_mode.get() == "Constant" and is_selected:
                        for j, cb in enumerate(self.inputframe.mixture_frame.checkboxes):
                            if j != index:
                                cb.deselect()
                cb = CTkCheckBox(
                    self.inputframe.mixture_frame,
                    text=str(round(val, 3)),
                    checkbox_height=16,
                    checkbox_width=16,
                    height=16,
                    command=on_toggle
                )
                cb.pack(anchor="w", padx=5, pady=(5,2) if i == 0 else (2,5) if i == len(mr_values)-1 else 2)
                self.inputframe.mixture_frame.checkboxes.append(cb)
                if i == 0:
                    cb.select()
                if len(mr_values) == 1:
                    cb.configure(state="disabled")
                    self.inputframe.mixture_mode.configure(state="disabled")

            # Chamber Pressure
            CTkLabel(
                self.inputframe, text=mapper.get_name('pc') + f" [{mapper.get_uom('pc')}]"
            ).grid(row=5, column=0, padx=5, pady=(5,0), sticky="ew")
            
            self.inputframe.pressure_mode = CTkOptionMenu(
                self.inputframe,
                values=plot_types,
                command= lambda mode: self.update_selection_frame(self.inputframe.pressure_frame, mode)
            )
            self.inputframe.pressure_mode.grid(row=5, column=1, padx=5, pady=(5,0), sticky="ew")
            self.inputframe.pressure_mode.set("Constant")

            self.inputframe.pressure_frame = CTkScrollableFrameUpdated(self.inputframe, height=66)
            self.inputframe.pressure_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

            pc_values = extract_variable(self, "pc")
            self.inputframe.pressure_frame.checkboxes = []
            for i, val in enumerate(pc_values):
                def on_toggle(index=i):
                    cb_clicked = self.inputframe.pressure_frame.checkboxes[index]
                    is_selected = cb_clicked.get()
                    if self.inputframe.pressure_mode.get() == "Constant" and is_selected:
                        for j, cb in enumerate(self.inputframe.pressure_frame.checkboxes):
                            if j != index:
                                cb.deselect()
                cb = CTkCheckBox(
                    self.inputframe.pressure_frame,
                    text=str(round(val / pressure_uom(uoms[1]), 1)),
                    checkbox_height=16,
                    checkbox_width=16,
                    height=16,
                    command=on_toggle
                )
                cb.pack(anchor="w", padx=5, pady=(5,2) if i == 0 else (2,5) if i == len(pc_values)-1 else 2)
                self.inputframe.pressure_frame.checkboxes.append(cb)
                if i == 0:
                    cb.select()
                if len(pc_values) == 1:
                    cb.configure(state="disabled")
                    self.inputframe.pressure_mode.configure(state="disabled")

            # Nozzle Inlet Conditions
            CTkLabel(
                self.inputframe, text=mapper.get_name('epsc') + f" [{mapper.get_uom('epsc')}]"
            ).grid(row=8, column=0, padx=5, pady=(5,0), sticky="ew")

            self.inputframe.inlet_mode = CTkOptionMenu(
                self.inputframe,
                values=plot_types,
                command= lambda mode: self.update_selection_frame(self.inputframe.inlet_frame, mode)
            )
            self.inputframe.inlet_mode.grid(row=8, column=1, padx=5, pady=(5,0), sticky="ew")
            self.inputframe.inlet_mode.set("Constant")

            self.inputframe.inlet_frame = CTkScrollableFrameUpdated(self.inputframe, height=66)
            self.inputframe.inlet_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

            epsc_values = extract_variable(self, "epsc")
            self.inputframe.inlet_frame.checkboxes = []
            for i, val in enumerate(epsc_values):
                def on_toggle(index=i):
                    cb_clicked = self.inputframe.inlet_frame.checkboxes[index]
                    is_selected = cb_clicked.get()
                    if self.inputframe.inlet_mode.get() == "Constant" and is_selected:
                        for j, cb in enumerate(self.inputframe.inlet_frame.checkboxes):
                            if j != index:
                                cb.deselect()
                cb = CTkCheckBox(
                    self.inputframe.inlet_frame,
                    text=str(round(val, 3)),
                    checkbox_height=16,
                    checkbox_width=16,
                    height=16,
                    command=on_toggle
                )
                cb.pack(anchor="w", padx=5, pady=(5,2) if i == 0 else (2,5) if i == len(epsc_values)-1 else 2)
                self.inputframe.inlet_frame.checkboxes.append(cb)
                if i == 0:
                    cb.select()
                if len(epsc_values) == 1:
                    cb.configure(state="disabled")
                    self.inputframe.inlet_mode.configure(state="disabled")

            # Nozzle Exit Conditions 
            CTkLabel(
                self.inputframe, text=mapper.get_name('eps') + f" [{mapper.get_uom('eps')}]"
            ).grid(row=11, column=0, padx=5, pady=(5,0), sticky="ew")

            self.inputframe.outlet_mode = CTkOptionMenu(
                self.inputframe,
                values=plot_types,
                command= lambda mode: self.update_selection_frame(self.inputframe.outlet_frame, mode)
            )
            self.inputframe.outlet_mode.grid(row=11, column=1, padx=5, pady=(5,0), sticky="ew")
            self.inputframe.outlet_mode.set("Constant")

            self.inputframe.outlet_frame = CTkScrollableFrameUpdated(self.inputframe, height=66)
            self.inputframe.outlet_frame.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

            eps_values = extract_variable(self, "eps")
            self.inputframe.outlet_frame.checkboxes = []
            for i, val in enumerate(eps_values):
                def on_toggle(index=i):
                    cb_clicked = self.inputframe.outlet_frame.checkboxes[index]
                    is_selected = cb_clicked.get()
                    if self.inputframe.outlet_mode.get() == "Constant" and is_selected:
                        for j, cb in enumerate(self.inputframe.outlet_frame.checkboxes):
                            if j != index:
                                cb.deselect()
                cb = CTkCheckBox(
                    self.inputframe.outlet_frame,
                    text=str(round(val, 3)),
                    checkbox_height=16,
                    checkbox_width=16,
                    height=16,
                    command=on_toggle
                )
                cb.pack(anchor="w", padx=5, pady=(5,2) if i == 0 else (2,5) if i == len(eps_values)-1 else 2)
                self.inputframe.outlet_frame.checkboxes.append(cb)
                if i == 0:
                    cb.select()
                if len(eps_values) == 1:
                    cb.configure(state="disabled")
                    self.inputframe.outlet_mode.configure(state="disabled")
            self.inputframe.grid_rowconfigure(14, weight=2)

            self.inputframe.plotbutton = CTkButton(self.inputframe, text="Plot", command=self.plot_wrap, height=28)
            self.inputframe.plotbutton.grid(row=15, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
            
            # Plot frame (right)
            self.plotframe = CTkFrame(self.plotwindow)
            self.plotframe.configure(border_width=1)
            self.plotframe.pack(side="left", fill="both", expand=True, padx=(0,5), pady=5)

            self.fig = Figure(figsize=(5,5), dpi=80)
            self.fig.set_facecolor("none")
            self.fig.patch.set_facecolor("none")

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotframe)
            self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=5, pady=5)
            self.canvas.get_tk_widget().configure(bg="#212121")

            self.ax = self.fig.add_subplot(111)
            format_2D_plot(self)

            self.plotwindow.after(100, self.plotwindow.lift)
            self.plotwindow.after(100, self.plotwindow.focus)
            
            self.plotwindow.lift()
            self.plotwindow.focus()
        else:
            self.plotwindow.lift()
            self.plotwindow.focus()
    
    def plot_wrap(self):
        if self.plot():
            logger.info("Plotting successful.")
        else:
            logger.warning("Plotting aborted due to invalid settings or errors.")
        
    def plot(self):
        logger.info("Plotting...")
        try:
            settings = {
                "mr": self.inputframe.mixture_mode.get(),
                "pc": self.inputframe.pressure_mode.get(),
                "epsc": self.inputframe.inlet_mode.get(),
                "eps": self.inputframe.outlet_mode.get()
            }

            var_count = countOf(settings.values(), "Variable")
            param_count = countOf(settings.values(), "Parameter")
            dependent_symbol = mapper.get_symbol(self.inputframe.dependent_dropdown.get())
            
            if var_count == 0:
                return abort_plot("No variable selected", "Select at least one variable to plot.")

            if var_count > 2:
                return abort_plot("Too many variables selected", "One or two variables must be selected for plotting.")

            if param_count > 1:
                return abort_plot("Too many parametric variables selected", "Only one variable can be selected for parametric plotting.")
            
            if var_count == 1:
                return plot_2D(self, settings, dependent_symbol, param_count)
            
            if var_count == 2:
                return plot_3D(self, settings, dependent_symbol, param_count)
        except Exception as e:
            logger.error(f"Error during plotting: {e}")
            raise

    def update_selection_frame(self, frame, mode):
        first_selected_found = False
        for checkbox in frame.winfo_children():
            if isinstance(checkbox, CTkCheckBox):
                if mode == "Variable":
                    checkbox.configure(state="disabled")
                elif mode == "Parameter":
                    checkbox.configure(state="normal")
                elif mode == "Constant":
                    checkbox.configure(state="normal")
                    if not first_selected_found and checkbox.get():
                        first_selected_found = True
                    else:
                        checkbox.deselect()
   
