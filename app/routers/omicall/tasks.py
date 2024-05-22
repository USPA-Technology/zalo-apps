from typing import List, Optional, Dict, Any
import json
import httpx
from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging

from models import Profile, Event
from .schema import ModelCustomers, Item


from core.config import (TOKEN_KEY_CDP_KiotViet, TOKEN_VALUE_CDP_KiotViet,
                         CDP_URL_PROFILE_SAVE, CDP_URL_EVENT_SAVE)

logger = logging.getLogger(__name__)
router = APIRouter()

cdp_api_url_profile_save = CDP_URL_PROFILE_SAVE
cdp_api_url_event_save = CDP_URL_EVENT_SAVE

cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_KiotViet,
    "tokenvalue": TOKEN_VALUE_CDP_KiotViet
}


def convert_customer_data_mapping(item: Item) -> Profile:
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



async def send_cdp_api(data: Item):
    logger.info("Process mapping data")
    result = convert_customer_data_mapping(data).model_dump()
    print(result)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url= cdp_api_url_profile_save, headers=cdp_headers, json=result)
            client_detail = response.json()
            return client_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")

       


















def map_to_profile_list(data: ModelCustomers) -> Profile:
    info = {}
    try:
        instance_id = data.instance_id
        payload = data.payload
        items  = payload.items
        
        for item in items:
            contact_type = item.contact_type
            created_by_name = item.create_by
            last_update_by = item.last_update_by
            attribute_structures = item.attribute_structure
            
            for attribute in attribute_structures:
                field_code = attribute.field_code
                if attribute[value]:
                    info[field_code] = attribute[value][0][display_value]
                else:
                    info[field_code] = None
                values = attribute.value
                for value in values:
                    display_value = value.display_value
    except ValidationError as e:
        print(e.json)
        
        
        
        
# Hàm get_contact_info sẽ trích xuất thông tin từ một mục liên hệ
def get_contact_info(item):
    info = {}
    for attribute in item['attribute_structure']:
        field_code = attribute['field_code']
        if attribute['value']:
            info[field_code] = attribute['value'][0]['display_value']
        else:
            info[field_code] = None
    return info

    return Profile(
    journeyMapIds = "value journeymap ids",
    dataLabels = "OmiCall",
    primaryEmail = datum.source_contact_id

    )



async def send_cdp_profile(profile: Profile):
    logger.info("Sending data to CDP API")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=cdp_api_url_profile_save, headers=cdp_headers, json= profile)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to CDP: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from CDP: {e.response.json()}")


from typing import Dict, Any



# Hàm chuyển đổi model
def convert_model_to_dict(model: ModelCustomers) -> Dict[str, Any]:
    data_dict = {}
    payload = model.payload
    if payload:
        items = payload.items
        for item in items:
            attribute_structures = item.attribute_structure
            for attribute in attribute_structures:
                field_code = attribute.field_code
                values = attribute.value
                if values:
                    display_value = values[0].display_value
                    data_dict[field_code] = display_value
    return Profile (
        
    )





# # Sử dụng hàm convert_model_to_dict để chuyển đổi dữ liệu
# model_data = ModelCustomers(**your_data_dict)
# result_dict = convert_model_to_dict(model_data)

# # In ra kết quả
# print(result_dict)


