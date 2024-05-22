from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import httpx
from dependencies import (is_valid_signature,
                          date_to_timestamp
                          )
from core.config import (SECRET_KEY_WEBHOOK,
                         ACCESS_TOKEN_OMICALL,
                         TOKEN_KEY_CDP_OMICALL,TOKEN_VALUE_CDP_OMICALL,
                         CDP_URL_PROFILE_SAVE, CDP_URL_EVENT_SAVE
                         )
from .schema import (WebhookModelCall,
                     ModelCustomers, ModelCallHistory,
                     )
from .tasks import (
                    send_cdp_api)

signature = SECRET_KEY_WEBHOOK
access_token = ACCESS_TOKEN_OMICALL

router = APIRouter(tags=["OmiCall"])


# [WEBHOOK] - Get data call 
@router.post("/omicall/customer/webhook/{secret}")
async def receive_webhook(data: WebhookModelCall, secret: str):
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
async def get_customer_list():
    api_url = "https://public-v1-stg.omicall.com/api/v2/contact/search"
    headers = {
        "Authorization": access_token
    }
    params = {
        "page": 1,
        "size": 3
    }
    payloads = {
        "some_key": "some_value"  
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=api_url, headers=headers, params=params, json=payloads)
            response.raise_for_status()
            results = response.json()
            customers = ModelCustomers(**results)
            items = customers.payload.items
            if items:
                for item in items:
                    await send_cdp_api(item)
            return {"message": "Takes have been queud."}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OmiCall: {e}")



# [API-GET] Receive a list of call history
@router.get('/omicall/callhistory/')
async def get_call_history_list():
    api_url = "https://public-v1-stg.omicall.com/api/call_transaction/list"
    headers = {
        "Authorization": access_token
    }
    params = {
        "page": 1,
        "size": 100,
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
            # if items:
            #     for item in items:
            #         # await send_cdp_api(item)
            #         print(items)
            return items
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to OmiCall: {e}")


