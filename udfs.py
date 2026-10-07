"""Pixeltable UDFs for the webhook vault (recorded by module path, e.g. `udfs.sign_payload`).

sign_payload reads WEBHOOK_HMAC_SECRET from the environment when it runs; the secret is never stored.
"""
import hashlib
import hmac
import os
from urllib.parse import urlparse

import pixeltable as pxt


@pxt.udf
def digest_payload(payload: str) -> str:
    """SHA-256 of the payload (no secret needed)."""
    return hashlib.sha256(payload.encode()).hexdigest()


@pxt.udf
def sign_payload(event: str, payload: str) -> str:
    """HMAC-SHA256 over 'event.payload', keyed by WEBHOOK_HMAC_SECRET (as a 'sha256=...' header value)."""
    secret = os.environ.get('WEBHOOK_HMAC_SECRET')
    if not secret:
        raise RuntimeError('WEBHOOK_HMAC_SECRET is not set')
    mac = hmac.new(secret.encode(), f'{event}.{payload}'.encode(), hashlib.sha256)
    return 'sha256=' + mac.hexdigest()


@pxt.udf
def target_host(url: str) -> str:
    return urlparse(url).hostname or ''
