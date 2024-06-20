from typing import List, Optional, Dict, Any
import json
import httpx
import requests
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
import time
import csv
import re
from .schema import RespCustomerList

from models import Profile, Event
from .schema import DatumCustomers, DatumOrders, DatumInvoices, InvoiceDetails, DatumProduct

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

def convert_kiotviettime_to_CDP_time(datetime_str):
  return datetime_str.split('.')[0] + 'Z'


    
# Process data for profiles
def convert_customer_data_mapping(item: DatumCustomers ) -> Profile:
    gender_str = set_gender(item.gender)
    return Profile (
        journeyMapIds = journeyMapIds,
        dataLabels = dataLables,
        primaryEmail = item.email,
        crmRefId= f"KiotViet-{item.code}",
        # secondaryEmails= item.email,
        primaryPhone = item.contactNumber,
        firstName = item.name,
        gender = gender_str,
        dateOfBirth = item.birthDate,
        livingLocation = item.address,
        livingCity= item.locationName,
        livingWard = item.wardName,
        totalTransactionValue= item.totalInvoiced,
        )

# Process data for events
def convert_event_data_mapping(item: DatumInvoices) -> Event:
    touchpoin_name = f"{item.soldByName} - {item.branchName}"
    return Event (
        eventTime= convert_kiotviettime_to_CDP_time(item.purchaseDate),
        targetUpdateCrmId= f"KiotViet-{item.customerCode}",
        tpname = touchpoin_name,
        tpurl= "uri://KiotViet:soldbyId:" + str(item.soldById),
        rawJsonData = item.model_dump_json(),
        metric = "purchase",
        tsid= item.code,
        tscur= "VND",
        tsval= item.totalPayment,

    )

""" 
Functions that receive data model
and send them to the CDP API after the conversion has been processed
"""

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


# Send event data to CDP
async def send_cdp_api_event(data: DatumInvoices):
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
    
    
    
# Send event data to CDP with retry logic
async def send_cdp_api_event_retry(data: DatumInvoices, retries=3, delay=2):
    logger.info("Processing send data")
    data_profile_converted = convert_event_data_mapping(data).model_dump()
    print(data_profile_converted)

    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=cdp_api_url_event_save,
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



# Assuming convert_event_data_mapping is a function that converts data to the desired format
# and model_dump is a method that dumps data to a dictionary

async def import_cdp_csv_product(data: DatumProduct, csv_file_path='cdp_products.csv'):
    logger.info("Processing send data")
    # Define the CSV file columns
    csv_columns = [
        'Product_Type', 'Keywords', 'Store_ID', 'Product_ID_Type', 'Product_ID', 'Title',
        'Description', 'Image_URL', 'Original_Price', 'Sale_Price', 'Currency', 'Full_URL'
    ]
    
    # Map the data to the corresponding CSV columns
    csv_data = {
        'Product_Type': data.categoryName or "",
        'Keywords': data.name or "",
        'Store_ID': data.retailerId or "",
        'Product_ID_Type': "SKU",
        'Product_ID': data.code or "",
        'Title': data.fullName or "",
        'Description': re.sub(r'</?br.*?>', ' ', data.description or ""),
        'Image_URL': ", ".join(data.images) if data.images else "",
        'Original_Price': data.basePrice or 0.0,
        'Sale_Price': data.basePrice or 0.0,
        'Currency': "VND",
        'Full_URL': f"https://www.everonvn.vn/tim-kiem?key={data.id}"
    }
    # print(csv_data)
    try:
        # Open the CSV file in append mode
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            
            # Write the header if the file is empty
            file.seek(0, 2)  # Move the cursor to the end of the file
            if file.tell() == 0:
                writer.writeheader()
            
            # Write the data to the CSV file
            writer.writerow(csv_data)
            logger.info(f"Data written to CSV file: {csv_file_path}")
    
    except Exception as e:
        logger.error(f"Failed to write data to CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to write data to CSV: {e}")
