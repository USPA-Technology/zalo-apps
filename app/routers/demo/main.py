from pydantic import BaseModel
from typing import List, Optional
import json
import httpx
from fastapi import HTTPException, APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

from core.config import (ACCESS_TOKEN_KIOTVIET, RETAILER, TOKEN_KEY_CDP_KiotViet, TOKEN_VALUE_CDP_KiotViet)


retailer = 'everon'
cdp_api_url = "https://dcdp.bigdatavietnam.org/api/profile/save"
cdp_headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": TOKEN_KEY_CDP_KiotViet,
    "tokenvalue": TOKEN_VALUE_CDP_KiotViet
}

class Model(BaseModel):
    id: int
    code: str
    name: str
    gender: bool
    contactNumber: str
    address: str
    retailerId: int
    branchId: int
    locationName: str
    wardName: str
    modifiedDate: str
    createdDate: str
    type: int
    organization: str
    groups: str
    debt: int
    totalInvoiced: int
    totalRevenue: int
    totalPoint: int
    product: Optional[str] = None


class Profile(BaseModel):
    journeyMapIds: str
    dataLabels: str
    primaryPhone: Optional[str] = None
    firstName: str

def map_to_profile(data: Model) -> Profile:
    # Example mapping logic, customize according to your data structure
    return Profile(
        journeyMapIds="7TZMFpPZJNVWNYhiyJVgeZ",
        dataLabels='TestKiotViet',
        primaryPhone=data.contactNumber,
        firstName=data.name
    )

async def send_cdp_api(data: Model):
    logger.info("Process mapping data")
    result = map_to_profile(data).model_dump()
    print(result)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(cdp_api_url, headers=cdp_headers, json=result)
            client_detail = response.json()
            return client_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")

@router.get('/getCustomerInfo_DEMO/{client_code}')
async def get_customer_info(client_code: str):
    """
    Retrieve information about a customer in KiotViet.

    Args:
        client_code (str): The client code of the customer.

    Returns:
        json: Information about the customer.
    """
    api_url = f"https://public.kiotapi.com/customers/code/{client_code}"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            client_data = response.json()
            # Map the response to ModelCustomer
            customer = Model(**client_data)  # Adjust this based on actual KiotViet response structure
            print(customer)
            return await send_cdp_api(customer)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from KiotViet: {e.response.json()}")




class Datum(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[bool] = None
    birthDate: Optional[str] = None
    contactNumber: Optional[str] = None
    address: Optional[str] = None
    locationName: Optional[str] = None
    wardName: Optional[str] = None
    email: Optional[str] = None
    organization: Optional[str] = None
    comments: Optional[str] = None
    taxCode: Optional[str] = None
    debt: Optional[float] = None
    totalInvoiced: Optional[float] = None
    totalPoint: Optional[float] = None
    totalRevenue: Optional[float] = None
    retailerId: Optional[int] = None
    modifiedDate: Optional[str] = None
    createdDate: Optional[str] = None
    rewardPoint: Optional[int] = None
    psidFacebook: Optional[int] = None

class ModelCustomers(BaseModel):
    total: Optional[int] = None
    pageSize: Optional[int] = None
    data: List[Datum]



def map_to_profile_list(datum: Datum) -> Profile:
    return Profile(
        journeyMapIds="7TZMFpPZJNVWNYhiyJVgeZ",
        dataLabels='TestKiotViet',
        primaryPhone=datum.contactNumber,
        firstName=datum.name
    )

async def send_cdp_api_list(profile: Profile):
    logger.info("Sending data to CDP API")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=cdp_api_url, headers=cdp_headers, json= profile)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to CDP: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from CDP: {e.response.json()}")

@router.get('/getCustomerList_DEMO/')
async def get_customer_list():
    api_url = "https://public.kiotapi.com/customers"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            client_data = response.json()
            

            # Adjust the mapping to fit the actual response structure
            customers = ModelCustomers(**client_data)
            profiles = [map_to_profile(datum).model_dump() for datum in customers.data]
            print(profiles)
            # Send profiles in batches
            batch_size = 1
            results = []
            for i in range(0, len(profiles), batch_size):
                batch = profiles[i:i + batch_size]
                result = await send_cdp_api_list(batch)
                results.append(result)
                print(results)
            return results
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to KiotViet: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from KiotViet: {e.response.json()}") 