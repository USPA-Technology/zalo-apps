from typing import List, Optional, Dict, Any
import json
import httpx
import requests
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
import time
from .schema import RespCustomerList

from models import Profile, Event
from .schema import DatumCustomers, DatumOrders, DatumInvoices

from core.config import (TOKEN_KEY_CDP_KiotViet, TOKEN_VALUE_CDP_KiotViet,
                         CDP_URL_PROFILE_SAVE, CDP_URL_EVENT_SAVE)

from core.config import (TOKEN_KEY_CDP_EVERON_KIOTVIET, TOKEN_VALUE_CDP_EVERON_KIOTVIET,
                         CDP_URL_PROFILE_EVERON_SAVE, CDP_URL_EVENT_EVERON_SAVE,
                         CDP_OBSERVER_EVERON_KIOTVIET)

from dependencies import set_gender


logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_EVERON_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_EVERON_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_EVERON_KIOTVIET,
    "tokenvalue": TOKEN_VALUE_CDP_EVERON_KIOTVIET
}

journeyMapIds =  CDP_OBSERVER_EVERON_KIOTVIET
dataLables = "KiotViet"

    
# Process data for profiles
def convert_customer_data_mapping(item: DatumCustomers ) -> Profile:
    gender_str = set_gender(item.gender)             
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLables,
        # primaryEmail = 'lam@gmail.com',
        crmRefId= f"KiotViet-{item.code}",
        secondaryEmails= item.email,
        primaryPhone = item.contactNumber,
        firstName = item.name,
        gender = gender_str,
        dateOfBirth = item.birthDate,
        livingLocation = item.address,
        totalTransactionValue= item.totalInvoiced,
        )

# Process data for events
def convert_event_data_mapping(item: DatumOrders) -> Event:
    evendata_dict = {
            "id": item.id,
            "purchaseDate": item.purchaseDate,
            "customerCode": item.customerCode,
            "total": item.total,
            "status": item.status,   
    }
    eventdata_json = json.dumps(evendata_dict)
    return Event (
        targetUpdateEmail= "nguyenngocbaolamcva2020@gmail.com",
        tpname = 'Order',
        eventdata=eventdata_json,
        metric = "purchase",
    )


""" 
Functions that receive data model
and send them to the CDP API after the conversion has been processed
"""
# Send profile data to CDP
async def send_cdp_api_profile(data: DatumCustomers):
    logger.info("Processing send data")
    data_profile_coverted = convert_customer_data_mapping(data).model_dump()
    print(data_profile_coverted)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url= cdp_api_url_profile_save,
                                         headers=cdp_headers,
                                         json=data_profile_coverted)
            response_result = response.json()
            print(response_result)
            return response_result
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")

# Send profile data to CDP with retry logic
async def send_cdp_api_profile_retry(data: DatumCustomers, retries=3, delay=2):
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



# [Plan 2] Send data with requests module
def send_cdp_api_profile_request(data: DatumCustomers):
    logger.info("Processing send data")
    result = convert_customer_data_mapping(data).model_dump()
    logger.info(f"Sending data: {result}")
    print(result)
    try:
        response = requests.post(url=cdp_api_url_profile_save, headers=cdp_headers, json=result)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        client_detail = response.json()
        logger.info(f"Received response: {client_detail}")
        return client_detail
    except requests.RequestException as e:
        logger.error(f"Error connection with CDP: {e}")
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")
   
   
    
# Send event data to CDP
async def send_cdp_api_event(data: DatumOrders):
    logger.info("Processing send data")
    data_converted = convert_event_data_mapping(data).model_dump()
    print(data_converted)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=cdp_api_url_event_save, headers=cdp_headers, json=data_converted)
            result = response.json()
            print(result)
            return result
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")


# Send profile data to CDP
def send_cdp_api_profile_request_test(data: DatumCustomers):
    logger.info("Processing send data")
    result = convert_customer_data_mapping(data).model_dump()
    logger.info(f"Sending data: {result}")
    try:
        response = requests.post(url=cdp_api_url_profile_save, headers=cdp_headers, json=result)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        client_detail = response.json()
        logger.info(f"Received response: {client_detail}")
        return client_detail
    except requests.RequestException as e:
        logger.error(f"Error connection with CDP: {e}")
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")


# Retry function for sending profile data
def send_with_retries(data, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return send_cdp_api_profile_request(data)
        except HTTPException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise
            
            