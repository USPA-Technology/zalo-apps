import asyncio

from celery import current_task
from celery.utils.log import get_task_logger
from routers.kiotviet.schema import ModelCustomer
from models import Profile, Event
from pydantic import BaseModel, Field
from .celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def long_task(word: str) -> dict:
    logger.info("long_task called")
    asyncio.run(long_async_task())
    return {'result': word}


async def long_async_task():
    for i in range(10):
        await asyncio.sleep(1)
        
@celery_app.task
def send_cdp_api(Data: ModelCustomer):
    result = map_to_profile(Data)
    print(result)
    
    
    
def map_to_profile(data: ModelCustomer) -> Profile:
    # Example mapping logic, customize according to your data structure
    return Profile(
        firstName = data.Notifications[0].Data[0].Name
    )