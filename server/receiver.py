import socket
import json
import config
from filesystem import handle_data
from utils import log
from decryption import decrypt_data


HOST, PORT = config.LISTEN_ALL, config.LISTENING_PORT


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.settimeout(config.SOCKET_TIMEOUT)
        s.listen()
        log(f"Server started on {HOST}:{PORT}", module="receiver")

        try:
            while True:
                try:
                    conn, addr = s.accept()
                    conn.settimeout(config.SOCKET_TIMEOUT)
                    client_ip = addr[0]
                    log(f"Connection from {client_ip}", "DEBUG", "receiver")

                    try:
                        # Read first byte (encryption marker)
                        encryption_flag = conn.recv(1)
                        if not encryption_flag:
                            continue

                        # Read remaining data
                        raw_data = b''
                        while True:
                            chunk = conn.recv(config.BUFFER_SIZE)
                            if not chunk:
                                break
                            raw_data += chunk

                        if not raw_data:
                            log("Empty payload received", "DEBUG", "receiver")
                            continue

                        # Handle decryption if needed
                        if encryption_flag == b"\x01":  # Encrypted
                            decrypted = decrypt_data(raw_data)
                            if decrypted is None:
                                log("Decryption failed, skipping payload", "WARNING", "receiver")
                                continue
                            processed_data = decrypted
                        else:  # plaintext
                            processed_data = raw_data

                        # Check for screenshot marker
                        if b"\n\nBINARY\n\n" in processed_data:
                            # Screenshot handling
                            try:
                                header_part, binary_part = processed_data.split(b"\n\nBINARY\n\n", 1)
                                header = json.loads(header_part.decode('utf-8'))

                                # Create payload
                                payload = {
                                    "type": header["type"],
                                    "timestamp": header["timestamp"],
                                    "binary_data": binary_part
                                }
                                handle_data(client_ip, payload)
                            except json.JSONDecodeError:
                                log("Invalid screenshot header", "WARNING", "receiver")
                            except Exception as e:
                                log(f"Screenshot processing error: {str(e)}", "ERROR", "receiver")
                        else:
                            # Regular JSON payload
                            try:
                                payload = json.loads(processed_data.decode('utf-8'))
                                handle_data(client_ip, payload)
                            except json.JSONDecodeError:
                                log("Invalid JSON payload", "WARNING", "receiver")
                            except Exception as e:
                                log(f"Payload processing error: {str(e)}", "ERROR", "receiver")

                    except socket.timeout:
                        log(f"Connection with {client_ip} timed out", "WARNING", "receiver")
                    except Exception as e:
                        log(f"Error processing data from {client_ip}: {e}", "ERROR", "receiver")
                    finally:
                        conn.close()

                except socket.timeout:
                    continue
                except Exception as e:
                    log(f"Error accepting connection: {e}", "ERROR", "receiver")

        except KeyboardInterrupt:
            log("Server shutting down...")
        except Exception as e:
            log(f"Server runtime error: {e}", "ERROR", "receiver")
