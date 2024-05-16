from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request
import hmac
import hashlib


def is_valid_signature(secret: str, signature: str) -> bool:
    computed_signature = hmac.new(
        secret.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)
