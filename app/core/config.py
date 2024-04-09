import os
import time
import requests
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(override=True)

# Database Arango
ARANGODB_USERNAME = os.getenv("ARANGODB_USERNAME")
ARANGODB_PASSWORD = os.getenv("ARANGODB_PASSWORD")


# Access Token of Zalo OA
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
APP_ID = os.getenv("APP_ID")
SECRET_KEY = os.getenv("SECRET_KEY")




def refresh_access_token():
    url = "https://oauth.zaloapp.com/v4/oa/access_token"
    refresh_token = ACCESS_TOKEN
    app_id = APP_ID
    secret_key = SECRET_KEY

    payload = {
        "refresh_token": refresh_token,
        "app_id": app_id,
        "grant_type": "refresh_token"
    }
    headers = {
        'secret_key': secret_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for any HTTP error status codes
        data = response.json()
        print("Access token refreshed successfully.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing access token: {e}")

# Gọi hàm để cập nhật lại các biến trong tệp .env
