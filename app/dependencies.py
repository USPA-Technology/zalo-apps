from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request
import hmac
import hashlib
import time, datetime
import json
import os
import logging

def is_valid_signature(secret: str, signature: str) -> bool:
    computed_signature = hmac.new(
        secret.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

# Function set gender 
def set_gender(gender: str | bool | None):
    if isinstance(gender, bool):
        if gender:
            gender_str = "male"
        else:
            gender_str = "female"
    elif isinstance(gender, str):
        gender_str = gender
        
    elif gender is None:
        gender_str = "None"
    else:
        raise ValueError("gender must be a string or boolean")
    
    # print(f"Gender set to: {gender_str}")
    return gender_str
# # Example usage:
# set_gender("female")  # Output: Gender set to: female
# set_gender(True)      # Output: Gender set to: male
# set_gender(False)     # Output: Gender set to: female


# Function to convert string (dd/MM/yyyy) to timestamp in milliseconds
def date_to_timestamp(date_str):
    dt = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    timestamp = int(dt.timestamp() * 1000)  # convert to milliseconds
    return timestamp

# Function to convert timestamp in milliseconds to string (dd/MM/yyyy)
def timestamp_to_date(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)  # convert from milliseconds
    date_str = dt.strftime('%d/%m/%Y')
    return date_str

# Example usage
# from_date = date_to_timestamp("01/05/2023")
# to_date = date_to_timestamp("01/06/2023")
# print(from_date)
# print(to_date)

# date_str_from_timestamp = timestamp_to_date(1638774810356)  # Example timestamp in milliseconds
# print(date_str_from_timestamp)




logger = logging.getLogger(__name__)

LOG_FILE = "fetch_log.json"

def log_last_page(page: int):
    log_data = {"last_page": page}
    with open(LOG_FILE, "w") as log_file:
        json.dump(log_data, log_file)
    logger.info(f"Logged last fetched page: {page}")

def get_last_logged_page() -> int:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            log_data = json.load(log_file)
            return log_data.get("last_page", 1)
    return 1
