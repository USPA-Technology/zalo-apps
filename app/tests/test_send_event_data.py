import http.client
import json

from datetime import datetime

now = datetime.now() # current date and time

import httpx
from fastapi import HTTPException
api_url = ''

headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "*",
    "tokenkey": '',
    "tokenvalue": ''
}
# print(headers)

test_metric = "purchase"


# get current datetime in format %Y-%m-%dT%H:%M:%S.%fZ
formatted_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

tracking_event = {
    # the target update profile's email
    'eventTime': '2024-05-08T10:51:25.110Z',
    'targetUpdatePhone': "0386816313",
    'tpname': "Bộ Everon EPC-24041 thuộc bộ sưu tập 2024 - 2025",  # TOUCHPOINT_NAME
    'tpurl': "https://www.everonvn.vn/chi-tiet/everon-epc24041.html",  # TOUCHPOINT_URL
    'tprefurl': "https://google.com",  # TOUCHPOINT_REFERRER_URL
    'eventdata': '{"itemtId": "2019010113333", "idType" : "SKU", quantity : 2}',  # custom event data
    'imageUrls': "https://www.everonvn.vn/chi-tiet/images/upload/hinhanh/EPC-24041.jpg",
    'metric': test_metric,
    'tsval': 5120100,
    'tscur': 'VND'
}


if test_metric == 'purchase' :
    shoppingCartItems = []
    shoppingCartItems.append({
        "name": "Bộ chăn bốn mùa Sắc Hạ ESC23002",
        "itemtId": "2750",
        "idType": "item_ID",
        "originalPrice": 5299000,
        "salePrice": 5299000,
        "quantity": 1,
        "currency": "VND",
        "supplierId": "",
        "couponCode": "",
        "fullUrl": "https://everon.com/bo-chan-bon-mua/bo-chan-bon-mua-sac-ha-esc23002-p2750.html",
        "imageUrl": "https://everon.com/images/products/2022/10/05/compress_square/4-mua_1664934649.jpg"
    })
    transaction_id = "DEMO_TRANSACTION_" + now.strftime("%m/%d/%Y, %H:%M:%S")
    tracking_event['scitems'] = json.dumps(shoppingCartItems)
    tracking_event['tsid'] = transaction_id


json_payload = tracking_event
print(json_payload)
# uri = '/api/event/save'
# connection.request('POST', uri, json_payload, headers)

# response = connection.getresponse()
# result = json.dumps(response.read().decode(), indent=2)
# print(result)

async def send_test_api():
    try:
        async with httpx.AsyncClient() as client:
            print(json)
            response = await client.post(url = api_url, headers=headers, json=json_payload)
            orders = response.json()
            return orders
    except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")

import asyncio

def test_send_test_api():
    orders = asyncio.run(send_test_api())
    print(orders)
    # Add your assertions here to validate the response
    
# Call the test function
test_send_test_api()