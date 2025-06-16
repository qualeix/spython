import os
import config
import base64
from utils import log
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# Generate key from config string
KEY = base64.b64decode(config.ENCRYPTION_KEY)
if len(KEY) not in [16, 24, 32]:
    log(f"Encryption key must be 16, 24 or 32 bytes long, got {len(KEY)}", "WARNING", "encryption")


def encrypt_data(data):
    """Encrypt data using AES-GCM"""
    try:
        # Generate random nonce
        nonce = os.urandom(12)

        # Create Cipher
        cipher = Cipher(
            algorithms.AES(KEY),
            modes.GCM(nonce),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Encrypt and finalize
        if isinstance(data, str):
            data = data.encode('utf-8')
        ciphertext = encryptor.update(data) + encryptor.finalize()
        log(f"Encrypted {len(data)} bytes", "DEBUG", "encryption")

        # Return nonce + tag + ciphertext
        return nonce + encryptor.tag + ciphertext
    except Exception as e:
        log(f"Encryption failed: {str(e)}", "ERROR", "encryption")
        return None
