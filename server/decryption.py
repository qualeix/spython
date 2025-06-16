import base64
import config
from utils import log
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Generate key from config string
KEY = base64.b64decode(config.ENCRYPTION_KEY)
if len(KEY) not in [16, 24, 32]:
    log(f"Decryption key must be 16, 24 or 32 bytes long, got {len(KEY)}", "WARNING", "decryption")


def decrypt_data(encrypted):
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

        # Decrypt data
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext
    except InvalidTag:
        log("Decryption failed: Authentication tag invalid", "ERROR", "decryption")
        return None
    except Exception as e:
        log(f"Decryption failed: {e}", "ERROR", "decryption")
        return None
