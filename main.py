import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import Depends, HTTPException
from app.core.config import ACCESS_TOKEN
from app.core.db import db_profile, sys_db
import requests
import httpx
import json

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
            response = await client.get(api_url, params={"data": json.dumps({"offset":0,"count":5,"tag_name":""})}, headers={"access_token": access_token})
            users_follow = response.json()["data"]["followers"]
            # user_ids = [follower["user_id"] for follower in users_follow]
            #     db_profile.insert({"user_id_zalo": user_id})
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
