from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request
import hmac
import hashlib
import time, datetime
import json
import os
import logging

LOG_FILE = "processed_items.log"

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
    
    print(f"Gender set to: {gender_str}")
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


LOG_FILE = "processed_items.log"

class ProcessedItemLogger:
    def __init__(self, log_file=LOG_FILE):
        self.log_file = log_file

    def get_last_processed_item(self):
        if not os.path.exists(self.log_file):
            return 0
        with open(self.log_file, "r") as file:
            last_line = file.readlines()[-1].strip()
            return int(last_line) if last_line else 0

    def log_processed_item(self, item_id):
        with open(self.log_file, "a") as file:
            file.write(f"{item_id}\n")