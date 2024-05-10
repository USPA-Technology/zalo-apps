from fastapi import APIRouter
from fastapi import HTTPException
from ..core.config import ACCESS_TOKEN_ZALO
import httpx
import json

router = APIRouter(tags=['Zalo OA'])

# Retrieve a list of users in OA
@router.get('/getUsers/')
async def get_users():
    api_url = "https://openapi.zalo.me/v3.0/oa/user/getlist"
    access_token = ACCESS_TOKEN_ZALO
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url,
                                        params={"data": json.dumps({"offset": 0, "count": 20, "tag_name": ""})},
                                        headers={"access_token": access_token})
            users_follow = response.json()['data']['users']
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