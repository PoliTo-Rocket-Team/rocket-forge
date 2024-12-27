from customtkinter import CTkEntry, CTkTextbox
from typing import Any


def update_entry(entry: CTkEntry, value: Any, disabled: bool = False) -> None:
    """
    Updates the contents of a CTkEntry widget.

    Parameters:
        entry (CTkEntry): The entry widget to be updated.
        value (Any): The value to set in the entry. Can be a string, integer, or float.
        disabled (bool): Whether to disable the entry after updating. Defaults to False.

    Returns:
        None
    """
    entry.configure(state="normal")
    entry.delete(0, 200)

    if isinstance(value, str):
        entry.insert(0, value)
    elif isinstance(value, int):
        entry.insert(0, str(value))
    elif isinstance(value, float):
        entry.insert(0, f"{value:.4f}")
    else:
        raise TypeError("Unsupported value type. Expected str, int, or float.")

    if disabled:
        entry.configure(state="disabled")


def update_textbox(textbox: CTkTextbox, value: str, disabled: bool = False) -> None:
    """
    Updates the contents of a CTkTextbox widget.

    Parameters:
        textbox (CTkTextbox): The textbox widget to be updated.
        value (str): The value to set in the textbox.
        disabled (bool): Whether to disable the textbox after updating. Defaults to False.

    Returns:
        None
    """
    textbox.configure(state="normal")
    textbox.delete("0.0", "200.0")
    textbox.insert("0.0", value)

    if disabled:
        textbox.configure(state="disabled")
