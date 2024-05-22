from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request
import hmac
import hashlib
import time, datetime


def is_valid_signature(secret: str, signature: str) -> bool:
    computed_signature = hmac.new(
        secret.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)



# Function covert string(dd/mm/YYYY) to timestamp miliseconds
def date_to_timestamp(date_str):
    dt = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    timestamp = int(dt.timestamp() * 1000)  # covert to milliseconds
    return timestamp

# from_date = date_to_timestamp("20/04/2024")
# to_date = date_to_timestamp("30/04/2024")
# print(from_date)
# print(to_date)