from typing import List, Optional, Dict, Any
import json
import httpx
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging

from models import Profile, Event
from .schema import ItemCustomer, ItemCallHistory

from core.config import (TOKEN_KEY_CDP_OMICALL, TOKEN_VALUE_CDP_OMICALL,
                         CDP_URL_PROFILE_SAVE, CDP_URL_EVENT_SAVE)

logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_OMICALL,
    "tokenvalue": TOKEN_VALUE_CDP_OMICALL
}

# Process data for profiles
def convert_customer_data_mapping(item: ItemCustomer ) -> Profile:
    data_dict = {}
    attribute_structures = item.attribute_structure
    for attribute in attribute_structures:
        field_code = attribute.field_code
        values = attribute.value
        if values:
            display_value = values[0].display_value
            data_dict[field_code] = display_value
                                
    return Profile (
        journeyMapIds = "4vBUFB4rbehETPIlAXJ4Bd",
        dataLabels = "OmiCall",
        primaryEmail = data_dict.get("mail"),
        primaryPhone = data_dict.get("phone_number"),
        firstName = data_dict.get("full_name"),
        gender = data_dict.get("gender"),
        dateOfBirth = data_dict.get("birth_date"),
        livingLocation = data_dict.get("address"),
        jobTitles = data_dict.get("job_title"),
            )

# Process data for events
def convert_event_data_mapping(item: ItemCallHistory) -> Event:
    return Event (
        targetUpdateEmail= "nguyenngocbaolamcva2020@gmail.com",
        tpname = item.direction,
        eventdata = {
            "transaction_id": item.transaction_id,
            "tenant_id": item.tenant_id,
            "source_number": item.source_number,
            "destination_number": item.destination_number,
            "hotline": item.hotline,
            "note": item.note,
            "created_date": item.created_date,
            "customer": item.customer,
        },
        metric = "qr-code-scan",
    )
    
# Send profile data to CDP
async def send_cdp_api_profile(data: ItemCustomer):
    logger.info("Processing send data")
    result = convert_customer_data_mapping(data).model_dump()
    print(result)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url= cdp_api_url_profile_save, headers=cdp_headers, json=result)
            client_detail = response.json()
            print(client_detail)
            return client_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")

    
# Send event data to CDP
async def send_cdp_api_event(data: ItemCallHistory):
    logger.info("Processing send data")
    result = convert_event_data_mapping(data).model_dump()
    print(result)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=cdp_api_url_event_save, headers=cdp_headers, json=json.dumps(result))
            event_detail = response.json()
            print(event_detail)
            return event_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")

