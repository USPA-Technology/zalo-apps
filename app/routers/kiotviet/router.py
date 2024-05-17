from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import ValidationError
from .schema import ModelKiotViet, ModelCustomer
from ...dependencies import is_valid_signature
from ...core.config import SECRET_KEY_WEBHOOK
import json
from ...models import Profile, Event
import httpx

from typing import TYPE_CHECKING
import celery.states
from celery.result import AsyncResult

from ...worker.celery_app import celery_app
from ...worker.celery_worker import long_task, send_cdp_api

if TYPE_CHECKING:
    from celery import Task
    long_task: Task

signature = SECRET_KEY_WEBHOOK

router  = APIRouter()

@router.post("kiotviet/webhook/{secret}")
async def receive_webhook(data: ModelKiotViet, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.post("/kiotviet/customer/webhook/{secret}")
async def receive_webhook_customer_update(data: ModelCustomer, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")















WEBHOOK_SECRETS = {
    "/secure-webhook/profile": "profile_secret_key",
    "/secure-webhook/event": "event_secret_key"
}



def map_to_profile(data: dict) -> Profile:
    # Example mapping logic, customize according to your data structure
    return Profile(
        journeyMapIds=data.get("journey_map_ids", ""),
        dataLabels=data.get("data_labels", ""),
        crmRefId=data.get("crm_ref_id", ""),
        governmentIssuedIDs=data.get("government_issued_ids", ""),
        primaryAvatar=data.get("primary_avatar"),
        primaryEmail=data.get("primary_email", ""),
        secondaryEmails=data.get("secondary_emails"),
        primaryPhone=data.get("primary_phone", ""),
        secondaryPhones=data.get("secondary_phones"),
        firstName=data.get("first_name", ""),
        middleName=data.get("middle_name"),
        lastName=data.get("last_name", ""),
        gender=data.get("gender"),
        dateOfBirth=data.get("date_of_birth"),
        livingLocation=data.get("living_location"),
        livingCity=data.get("living_city"),
        jobTitles=data.get("job_titles"),
        workingHistory=data.get("working_history"),
        mediaChannels=data.get("media_channels"),
        personalInterests=data.get("personal_interests"),
        contentKeywords=data.get("content_keywords"),
        productKeywords=data.get("product_keywords"),
        totalCLV=data.get("total_clv"),
        totalCAC=data.get("total_cac"),
        totalTransactionValue=data.get("total_transaction_value"),
        saleAgencies=data.get("sale_agencies"),
        saleAgents=data.get("sale_agents"),
        notes=data.get("notes"),
        extAttributes=data.get("ext_attributes"),
        incomeHistory=data.get("income_history")
    )

def map_to_event(data: dict) -> Event:
    # Example mapping logic, customize according to your data structure
    return Event(
        eventId=data.get("event_id", ""),
        eventType=data.get("event_type", ""),
        eventTime=data.get("event_time", ""),
        eventData=data.get("event_data", {})
    )

async def send_to_cdp(profile: Profile = None, event: Event = None):
    url = "https://example.com/cdp-api"  # Replace with your CDP endpoint
    async with httpx.AsyncClient() as client:
        if profile:
            response = await client.post(url + "/profile", json=profile.model_dump())
            response.raise_for_status()
        elif event:
            response = await client.post(url + "/event", json=event.model_dump())
            response.raise_for_status()



@router.post("/secure-webhook/{webhook_type}")
async def secure_webhook(webhook_type: str, request: Request, signature: str):
    webhook_url = f"/secure-webhook/{webhook_type}"
    secret_key = WEBHOOK_SECRETS.get(webhook_url)
    
    if not secret_key:
        raise HTTPException(status_code=404, detail="Webhook URL not found")
    
    data = await request.json()
    data_str = json.dumps(data)
    
    if not is_valid_signature(secret_key, data_str, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        if webhook_type == "profile":
            profile = map_to_profile(data)
            await send_to_cdp(profile=profile)
        elif webhook_type == "event":
            event = map_to_event(data)
            await send_to_cdp(event=event)
        else:
            raise HTTPException(status_code=400, detail="Invalid webhook type")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    
    return {"message": "Secure webhook received and processed!"}
