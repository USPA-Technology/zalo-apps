from fastapi import Depends, FastAPI, HTTPException
from app.core.config import ACCESS_TOKEN
from app.core.db import db_profile, sys_db
import requests
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
            response = await client.get(api_url, params={"data": json.dumps({"offset":0,"count":5,"tag_name":""})}, headers={"access_token": access_token})
            users_follow = response.json()["data"]["followers"]
            # user_ids = [follower["user_id"] for follower in users_follow]  # Lấy user_id từ mỗi follower
            # # Luu user_id vào cơ sở dữ liệu ArangoDB
            # for user_id in user_ids:
            #     db_profile.insert({"user_id_zalo": user_id})
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

# Run server
if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Optional: Start the server
