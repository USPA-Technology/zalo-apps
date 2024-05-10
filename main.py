import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import Depends, FastAPI, HTTPException
from app.core.config import ACCESS_TOKEN, scheduled_refresh_access_token
import schedule
import httpx
import json
import asyncio


DEV_MODE = os.getenv("DEV_MODE") == "true"
HOSTNAME = os.getenv("HOSTNAME")
FOLDER_RESOURCES = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
FOLDER_TEMPLATES = FOLDER_RESOURCES + "templates"

# init FAST API zaloapp
zaloapp = FastAPI()
origins = ["*"]
zaloapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
zaloapp.mount("/resources", StaticFiles(directory=FOLDER_RESOURCES), name="resources")
templates = Jinja2Templates(directory=FOLDER_TEMPLATES)


@zaloapp.get("/", response_class=HTMLResponse)
async def root(request: Request):
    ts = int(time.time())
    data = {"request": request, "HOSTNAME": HOSTNAME, "DEV_MODE": DEV_MODE, 'timestamp': ts}
    return templates.TemplateResponse("index.html", data)

@zaloapp.get("/zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", response_class=HTMLResponse)
async def zalo_verifier(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("zalo_verifierFkAJ0kdG000gtefTzgq9OptIWcBHf54zCp4s.html", data)


# Lay danh sach khach hang quan tam OA
@zaloapp.get('/getfollowers/')
async def get_followers():
    api_url = "https://openapi.zalo.me/v2.0/oa/getfollowers"
    access_token = ACCESS_TOKEN
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params={"data": json.dumps({"offset":0,"count":20,"tag_name":""})}, headers={"access_token": access_token})
            users_follow = response.json()['data']['followers']
            # user_ids = [follower["user_id"] for follower in users_follow]
            # db_profile.insert({"user_id_zalo": user_ids})
            # db_profile.insert_many({"user_id_zalo": users_follow})
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")


# Lay thong tin nguoi dung quan tam OA
@zaloapp.get('/getprofile/{user_id}')
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
@zaloapp.post('/tagfollower/{user_id}')
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
@zaloapp.post('/send_message_promotion/')
async def send_message(data: dict): # messege_template in models 
    api_url = "https://openapi.zalo.me/v3.0/oa/message/promotion"
    access_token = ACCESS_TOKEN
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=data, headers={"access_token": access_token})
            users_follow = response.json()
            return users_follow
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Zalo API: {e}")

# Nhan webhook
@zaloapp.post("/webhook")
async def receive_webhook(request: Request):
    result = await request.json()
    print(result)
    return result





# # Lên lịch chạy hàm scheduled_refresh_access_token vào 16:59:00 hàng ngày
# schedule.every().day.at("17:54:00").do(scheduled_refresh_access_token)

# def start_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# async def startup_event():
#     task = BackgroundTasks()
#     task.add_task(start_schedule)
#     print("Startup event activated!")
#     return {"message": "Refresh token success"}

# zaloapp.add_event_handler("startup", startup_event)
