from typing import List, Optional, Dict, Any
import json
import httpx
import requests
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
import time

from models import Profile, Event
from .schema import UserID, DataUserDetail

from core.config import (TOKEN_KEY_CDP_EVERON_ZALO, TOKEN_VALUE_CDP_EVERON_ZALO,
                         CDP_URL_PROFILE_EVERON_SAVE, CDP_URL_EVENT_EVERON_SAVE,
                         CDP_OBSERVER_EVERON_ZALO)



logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_EVERON_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_EVERON_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_EVERON_ZALO,
    "tokenvalue": TOKEN_VALUE_CDP_EVERON_ZALO
}

journeyMapIds =  CDP_OBSERVER_EVERON_ZALO
dataLables_follower = "Zalo OA follower"

    
# Process data for profiles
def convert_customer_data_mapping(user_id: UserID ) -> Profile:
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLables_follower,
        crmRefId= f"zalo-{user_id.user_id}",
        firstName="Zalo Visitor"
        )
    

# Send profile data to CDP with retry logic
async def send_cdp_api_profile_retry(data: DataUserDetail, retries=3, delay=2):
    logger.info("Processing send data")
    data_profile_converted = convert_user_detail_data_mapping(data).model_dump()
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


    
# Process data for mapping user detail from Zalo to CDP
def convert_user_detail_data_mapping(user: DataUserDetail) -> Profile:
    
    if user.shared_info is not None:
        phone_str = str(user.shared_info.phone)
        address = user.shared_info.address
        city = user.shared_info.city
        district = user.shared_info.district
    else:
        phone_str = None
        address = None
        city = None
        district = None
   
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLables_follower,
        firstName= user.display_name,
        # is_sensitive: false,
        # user_last_interaction_date: "06/07/2023",
        # user_is_follower: false,
        # tags_and_notes_info: {
        # "note": [],
        # "tag_names": []
        # },
        primaryAvatar= user.avatar,
        livingLocation= address,
        livingCity= city,
        livingDistrict= district,
        primaryPhone= phone_str,
        crmRefId= f"zalo-{user.user_id}",
        # socialMediaProfiles= {"zalo": user.user_id}
        )

     
     
