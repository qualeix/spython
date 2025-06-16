import os
import config
from datetime import datetime


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)
    log(f"Created/verified directory: {path}", "DEBUG", "filesystem")
    return path


def log(message, level="INFO", module=None):
    # Color support for terminals
    if config.LOG_COLORS:
        colors = {
            "DEBUG": "\033[94m",  # Blue
            "INFO": "\033[92m",  # Green
            "SUCCESS": "\033[96m",  # Cyan
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "ENDC": "\033[0m"  # Reset
        }
    else:
        colors = {level: "" for level in ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"]}
        colors["ENDC"] = ""

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

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module_prefix = f"{module} | " if module else ""

    # Apply color if supported
    color_prefix = colors.get(level, "")
    color_suffix = colors["ENDC"]

    print(f"{color_prefix}[{level}] {timestamp} : {module_prefix}{message}{color_suffix}")
