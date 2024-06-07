from fastapi import APIRouter
from fastapi import HTTPException
from core.config import ACCESS_TOKEN_ZALO, ACCESS_TOKEN_ZALO_OA_EVERON
import httpx
import json
import logging

from .schema import ModelListUser, ModelUserDetail, UserID
from .tasks import send_cdp_api_profile_retry
from dependencies import ProcessedItemLogger

router = APIRouter(tags=['Zalo OA'])

# Config logging
logging.basicConfig(filename='customer_retrieval_zalo.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = ProcessedItemLogger()



# [API-GET] Get the customer list
@router.get('/zalo/users')
async def get_user_list_id(
    offset: int = 0,
    count: int = 50,
    tag_name: str = None,
    last_interation_period: str = None,
    is_follower: bool = True,

):

    api_url = "https://openapi.zalo.me/v3.0/oa/user/getlist"
    access_token = ACCESS_TOKEN_ZALO_OA_EVERON
    headers = {
        "access_token": access_token
    }
    total_user_id = []
    last_processed_item = logger.get_last_processed_item()
    logging.info(f"Starting from last processed item: {last_processed_item}")
    
    while True:
        params = {
            "data": json.dumps({
                "offset": offset,
                "count": count,
                # "tag_name": tag_name,
                # "last_interaction_period": last_interation_period,
                "is_follower": is_follower,
            })
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=api_url, headers=headers, params=params)
                response.raise_for_status()
                response_result = response.json()
                print(response_result)
                # return response_result
                model_users = ModelListUser(**response_result)
                list_user_id = model_users.data.users
            
                if not list_user_id:
                    logging.info("No more users to process import data of from Zalo OA")
                    break
                for user in list_user_id:
                    # if offset > last_processed_item:
                            user_id_str = str(user.user_id)
                            await get_user_info(user_id_str)
                            total_user_id.append(user_id_str)
                            # logger.log_processed_item()
                            logging.info(f'Processed offset: {offset}')
                
                offset += count # Update offset by count to get the next set of result
            
        except httpx.RequestError as e:
            logging.error(f"Error connection with KiotViet: {e}")
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    
    total_user = len(total_user_id)
    return {f"Total user": {total_user}}
        
        
# Retrieve a list of users in OA
@router.get('/getUsers/')
async def get_users():
    api_url = "https://openapi.zalo.me/v3.0/oa/user/getlist"
    access_token = ACCESS_TOKEN_ZALO_OA_EVERON
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url,
                                        params={"data": json.dumps({"offset": 0, "count": 20, "tag_name": ""})},
                                        headers={"access_token": access_token})
            users_follow = response.json()["data"]["users"]
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with Zalo API")


# Retrieve user details
@router.get('/getUserDetails/{user_id}')
async def get_user_info(user_id: str):
    api_url = "https://openapi.zalo.me/v3.0/oa/user/detail"
    access_token = ACCESS_TOKEN_ZALO_OA_EVERON
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, 
                                        params={"data": json.dumps({"user_id": user_id})}, 
                                        headers={"access_token": access_token})
            user_detail = response.json()
            model_user_detail = ModelUserDetail(**user_detail)
            if model_user_detail.data:
                data_user_detail = model_user_detail.data
                await send_cdp_api_profile_retry(data_user_detail)
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
    
    
