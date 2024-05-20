import asyncio

from celery import current_task
from celery.utils.log import get_task_logger
from routers.kiotviet.schema import ModelCustomer
from models import Profile, Event
from pydantic import BaseModel, Field
from .celery_app import celery_app
import httpx
from fastapi import HTTPException
import json

logger = get_task_logger(__name__)


@celery_app.task
def long_task(word: str) -> dict:
    logger.info("long_task called")
    asyncio.run(long_async_task())
    return {'result': word}


async def long_async_task():
    for i in range(10):
        await asyncio.sleep(1)




headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": '7TZMFpPZJNVWNYhiyJVgeZ',
    "tokenvalue": '9829510_2cbtrrVUbs4MnvyUgQVDjV'
}

api_url = 'https://dcdp.bigdatavietnam.org/api/profile/save'

# @celery_app.task
async def send_cdp_api(Data: ModelCustomer):
    logger.info("Process mapping data")
    result = json.loads(map_to_profile(Data))
    print(result)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=result)
            client_detail = response.json()
            return client_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with CDP: {e}")
    
    
    
    
def map_to_profile(data: ModelCustomer) -> Profile:
    # Example mapping logic, customize according to your data structure
    return Profile(
        journeyMapIds= "7TZMFpPZJNVWNYhiyJVgeZ",
        dataLabels= 'TestKiotViet',
        primaryEmail= data.Notifications[0].Data[0].Email,
        primaryPhone= data.Notifications[0].Data[0].ContactNumber,
        firstName= data.Notifications[0].Data[0].Name
        
    )