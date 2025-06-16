import os
import time
import config
from utils import log


def manage_screenshots_storage(client_dir):
    try:
        screenshot_dir = os.path.join(client_dir, "screenshots")

        # 1. Age-based cleanup
        if config.SCREENSHOT_RETENTION_DAYS > 0:
            current_time = time.time()
            for filename in os.listdir(screenshot_dir):
                filepath = os.path.join(screenshot_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > config.SCREENSHOT_RETENTION_DAYS * 86400:
                    os.remove(filepath)
                    log(f"Purged old screenshot: {filename}", "DEBUG", "management")

        # 2. Count-based cleanup
        if config.MAX_SCREENSHOTS_PER_CLIENT > 0:
            screenshots = sorted(os.listdir(screenshot_dir), key=lambda f: os.path.getmtime(os.path.join(screenshot_dir, f)))
            while len(screenshots) > config.MAX_SCREENSHOTS_PER_CLIENT:
                oldest = screenshots.pop(0)
                os.remove(os.path.join(screenshot_dir, oldest))
                log(f"Purged excess screenshot: {oldest}", "DEBUG", "management")

        # 3. Size-based cleanup
        if config.MAX_SCREENSHOT_DIR_SIZE_MB > 0:
            total_size = 0
            files = []
            for filename in os.listdir(screenshot_dir):
                filepath = os.path.join(screenshot_dir, filename)
                file_size = os.path.getsize(filepath)
                total_size += file_size
                files.append((filepath, os.path.getmtime(filepath), file_size))

            # Convert to MB
            total_size_mb = total_size / (1024 * 1024)

            if total_size_mb > config.MAX_SCREENSHOT_DIR_SIZE_MB:
                # Sort by oldest first
                files.sort(key=lambda x: x[1])
                while total_size_mb > config.MAX_SCREENSHOT_DIR_SIZE_MB and files:
                    oldest = files.pop(0)
                    os.remove(oldest[0])
                    total_size_mb -= oldest[2] / (1024 * 1024)
                    log(f"Purged large screenshot: {os.path.basename(oldest[0])}", "DEBUG", "management")

    except Exception as e:
        log(f"Storage management error: {e}", "ERROR", "management")
