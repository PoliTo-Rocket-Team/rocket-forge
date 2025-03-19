import sys
import logging

class _Logger:
    # Define color codes
    COLORS = {
        'DEBUG': '\033[94m',   # Blue
        'INFO': '\033[92m',    # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[95m' # Magenta
    }
    RESET = '\033[0m'  # Reset color

    def __init__(self):
        self.original_stdout = sys.stdout
        self.logger = logging.getLogger('RF_Logger')
        self.logger.setLevel(logging.DEBUG)
        
        # Create console handler with a higher log level
        ch = logging.StreamHandler(self.original_stdout)
        ch.setLevel(logging.DEBUG)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter(">>> %(asctime)s.%(msecs)03d [%(levelname)s] - %(message)s", "%H:%M:%S")
        ch.setFormatter(self.ColoredFormatter(formatter))
        
        # Add the handlers to the logger
        self.logger.addHandler(ch)

    def ColoredFormatter(self, formatter):
        # Define a custom formatter class
        class CustomFormatter(logging.Formatter):
            # Define custom format method that wraps the standard format with color codes
            def format(self, record):
                log_color = _Logger.COLORS.get(record.levelname, _Logger.RESET)
                formatted_record = formatter.format(record)
                return f"{log_color}{formatted_record}{_Logger.RESET}"
        return CustomFormatter()

# Create a single instance of the logger
logger = _Logger().logger
logger.info("Logger initialized.")