import sys
import os


def resource_path(relative_path: str) -> str:
    """
    Obtains the absolute path of a file or resource relative to the main executable's path.

    This is particularly useful when packaging applications with PyInstaller, where resources
    are extracted to a temporary directory.

    Parameters:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        # sys._MEIPASS is set by PyInstaller to the path of the temporary directory
        # where the application's assets are extracted.
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
