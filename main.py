import os
import time
from dotenv import load_dotenv

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import Depends, FastAPI, HTTPException
from app.core.config import ACCESS_TOKEN, TOKEN_KEY_CDP_KiotViet, TOKEN_VALUE_CDP_KiotViet
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

@zaloapp.post("/webhook/kiotviet/customer")
async def receive_webhook_kiotviet(request: Request):
    result = await request.json()
    print(result)
    return result



@zaloapp.post("/webhook/kiotviet/invoice")
async def receive_webhook_kiotviet(request: Request):
    result = await request.json()
    print(result)
    return result


#-------------------------------------------------------Test--------
import http.client
from datetime import datetime
import json
from typing import List, Optional

@zaloapp.post("/webhook/kiotviet/order")
async def receive_webhook_kiotviet(request: Request):
    
    # Nhận dữ liệu JSON từ yêu cầu webhook
    webhook_data = await request.json()
    
    # Lấy danh sách thông báo từ dữ liệu webhook
    notifications = webhook_data.get('Notifications', [])
    
    # Duyệt qua từng thông báo
    for notification in notifications:
        
        # Lấy danh sách dữ liệu từ thông báo
        data_list = notification.get('Data', [])
        
        # Duyệt qua từng bản ghi dữ liệu
        for data in data_list:
            
            # Lấy thông tin từ dữ liệu
            
            # Id
            id = data.get('Id')
            
            # Thông tin chi tiết đơn hàng
            order_details = data.get('OrderDetails', [])
            
            # Lặp qua từng sản phẩm trong đơn hàng
            for order_detail in order_details:
                
                # Tên sản phẩm
                product_name = order_detail.get('ProductName')
                
                # Giá sản phẩm
                price = order_detail.get('Price')
                
                # Số lượng sản phẩm
                quantity = order_detail.get('Quantity')
                
                # ... tiếp tục lấy các thông tin khác
                
                # Xây dựng sự kiện theo định dạng mong muốn
                
                # Thời gian sự kiện
                event_time = datetime.now().isoformat()
                
                # Dữ liệu sự kiện
                event_data = {
                    'idType': 'SKU',
                    'itemId': id,
                    'quantity': quantity
                }
                
                # Xây dựng thông tin sự kiện
                tracking_event = {
                    'eventTime': event_time,
                    'tpname': product_name,
                    'eventdata': json.dumps(event_data),
                    'metric': 'purchase',
                    'tsval': price,
                    'tscur': 'VND',
                    # Thêm các thông tin khác nếu cần
                }
                
                # Gửi sự kiện đến hệ thống theo yêu cầu
                
                # Chuyển đổi dữ liệu sự kiện sang định dạng JSON
                json_payload = json.dumps(tracking_event)
                
                # Gửi yêu cầu POST đến hệ thống với dữ liệu sự kiện
                uri = '/api/event/save'
                headers = {
                    "Content-Type": 'application/json',
                    "Access-Control-Allow-Origin": "*",
                    "tokenkey": TOKEN_KEY_CDP_KiotViet,
                    "tokenvalue": TOKEN_VALUE_CDP_KiotViet,
                }
                connection = http.client.HTTPSConnection('https://dcdp.bigdatavietnam.org')
                connection.request('POST', uri, json_payload, headers)
                
                # Nhận phản hồi từ hệ thống
                response = connection.getresponse()
                result = json.dumps(response.read().decode(), indent=2)
                print(result)
                
    return 'Success'














