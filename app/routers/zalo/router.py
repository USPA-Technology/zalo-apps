from fastapi import APIRouter
from fastapi import HTTPException
from core.config import ACCESS_TOKEN_ZALO
import httpx
import json
import logging

from .schema import ModelListUser

router = APIRouter(tags=['Zalo OA'])


# [API-GET] Get the customer list
@router.get('/kiotviet/customers')
async def get_customers(
    offset: int = 0,
    count: int = 50,
    tag_name: str = None,
    last_interation_period: str = 'L30D',
    is_follower: bool = True,

):

    api_url = "https://openapi.zalo.me/v3.0/oa/user/getlist"
    access_token = ACCESS_TOKEN_ZALO
    headers = {
        "access_token": access_token
    }

    while True:
        params = {
            "offset": offset,
            "count": count,
            "tag_name": tag_name,
            "last_interaction_period": last_interation_period,
            "is_follower": is_follower,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=api_url, headers=headers, params=params)
                response.raise_for_status()
                response_result = response.json()
                model_users = ModelListUser(**response_result)
                list_user_id = model_users.data.users 
                # Uncomment the following line if total records need to be dynamically fetched
                # total_records = customer_model.total
                if list_user_id:
                    for user_id in list_user_id:
                            await send_cdp_api_profile_retry(item)
                            logger.log_processed_item(current_item)
                            logging.info(f'Processed item: {current_item}')
                        current_item += 1
                        
                if current_item >= total_records:
                    break
                if current_item <= last_processed_item:
                    print("error current items")
                    break
        except httpx.RequestError as e:
            logging.error(f"Error connection with KiotViet: {e}")
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    
    return {"total": total_records, "data": all_customers}














# Retrieve a list of users in OA
@router.get('/getUsers/')
async def get_users():
    api_url = "https://openapi.zalo.me/v3.0/oa/user/getlist"
    access_token = ACCESS_TOKEN_ZALO
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url,
                                        params={"data": json.dumps({"offset": 0, "count": 20, "tag_name": "", "last_interaction_period": "L30D", "is_follower": True})},
                                        headers={"access_token": access_token})
            users_follow = response.json()
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with Zalo API")

# Retrieve user details
@router.get('/getUserDetails/{user_id}')
async def get_user_info(user_id: str):
    api_url = "https://openapi.zalo.me/v3.0/oa/user/detail"
    access_token = ACCESS_TOKEN_ZALO
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, 
                                        params={"data": json.dumps({"user_id": user_id})}, 
                                        headers={"access_token": access_token})
            user_detail = response.json()
            return user_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with Zalo API: {e}")


# Assign customer labels in OA
@router.post('/tagfollower/{user_id}')
async def tag_follower(user_id: str, tag_name: str):
    api_url = "https://openapi.zalo.me/v2.0/oa/tag/tagfollower"
    access_token = ACCESS_TOKEN_ZALO
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, params={"data": json.dumps({"user_id": user_id, "tag_name": tag_name})}, headers={"access_token": access_token})
            user_detail = response.json()
            return user_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Send media information to individual customers
@router.post('/send_message_promotion/')
async def send_message_media(data: dict): # messege_template in models 
    api_url = "https://openapi.zalo.me/v3.0/oa/message/promotion"
    access_token = ACCESS_TOKEN_ZALO
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=data, headers={"access_token": access_token})
            users_follow = response.json()
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")