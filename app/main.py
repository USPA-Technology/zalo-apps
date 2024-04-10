from fastapi import Depends, FastAPI, HTTPException, Form
from app.core.config import ACCESS_TOKEN
from app.core.db import db_profile, sys_db
import httpx
import json

app = FastAPI()


# Lay danh sach khach hang quan tam OA
@app.get('/getfollowers/')
async def get_followers():
    api_url = "https://openapi.zalo.me/v2.0/oa/getfollowers"
    access_token = ACCESS_TOKEN
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params={"data": json.dumps({"offset":0,"count":20,"tag_name":""})}, headers={"access_token": access_token})
            users_follow = response.json()["data"]["followers"]
            # user_ids = [follower["user_id"] for follower in users_follow]
            # db_profile.insert({"user_id_zalo": user_ids})
            # db_profile.insert_many({"user_id_zalo": users_follow})
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Lay thong tin nguoi dung quan tam OA
@app.get('/getprofile/{user_id}')
async def get_profile(user_id: str):
    api_url = "https://openapi.zalo.me/v2.0/oa/getprofile"
    access_token = ACCESS_TOKEN
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params={"data": json.dumps({"user_id": user_id})}, headers={"access_token": access_token})
            user_detail = response.json()
            return user_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Gan nhan nguoi dung
@app.post('/tagfollower/{user_id}')
async def tag_follower(user_id: str, tag_name: str):
    api_url = "https://openapi.zalo.me/v2.0/oa/tag/tagfollower"
    access_token = ACCESS_TOKEN
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, params={"data": json.dumps({"user_id": user_id, "tag_name": tag_name})}, headers={"access_token": access_token})
            user_detail = response.json()
            return user_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Gui tin truyen thong den khach hang ca nhan
@app.post('/get_message_promotion/')
async def get_message(data: dict): # messege_template in models 
    api_url = "https://openapi.zalo.me/v3.0/oa/message/promotion"
    access_token = ACCESS_TOKEN
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=data, headers={"access_token": access_token})
            users_follow = response.json()
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Run server uvicorn 
if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Optional: Start the server
    
