import httpx
import time
import os
import json
import logging
import asyncio
from typing import List, Dict
from httpx import HTTPStatusError
# from core.config import ACCESS_TOKEN_KIOTVIET
# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "fetch_log.json")

api_url = "https://public.kiotapi.com/invoices"
access_token = 'ACCESS_TOKEN_KIOTVIET'
headers = {
        "Retailer": 'everon',
        "Authorization": access_token
    }

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

async def send_with_retries(data, retries=3, delay=2):
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.get(url= api_url, headers=headers)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, HTTPStatusError) as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    sleep_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error("All retry attempts failed.")
                    raise

async def fetch_all_profiles(page_size: int, start_page: int = 1):
    page = start_page
    while True:
        try:
            logger.info(f"Fetching page {page} with size {page_size}")
            profiles = await send_with_retries({"page": page, "size": page_size})
            if not profiles:
                logger.info("No more profiles to fetch.")
                break
            process_profiles(profiles)
            log_last_page(page)
            page += 1
        except Exception as e:
            logger.error(f"Fetching failed at page {page}: {e}")
            break

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

def process_profiles(profiles: List[Dict]):
    for profile in profiles:
        # Xử lý từng profile ở đây
        logger.info(f"Processed profile: {profile}")

async def main():
    last_page = get_last_logged_page()
    page_size = 100  # Kích thước trang mặc định ban đầu

    # Điều chỉnh kích thước trang tùy thuộc vào yêu cầu của bạn
    try:
        await fetch_all_profiles(page_size, start_page=last_page)
    except Exception as e:
        logger.error(f"Error fetching profiles: {e}")

if __name__ == "__main__":
    asyncio.run(main())
