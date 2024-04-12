import os
import time
import requests
from dotenv import load_dotenv
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
    refresh_token = REFRESH_TOKEN
    app_id = APP_ID
    secret_key = SECRET_KEY

    payload = {
        "refresh_token": refresh_token,
        "app_id": app_id,
        "grant_type": "refresh_token"
    }
    headers = {
        'secret_key': secret_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for any HTTP error status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing access token: {e}")


def scheduled_refresh_access_token():
    # Call refresh_access_token function
    try:
        call_refresh_access_token = refresh_access_token
        json_data = json.loads(call_refresh_access_token)
        access_token_new = json_data['access_token']
        refresh_token_new = json_data['refresh-token']
        
        print(access_token_new)
        print(refresh_token_new)
        
        with open('.env', 'r') as env_file:
            
            lines = env_file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("ACCESS_TOKEN="):
                    lines[i] = f"ACCESS_TOKEN={access_token_new}\n"
                elif line.startswith("REFRESH_TOKEN="):
                    lines[i] = f"REFRESH_TOKEN={refresh_token_new}\n"
                    
        with open('.env', 'w') as env_file:
            env_file.writelines(lines)
        print("Tokens updated successfully.")
    except Exception as e:
        print(f"Error updating tokens: {e}")
        

y = refresh_access_token()
print(y)

