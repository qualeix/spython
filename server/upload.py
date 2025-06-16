import os
import config
import functools
from utils import log
from http.server import HTTPServer, SimpleHTTPRequestHandler


HOST = config.LISTEN_ALL
HTTP_PORT = config.HTTP_PORT


class QuietHandler(SimpleHTTPRequestHandler):
    """Suppress normal request logging"""
    def log_request(self, code = "-", size = "-"):
        pass


def start_http_server():
    try:
        # Compute the absolute path to “tools”
        base_dir = os.path.dirname(os.path.abspath(__file__))
        tools_dir = os.path.join(base_dir, "tools")

        if not os.path.exists(tools_dir):
            log(f"Tools directory not found", "ERROR", "upload")
            return

        # Create a handler that serves only from tools_dir
        handler = functools.partial(QuietHandler, directory=tools_dir)

        # Create and configure server
        httpd = HTTPServer((HOST, HTTP_PORT), handler)
        httpd.timeout = 1  # Allows for a graceful shutdown
        log(f"HTTP server running, serving: {tools_dir[-12:]}", module="upload")

        # Run the server
        while True:
            httpd.handle_request()
    except PermissionError:
        log(f"Permission denied for HTTP port {HTTP_PORT}", "ERROR", "upload")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            log(f"HTTP port {HTTP_PORT} already in use", "ERROR", "upload")
        else:
            log(f"HTTP server error: {e}", "ERROR", "upload")
    except Exception as e:
        log(f"Unexpected HTTP server error: {e}", "ERROR", "upload")
