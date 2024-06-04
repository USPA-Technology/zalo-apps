import http.client
import json

from datetime import datetime

now = datetime.now() # current date and time

import httpx
from fastapi import HTTPException
api_url = 'https://cdpeveron.dpoint.vn/api/profile/save'

headers = {
    "Content-Type": 'application/json',
    "Access-Control-Allow-Origin": "",
    "tokenkey": '1aV9CvRmD6WCvaWAjUOfGk',
    "tokenvalue": '434889_1Lsix9Je1X6GKbaqzRMda7'
}
sampleExtAttributes = {}
sampleSocialMediaProfiles = {"zalo": "123456789-213828"}
sampleIncomeHistory = {"2022-2023": 2000000, "2023-2024": 3000000}

profile = {
    "journeyMapIds": "1aV9CvRmD6WCvaWAjUOfGk",
    "dataLabels": " KOL person; investors",
    "crmRefId": "",
    "governmentIssuedIDs": "",
    "primaryAvatar": "https://cdn1.iconfinder.com/data/icons/user-pictures/100/male3-512.png",
    "primaryEmail": "",
    "secondaryEmails": "",
    "primaryPhone": "",
    "secondaryPhones": "",
    "firstName": "Bảo",
    "middleName": "",
    "lastName": "Laam",
    "gender": "male",  # or female
    "dateOfBirth": "1986-10-28",  # yyyy-MM-dd
    "livingLocation": "Ho Chi Minh City",  # the address of customer
    "livingCity": "",  # the city where customer is living
    "jobTitles": "Manager",  # the Job Title, e.g: CEO; Manager; Head of Sales
    "workingHistory": "Microsoft",
    # reachable media channels, E.g: facebook; linkedin; chat
    "mediaChannels": "website; facebook; linkedin; ",
    "personalInterests": "coding; business; ",
    "contentKeywords": "history; microsoft; product manament",
    "productKeywords": "history; microsoft; technology",
    "totalCLV": 9000,  # this is example data
    "totalCAC": 999,  # this is example data
    "totalTransactionValue": 200,  # this is example data
    "saleAgencies": "Agency A; Agency B; Agency C",  # the list of sales sources
    "saleAgents": "Mr.Thomas; Ms.Anna",  # the list of sales persons
    "notes": "this is a test",
    "extAttributes": json.dumps(sampleExtAttributes),
    "incomeHistory": json.dumps(sampleIncomeHistory),
    "socialMediaProfiles": json.dumps(sampleSocialMediaProfiles)
}


json_payload = json.dumps(profile)
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
            response = await client.post(url = api_url, headers=headers, json=profile)
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