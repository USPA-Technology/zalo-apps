from typing import List, Optional, Dict, Any
import json
import httpx
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
import time

from models import Profile, Event
from .schema import ItemCustomer, ItemCallHistory

from core.config import (TOKEN_KEY_CDP_EVERON_OMICALL, TOKEN_VALUE_CDP_EVERON_OMICALL,
                         CDP_URL_PROFILE_EVERON_SAVE, CDP_URL_EVENT_EVERON_SAVE,
                         CDP_OBSERVER_EVERON_OMICALL)

logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_EVERON_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_EVERON_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_EVERON_OMICALL,
    "tokenvalue": TOKEN_VALUE_CDP_EVERON_OMICALL
}

journeyMapIds =  CDP_OBSERVER_EVERON_OMICALL

# Process data for profiles
def convert_customer_data_mapping(item: ItemCustomer ) -> Profile:
    dataLabels = f"Omicall ; {item.contact_categories_view[0].name}"
    data_dict = {}
    attribute_structures = item.attribute_structure
    for attribute in attribute_structures:
        field_code = attribute.field_code
        values = attribute.value
        if values:
            display_value = values[0].display_value
            data_dict[field_code] = display_value
                                
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLabels,
        crmRefId= f"OmiCall-{item.id}",
        primaryEmail = data_dict.get("mail"),
        primaryPhone = data_dict.get("phone_number"),
        firstName = data_dict.get("full_name"),
        gender = data_dict.get("gender"),
        dateOfBirth = data_dict.get("birth_date"),
        livingLocation = data_dict.get("address"),
        jobTitles = data_dict.get("job_title"),
        applicationIDs= {"Refcode": data_dict.get("ref_code")}
        )

# Process data for events
def convert_event_data_mapping(item: ItemCallHistory) -> Event:
    return Event (
        eventTime= item.created_date,
        # TargetUpdate Customer_code with KiotViet
        targetUpdateEmail= "nguyenngocbaolamcva2020@gmail.com",
        # Tpname
        tpname = item.direction,
        eventdata = {
            'transaction_id': item.transaction_id,
            'tenant_id': item.tenant_id,
            'source_number': item.source_number,
            'destination_number': item.destination_number,
            'disposition': item.disposition,
            'hotline': item.hotline,
            'tag': item.tag,
            'note': item.note,
            'last_updated_data': item.created_date,
            'customer': item.customer,
        },
        metric = "qr-code-scan",
    )
    
# Send profile data to CDP with retry logic
async def send_cdp_api_profile_retry(data: ItemCustomer, retries=3, delay=2):
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