import os
import sys
import threading
from utils import log
from receiver import start_server
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
