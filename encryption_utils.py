import ascon
import os
import base64
import hashlib

def generate_key():
    """Generate a 128-bit ASCON key (16 bytes)."""
    return os.urandom(16)

def generate_shared_key(password="SecureTalkDemo2024"):
    """Generate a shared 128-bit key from a password for all clients."""
    return hashlib.sha256(password.encode()).digest()[:16]

def encrypt_message(key, plaintext):
    """
    Encrypt a message using ASCON-AEAD128.
    Returns Base64 encoded bytes containing: nonce + ciphertext (with embedded tag).
    """
    nonce = os.urandom(16)
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    ciphertext = ascon.encrypt(key, nonce, b"", plaintext, variant="Ascon-128")
    
    msg_bytes = nonce + ciphertext
    return base64.b64encode(msg_bytes)

def decrypt_message(key, b64_encoded_msg):
    """
    Decrypt a Base64 encoded ASCON-AEAD128 message.
    Expected format: nonce (16 bytes) + ciphertext (with embedded tag).
    """
    try:
        msg_bytes = base64.b64decode(b64_encoded_msg)
        
        if len(msg_bytes) < 32:
            raise ValueError("Message too short - corrupted data")
        
        nonce = msg_bytes[:16]
        ciphertext = msg_bytes[16:]
        
        plaintext = ascon.decrypt(key, nonce, b"", ciphertext, variant="Ascon-128")
        
        if plaintext is None:
            raise ValueError("Decryption failed: Authentication failed")
        
        return plaintext.decode()
        
    except ValueError as e:
        raise ValueError(f"Decryption failed: {e}")
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
