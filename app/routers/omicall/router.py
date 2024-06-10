from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import logging
import httpx
from dependencies import (is_valid_signature,
                          date_to_timestamp,
                          )
from core.config import (SECRET_KEY_WEBHOOK,
                         ACCESS_TOKEN_OMICALL,)
from .schema import (WebhookModelCall,
                     ModelCustomers, ModelCallHistory,
                     )
from .tasks import (send_cdp_api_profile_retry,
                    send_cdp_api_event)

signature = SECRET_KEY_WEBHOOK
access_token = ACCESS_TOKEN_OMICALL

# Config logging
logging.basicConfig(filename='customer_retrieval_zalo.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter(tags=["OmiCall"])


# [WEBHOOK] - Get data call 
@router.post("/omicall/call/webhook/{secret}")
async def receive_webhook_call(data: WebhookModelCall, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# [API-POST] Receive a list of customers 
@router.post('/omicall/customers/')
async def get_customer_list(
    page: int = 1,
    size: int = 50
    
):
    
    api_url = "https://public-v1-stg.omicall.com/api/v2/contact/search"
    headers = {
        "Authorization": access_token
    }
    total_successful_customer = 0
    while True:
        params = {
            "page": page,
            "size": size
        }
        payloads = {
            "keyword": ""  
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=api_url, headers=headers, params=params, json=payloads)
                response.raise_for_status()
                results = response.json()
                customers = ModelCustomers(**results)
                items = customers.payload.items
                            
                if not items:
                    logging.info("No more users to process import data of from OmiCall")
                    break
                for item in items:
                    await send_cdp_api_profile_retry(item)
                    total_successful_customer += 1
                # return {"message": "Takes have been queud."}
                page += 1
                print(page)
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to OmiCall: {e}")
    
   
    return {f"Total_successful_customers": total_successful_customer, f"Page": page}



# [API-GET] Receive a list of call history
@router.get('/omicall/callhistory/')
async def get_call_history_list():
    api_url = "https://public-v1-stg.omicall.com/api/call_transaction/list"
    headers = {
        "Authorization": access_token
    }
    params = {
        "page": 1,
        "size": 1,
        "from_date": date_to_timestamp("20/04/2024"),
        "to_date": date_to_timestamp("30/04/2024"),
    }
    payloads = {
        "some_key": "some_value"  
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=api_url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            calls = ModelCallHistory(**results)
            items = calls.payload.items
            if items:
                for item in items:
                    await send_cdp_api_event(item)
            return {"message": "Takes have been queud."}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OmiCall: {e}")



# [API-GET] Receive a list of tickets
@router.get('/omicall/tickets/')
async def get_call_history_list():
    api_url = "https://public-v1-stg.omicall.com/api/call_transaction/list"
    headers = {
        "Authorization": access_token
    }
    params = {
        "page": 1,
        "size": 1,
        "from_date": date_to_timestamp("20/04/2024"),
        "to_date": date_to_timestamp("30/04/2024"),
    }
    payloads = {
        "some_key": "some_value"  
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=api_url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
            calls = ModelCallHistory(**results)
            items = calls.payload.items
            if items:
                for item in items:
                    await send_cdp_api_event(item)
            return {"message": "Takes have been queud."}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OmiCall: {e}")



