import os
import config
from datetime import datetime


# Color support for terminals
if config.LOG_COLORS:
    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "SUCCESS": "\033[96m",  # Cyan
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "ENDC": "\033[0m"       # Reset
    }
else:
    COLORS = {level: "" for level in ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"]}
    COLORS["ENDC"] = ""


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message, level="INFO", module=None):
    """
    Log messages with filtering based on level and module
    :param message: Log message content
    :param level: Log level (DEBUG, INFO, SUCCESS, WARNING, ERROR)
    :param module: Module name for filtering
    """
    # Validate log level
    valid_levels =["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"]
    if level not in valid_levels:
        level = "INFO"

    # Define log level severity
    levels = {
        "DEBUG": 0,
        "INFO": 1,
        "SUCCESS": 2,
        "WARNING": 3,
        "ERROR": 4
    }

    # Skip logs below configured level
    if levels.get(level, 1) < levels.get(config.LOG_LEVEL, 1):
        return

    # Skip logs from silent modules
    if module and module in config.SILENT_MODULES:
        return

    timestamp = get_timestamp()
    module_prefix = f"{module} | " if module else ""

    color_prefix = COLORS.get(level, "")
    color_suffix = COLORS["ENDC"]

    print(f"{color_prefix}[{level}] {timestamp} : {module_prefix}{message}{color_suffix}")


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)
    log(f"Created/verified directory: {path}", "DEBUG", "filesystem")
    return path
