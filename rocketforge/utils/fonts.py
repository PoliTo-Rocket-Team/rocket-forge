import platform
from typing import Tuple


def get_font() -> Tuple[str, int]:
    """
    Determines the default font and size based on the operating system.

    The function selects a monospace font suitable for the current operating system:
    - Windows: Consolas
    - macOS (Darwin): Menlo
    - Linux: Mono
    - Other systems: Courier (default fallback)

    Returns:
        Tuple[str, int]: A tuple containing the font name and font size.
    """
    system = platform.system()

    if system == "Windows":
        return "Consolas", 12

    elif system == "Darwin":
        return "Menlo", 12

    elif system == "Linux":
        return "Mono", 12

    else:
        return "Courier", 12
