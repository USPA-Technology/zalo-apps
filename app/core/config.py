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
ACCESS_TOKEN_ZALO = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN_ZALO = os.getenv("REFRESH_TOKEN")
APP_ID_ZALO = os.getenv("APP_ID")
SECRET_KEY_ZALO = os.getenv("SECRET_KEY")

# [KiotViet - ENV]
ACCESS_TOKEN_KIOTVIET = os.getenv("ACCESS_TOKEN_KIOTVIET")
RETAILER = os.getenv("RETAILER")

# Secret for Webhook
SECRET_KEY_WEBHOOK = os.getenv("SECRET_KEY_WEBHOOK")


def refresh_access_token():
    url = "https://oauth.zaloapp.com/v4/oa/access_token"
    refresh_token = REFRESH_TOKEN_ZALO
    app_id = APP_ID_ZALO
    secret_key = SECRET_KEY_ZALO

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
        



# # Lên lịch chạy hàm scheduled_refresh_access_token vào 16:59:00 hàng ngày
# schedule.every().day.at("17:54:00").do(scheduled_refresh_access_token)

# def start_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# async def startup_event():
#     task = BackgroundTasks()
#     task.add_task(start_schedule)
#     print("Startup event activated!")
#     return {"message": "Refresh token success"}

# zaloapp.add_event_handler("startup", startup_event)
