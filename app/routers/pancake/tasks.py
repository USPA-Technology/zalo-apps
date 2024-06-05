from typing import List, Optional, Dict, Any
import json
import httpx
import requests
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
import time

from models import Profile, Event
from .schema import DatumCustomer

from core.config import (TOKEN_KEY_CDP_EVERON_PANCAKE_POS, TOKEN_VALUE_CDP_EVERON_PANCAKE_POS,
                         CDP_URL_PROFILE_EVERON_SAVE, CDP_URL_EVENT_EVERON_SAVE,
                         CDP_OBSERVER_EVERON_PANCAKE_POS)

from dependencies import set_gender


logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_EVERON_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_EVERON_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_EVERON_PANCAKE_POS,
    "tokenvalue": TOKEN_VALUE_CDP_EVERON_PANCAKE_POS
}

journeyMapIds =  CDP_OBSERVER_EVERON_PANCAKE_POS
dataLables = "PanCake-Pos"

    
# Process data for profiles
def convert_customer_data_mapping(item: DatumCustomer ) -> Profile:
    gender_str = set_gender(item.gender)
    # Check if shop_customer_addresses is not None before accessing its elements
    if len(item.shop_customer_addresses) == 0:
        living_location = None
    else:
        living_location = item.shop_customer_addresses[0].full_address
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLables,
        crmRefId= f"PanCake-{item.id}",
        primaryPhone = item.phone_numbers[0],
        firstName = item.name,
        gender = gender_str,
        dateOfBirth = item.date_of_birth,
        livingLocation = living_location,
        totalTransactionValue= item.purchased_amount,
    )


# Send profile data to CDP with retry logic
async def send_cdp_api_profile_retry(data: DatumCustomer, retries=3, delay=2):
    logger.info("Processing send data")
    data_profile_converted = convert_customer_data_mapping(data).model_dump()
    print(data_profile_converted)

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=cdp_api_url_profile_save,
                                             headers=cdp_headers,
                                             json=data_profile_converted)
                response.raise_for_status()  # Raise an HTTPError if the response was unsuccessful
                response_result = response.json()
                print(response_result)
                return response_result
        except httpx.RequestError as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error("Max retries exceeded. Could not connect to CDP.")
                raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")

    return None