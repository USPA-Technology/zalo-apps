import httpx
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def get_customer_info():
    api_url = "http://example.com/v1/kiotviet/customer/KH000001"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json",
    }

    # Validate headers
    for key, value in headers.items():
        if value is None:
            raise ValueError(f"Header {key} has a None value")

    logger.debug(f"Headers: {headers}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: raises an error for 4xx/5xx responses
        return response.json()
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        raise
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        raise

# Call the function (e.g., in an async context)
# await get_customer_info()
