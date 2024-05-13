from fastapi import Request, Response, status, APIRouter

from svix.webhooks import Webhook, WebhookVerificationError

secret = "whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw"

router = APIRouter()

@router.post("/webhook/", status_code=status.HTTP_204_NO_CONTENT)
async def webhook_handler(request: Request, response: Response):
    headers = request.headers
    payload = await request.body()

    try:
        wh = Webhook(secret)
        msg = wh.verify(payload, headers)
    except WebhookVerificationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    result = request.json()
    print(result)

    # Do something with the message...