import numpy as np
import operator
from functools import reduce
from itertools import product 
from matplotlib import cm
from rocketforge.utils.logger import logger
from rocketforge.utils.conversions import pressure_uom
from rocketforge.nested.mapper import mapper
from rocketforge.nested.helpers import extract_variable, get_slice_index, validate_slice_index, abort_plot

def plot_2D(nestedframe, settings: dict, dependent_symbol: str, param_count: int) -> bool:
    """
    Plots a 2D graph based on the provided settings.

    Args:
        nestedframe: The frame containing plot and data references.
        settings (dict): Dictionary mapping variable/parameter names to their roles.
        dependent_symbol (str): Symbol for the dependent variable.
        param_count (int): Number of parameters being varied.

    Returns:
        bool: True if plot was successful, False otherwise.
    """
    nestedframe.fig.clf()
    nestedframe.ax = nestedframe.fig.add_subplot(111)
    variable_symbol = next(k for k, v in settings.items() if v == "Variable")
    format_2D_plot(nestedframe, variable_symbol, dependent_symbol)
    parametric = param_count > 0
    slice_index = get_slice_index(nestedframe, parametric)
    slice_index_valid, invalid_name = validate_slice_index(slice_index, settings)
    if not slice_index_valid:
        return abort_plot(f"{invalid_name} is not selected", f"Select a value for: {invalid_name}")
    if not parametric:
        logger.info("Plotting non-parametric 2D graph...")
        x = extract_variable(nestedframe, variable_symbol)
        x = [_x / pressure_uom("bar") for _x in x] if variable_symbol == "pc" else x
        y = extract_variable(nestedframe, variable_symbol, dependent_symbol, slice_index)
        nestedframe.ax.plot(x, y, color=cm.YlOrRd(0.5), linewidth=2)
    else:
        logger.info("Plotting parametric 2D graph...")
        param_axis_gen = (i for i, s in enumerate(slice_index) if len(s) > 1) # Gets the axis that stores multiple values
        param_axis = next(param_axis_gen, None)
        if param_axis is None:
            return abort_plot("Not enough values for the parameter", "Select at least two values for the parameter to plot.")
        idxs = product(*slice_index)
        length = reduce(operator.mul, map(len, slice_index), 1)
        colors = [cm.YlOrRd(i) for i in np.linspace(.3, .9, length)]
        nestedframe.ax.set_prop_cycle('color', colors)
        parameter_symbol = next(k for k, v in settings.items() if v == "Parameter")
        param = extract_variable(nestedframe, parameter_symbol)
        param = [p / pressure_uom("bar") for p in param] if parameter_symbol == "pc" else param
        param_uom = f" {mapper.get_uom(parameter_symbol)}" if parameter_symbol == "pc" else ""
        x = extract_variable(nestedframe, variable_symbol)
        x = [_x / pressure_uom("bar") for _x in x] if variable_symbol == "pc" else x
        for i, idx in enumerate(idxs):
            y = extract_variable(nestedframe, variable_symbol, dependent_symbol, list(idx))
            nestedframe.ax.plot(x, y, linewidth=2, label=f"{param[idx[param_axis]]}{param_uom}")
        legend = nestedframe.ax.legend(
            loc='upper right',
            title=mapper.get_name(parameter_symbol),
            title_fontsize='large',
            alignment='left',
            labelcolor='white',
            facecolor='black',
            edgecolor='white',
            framealpha=0.8
        )
        legend.get_title().set_color('white')
    nestedframe.canvas.draw()
    return True
    
def format_2D_plot(nestedframe, variable_symbol: str = None, dependent_symbol: str = None) -> None:
    """
    Formats a 2D plot for a given frame object by adjusting subplot layout, setting axis labels, title, grid, and colors.

    Args:
        nestedframe: The frame containing the figure (`fig`) and axes (`ax`) to be formatted.
        variable_symbol (str, optional): Symbol for the independent variable. If None, uses a default label.
        dependent_symbol (str, optional): Symbol for the dependent variable. If None, uses a default label.
    """
    variable_name = "Independent Variable" if variable_symbol is None else mapper.get_name(variable_symbol)
    variable_uom = f" [{mapper.get_uom(variable_symbol)}]" if variable_symbol else ""
    dependent_name = "Dependent Variable" if dependent_symbol is None else mapper.get_name(dependent_symbol)
    dependent_uom = f" [{mapper.get_uom(dependent_symbol)}]" if dependent_symbol else ""
    nestedframe.fig.subplots_adjust(top=0.9, bottom=0.15, left=0.15, right=0.9)
    nestedframe.ax.set(title=f"{dependent_name} vs {variable_name}",
                xlabel=variable_name + variable_uom,
                ylabel=dependent_name + dependent_uom)
    nestedframe.ax.grid()
    nestedframe.ax.set_facecolor("none")
    for side in ["top", "bottom", "left", "right"]: nestedframe.ax.spines[side].set_color("white")
    nestedframe.ax.tick_params(axis="both", colors="white")
    nestedframe.ax.title.set_color("white")
    nestedframe.ax.title.set_fontsize(14)
    nestedframe.ax.xaxis.label.set_color("white")
    nestedframe.ax.yaxis.label.set_color("white")

def plot_3D(nestedframe, settings: dict, dependent_symbol: str, param_count: int) -> bool:
    """
    Plots a 3D graph based on the provided settings.

    Args:
        nestedframe: The frame containing plot and data references.
        settings (dict): Dictionary mapping variable/parameter names to their roles.
        dependent_symbol (str): Symbol for the dependent variable.
        param_count (int): Number of parameters being varied.

    Returns:
        bool: True if plot was successful, False otherwise.
    """
    nestedframe.fig.clf()
    nestedframe.ax = nestedframe.fig.add_subplot(111, projection='3d')
    variable_symbols = [k for k, v in settings.items() if v == "Variable"]
    format_3D_plot(nestedframe, variable_symbols, dependent_symbol)
    parametric = param_count > 0
    slice_index = get_slice_index(nestedframe, parametric)
    if not validate_slice_index(slice_index, settings):
        return abort_plot(
            f"{mapper.get_name(list(settings.keys())[i])} is not selected",
            f"Select a value for: {mapper.get_name(list(settings.keys())[i])}"
        )
    if not parametric:
        logger.info("Plotting non-parametric 3D graph...")
        X = extract_variable(nestedframe, variable_symbols[0])
        X = [x / pressure_uom("bar") for x in X] if variable_symbols[0] == "pc" else X
        Y = extract_variable(nestedframe, variable_symbols[1])
        Y = [y / pressure_uom("bar") for y in Y] if variable_symbols[1] == "pc" else Y
        X, Y = np.meshgrid(X, Y)
        Z = extract_variable(nestedframe, variable_symbols, dependent_symbol, slice_index)
        col = cm.YlOrRd(0.5)
        nestedframe.ax.plot_surface(X, Y, Z, color=col, edgecolor=col, linewidth=2, alpha=0.6)
    else:
        logger.info("Plotting parametric 3D graph...")
        param_axis_gen = (i for i, s in enumerate(slice_index) if len(s) > 1) # Gets the axis that stores multiple values
        param_axis = next(param_axis_gen, None)
        if param_axis is None:
            return abort_plot("Not enough values for the parameter", "Select at least two values for the parameter to plot.")
        idxs = product(*slice_index)
        length = reduce(operator.mul, map(len, slice_index), 1)
        colors = [cm.YlOrRd(i) for i in np.linspace(.3, .9, length)]
        parameter_symbol = next(k for k, v in settings.items() if v == "Parameter")
        param = extract_variable(nestedframe, parameter_symbol)
        param = [p / pressure_uom("bar") for p in param] if parameter_symbol == "pc" else param
        param_uom = f" {mapper.get_uom(parameter_symbol)}" if parameter_symbol  == "pc" else ""
        X = extract_variable(nestedframe, variable_symbols[0])
        Y = extract_variable(nestedframe, variable_symbols[1])
        X, Y = np.meshgrid(X, Y)
        for i, idx in enumerate(idxs):
            Z = extract_variable(nestedframe, variable_symbols, dependent_symbol, list(idx))
            nestedframe.ax.plot_surface(X, Y, Z, color=colors[i], edgecolor=colors[i], linewidth=2, alpha=0.6, label=f"{param[idx[param_axis]]}{param_uom}")
        legend = nestedframe.ax.legend(
            loc='upper right',
            title=mapper.get_name(parameter_symbol),
            title_fontsize='large',
            alignment='left',
            labelcolor='white',
            facecolor='black',
            edgecolor='white',
            framealpha=0.8
        )
        legend.get_title().set_color('white')
    nestedframe.canvas.draw()
    return True
        
def format_3D_plot(nestedframe, variable_symbols: list[str] = None, dependent_symbol: str = None) -> None:
    """
    Formats a 3D plot for a given frame object by adjusting subplot layout, setting axis labels, title, grid, and colors.

    Args:
        nestedframe: The frame containing the figure (`fig`) and axes (`ax`) to be formatted.
        variable_symbols (list[str], optional): Symbols for the independent variables. If None, uses default labels.
        dependent_symbol (str, optional): Symbol for the dependent variable. If None, uses a default label.
    """
    variable_names = ["Independent Variable 1", "Independent Variable 2"] if variable_symbols is None else [mapper.get_name(sym) for sym in variable_symbols]
    variable_uoms = [f" [{mapper.get_uom(sym)}]" for sym in variable_symbols] if variable_symbols else ["", ""]
    dependent_name = "Dependent Variable" if dependent_symbol is None else mapper.get_name(dependent_symbol)
    dependent_uom = f" [{mapper.get_uom(dependent_symbol)}]" if dependent_symbol else ""
    nestedframe.fig.subplots_adjust(top=0.95, bottom=0, left=0, right=1)
    nestedframe.ax.set(
        title=f"{dependent_name} vs {variable_names[0]} and {variable_names[1]}",
        xlabel=variable_names[0] + variable_uoms[0],
        ylabel=variable_names[1] + variable_uoms[1],
        zlabel=dependent_name + dependent_uom
    )
    nestedframe.ax.grid()
    nestedframe.ax.set_facecolor("none")
    nestedframe.ax.tick_params(axis="both", colors="white")
    nestedframe.ax.title.set_color("white")
    nestedframe.ax.title.set_fontsize(14)
    for axis in [nestedframe.ax.xaxis, nestedframe.ax.yaxis, nestedframe.ax.zaxis]:
        axis.label.set_color('white')
        axis.pane.set_facecolor('white')
        axis.line.set_color('white')
        axis.pane.set_alpha(.05)
