from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError
from .schema import ModelKiotViet, Datum
from ...dependencies import is_valid_signature
from ...core.config import SECRET_KEY_WEBHOOK

signature = SECRET_KEY_WEBHOOK

router  = APIRouter()


ModelKiotViet.Notifications

@router.post("kiotviet/webhook/{secret}")
async def receive_webhook(data: ModelKiotViet, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data_customer_name": Datum.CustomerName}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
