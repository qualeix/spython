import sys
import os

# Add server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import other modules
import threading
from receiver import start_server
from utils import log
from upload import start_http_server


def main():
    log("Server starting...")
    try:
        # Start HTTP server as separate thread
        http_thread = threading.Thread(target=start_http_server, daemon=True)
        http_thread.start()

        # Start the main receiver server
        start_server()
    except KeyboardInterrupt:
        log("Server shutting down...")
    except Exception as e:
        log(f"Server fatal error: {e}", "ERROR")


if __name__ == "__main__":
    main()
