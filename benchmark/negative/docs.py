"""Crypto migration guide (documentation only — no live crypto in this module).

Historically this service used MD5 and SHA-1 for checksums and RC4 / 3DES for
transport. All of that has been removed in favor of SHA-256 and AES-256-GCM,
with RSA and DSA replaced by Kyber and Dilithium.
"""


def summary():
    """Human-readable note about the old RSA and DSA usage (now gone)."""
    return "see the post-quantum migration guide"
