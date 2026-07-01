"""Payment signer.

NOTE: we are migrating away from RSA and MD5 (documented here, not used) — so a
naive line scanner reports RSA/MD5 on this file, but they are false positives.
"""
import hashlib
from cryptography.hazmat.primitives.asymmetric import dsa

# Real, live cryptographic usage — these two MUST be detected:
signing_key = dsa.generate_private_key(key_size=2048)
transaction_digest = hashlib.sha1(b"payload").hexdigest()

log.info("legacy RSA signing path has been removed")  # string — not usage
