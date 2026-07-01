"""Account service — key rotation with audit logging.

None of the algorithm names below are cryptographic *usage*; they live in log
messages, an exception string, and a comment. A precise scanner must not flag
them.
"""
import logging

log = logging.getLogger(__name__)


def rotate(account_id):
    # Emit an audit trail — this is messaging, not crypto usage.
    log.info("Rotating RSA and ECDSA keys for account %s", account_id)
    log.warning("Legacy MD5 fingerprints will be dropped next release")
    if not account_id:
        raise ValueError("DSA signing key missing; SHA-1 fallback disabled")
    return "migrated to Kyber and AES-256"
