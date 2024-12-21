import sys, os


def resource_path(relative_path: str) -> str:
    """
    This function is used to obtain the absolute path of a file or resource relative to the main executable's path
    """
    try:
        """
        sys._MEIPASS is set by the PyInstaller module
        When a PyInstaller application is run, this variable contains the path to the temporary directory where the application's assets are extracted
        """
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
