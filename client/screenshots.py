import io
import config
import hashlib
import time
from PIL import ImageGrab
from utils import log, get_timestamp
from sender import send_screenshot


# Global state for change detection
last_screenshot_hash = None


def take_screenshot():
    try:
        screenshot = ImageGrab.grab()

        # Convert to JPEG in memory
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format='JPEG', quality=config.SCREENSHOT_QUALITY)
        return img_bytes.getvalue()
    except Exception as e:
        log(f"Screenshot capture failed: {e}", "ERROR", "screenshots")
        return None


def get_image_hash(image_bytes):
    """Generate hash for image change detection"""
    return hashlib.md5(image_bytes).hexdigest()


def start_screenshot_monitoring():
    global last_screenshot_hash
    log("Screenshot monitoring started", module="screenshots")

    try:
        while True:
            image_data = take_screenshot()
            if not image_data:
                time.sleep(config.SCREENSHOT_INTERVAL)
                continue

            # Check if screen changed
            current_hash = get_image_hash(image_data)
            if config.SCREENSHOT_ONLY_ON_CHANGE and current_hash == last_screenshot_hash:
                log("Screenshot unchanged, skipping", "DEBUG", "screenshots")
            else:
                timestamp = get_timestamp(sanitized=True)
                send_screenshot(image_data, timestamp)
                last_screenshot_hash = current_hash

            # Wait for next capture
            time.sleep(config.SCREENSHOT_INTERVAL)
    except KeyboardInterrupt:
        log("Screenshot monitoring stopped", module="screenshots")
    except Exception as e:
        log(f"Screenshot monitoring failed: {e}", "ERROR", "screenshots")
