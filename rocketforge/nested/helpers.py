import numpy as np
from tkinter.messagebox import showwarning
from rocketforge.utils.logger import logger
from rocketforge.nested.mapper import mapper


def extract_variable(nestedframe, axis_symbols: str | list[str], key: str = None, slice_index: list = None) -> np.ndarray:
    axis_map = {
        "mr": 0,
        "pc": 1,
        "epsc": 2,
        "eps": 3
    }

    if isinstance(axis_symbols, str):
        axis_symbols = [axis_symbols]
    if slice_index is None:
        slice_index = [0] * nestedframe.results.ndim
    for name in axis_symbols:
        if name not in axis_map:
            raise ValueError(f"Unknown axis name '{name}'. Must be one of: {list(axis_map.keys())}")
        slice_index[axis_map[name]] = slice(None)
    if key is None:
        key = axis_symbols[0] if len(axis_symbols) == 1 else axis_symbols

    sliced = nestedframe.results[tuple(slice_index)]
    try:
        if len(axis_symbols) == 1:
            return np.array([entry[key] for entry in sliced])
        elif len(axis_symbols) == 2:
            return np.array([[entry[key] for entry in row] for row in sliced]).T
        else:
            raise ValueError("only 1D or 2D extraction is supported")
    except KeyError:
        raise KeyError(f"Key '{key}' not found in result dictionaries.")


def get_slice_index(nestedframe, parametric):
    frames = [
        nestedframe.inputframe.mixture_frame,
        nestedframe.inputframe.pressure_frame,
        nestedframe.inputframe.inlet_frame,
        nestedframe.inputframe.outlet_frame
    ]
    modes = [
        nestedframe.inputframe.mixture_mode.get(),
        nestedframe.inputframe.pressure_mode.get(),
        nestedframe.inputframe.inlet_mode.get(),
        nestedframe.inputframe.outlet_mode.get()
    ]

    checked_indices = []
    for j, frame in enumerate(frames):
        indices = [i for i, cb in enumerate(frame.checkboxes) if cb.get()]
        if parametric:
            if len(indices) == 0 or modes[j] == "Variable":
                checked_indices.append([0])
            else:
                checked_indices.append(indices)
        else:
            checked_indices.append(indices[0] if indices else None)
    return checked_indices

def validate_slice_index(slice_index, settings):
    for i in range(len(slice_index)):
        if slice_index[i] is None and settings[list(settings.keys())[i]] != "Variable":
            return (False, mapper.get_name(list(settings.keys())[i]))
    return (True, None)

def abort_plot(log_msg, warn_msg):
    logger.warning(f"Invalid Plot Settings: {log_msg}. Aborting.")
    showwarning("Invalid Plot Settings", warn_msg)
    return False
