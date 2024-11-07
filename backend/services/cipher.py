# backend/services/cipher.py

import hashlib

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()
