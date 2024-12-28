import platform


def get_font():
    system = platform.system()
    if system == "Windows":
        return ("Consolas", 12)
    elif system == "Darwin":
        return ("Menlo", 12)
    elif system == "Linux":
        return ("Mono", 12)
    else:
        return ("Courier", 12)