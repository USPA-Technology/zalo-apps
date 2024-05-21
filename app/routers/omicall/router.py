from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from dependencies import is_valid_signature
from core.config import SECRET_KEY_WEBHOOK
from .schema import WebhookModelCall

signature = SECRET_KEY_WEBHOOK

router = APIRouter(tags=["OmiCall"])



# [WEBHOOK] - Get data call 
@router.post("kiotviet/order/webhook/{secret}")
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


