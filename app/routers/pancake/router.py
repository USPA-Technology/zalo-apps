from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import ValidationError
import httpx
import requests
import json
import logging
from typing import Annotated, List, Optional

from .schema import ( ModelCustomer,
                     )
from core.config import (SECRET_KEY_WEBHOOK,
                            API_KEY_EVERON_PANCAKE_POS, SHOP_ID_EVERON_PANCAKE_POS,
                            )
from .tasks import (
                    send_cdp_api_profile_retry,
                    )

signature = SECRET_KEY_WEBHOOK
shop_id = SHOP_ID_EVERON_PANCAKE_POS

router  = APIRouter(tags=['PanCake'])



# [API-GET] Get the customer list
@router.get('/pancake/customers')
async def get_customers(
    page_size: int = 50,
    page_number: int = 1,
):

    api_url = f"https://pos.pages.fm/api/v1/shops/{shop_id}/customers/"
    api_key = API_KEY_EVERON_PANCAKE_POS

    params = {
            'api_key': api_key,
            'page_size': page_size,
            'page_number': page_number,
        }
    try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=api_url, params=params)
                response.raise_for_status()
                response_result = response.json()
                print(response_result)
                customer_model = ModelCustomer(**response_result)
                customers = customer_model.data
                if customers:
                    for customer in customers:
                        await send_cdp_api_profile_retry(customer)
                return customers
    except httpx.RequestError as e:
        logging.error(f"Error connection with Pancake: {e}")
        raise HTTPException(status_code=500, detail=f"Error connection with Pancake: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")