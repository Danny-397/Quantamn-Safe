import hashlib


def add(a, b):
    return a + b


digest = hashlib.sha3_256(b"data").hexdigest()
note = "migrated to AES-256 and Kyber"
