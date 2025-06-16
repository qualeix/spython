import config
import base64
from utils import log
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag


# Generate key from config string
KEY = base64.b64decode(config.ENCRYPTION_KEY)
if len(KEY) not in [16, 24, 32]:
    log("Decryption key must be the same as the clients'", "WARNING", "decryption")


def decrypt_data(encrypted):
    """Decrypt data using AES-GCM"""
    try:
        # Validate minimum length
        if len(encrypted) < 28:  # 12 nonce + 16 tag
            log("Invalid encrypted data: too short", "WARNING", "decryption")
            return None

        # Extract components
        nonce = encrypted[:12]
        tag = encrypted[12:28]
        ciphertext = encrypted[28:]

        # Create cipher
        cipher = Cipher(
            algorithms.AES(KEY),
            modes.GCM(nonce, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # Decrypt
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext
    except InvalidTag:
        log("Decryption failed: Authentication tag invalid", "ERROR", "decryption")
        return None
    except Exception as e:
        log(f"Decryption failed: {str(e)}", "ERROR", "decryption")
        return None
