from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import ValidationError
import httpx
import requests
import json
from typing import TYPE_CHECKING, Annotated, List, Optional

from .schema import (
                     WebhookCustomer, WebhookOrder, WebHookInvoice,
                     RespCustomerList,
                     RespOrderList,
                     RespInvoiceList
                     )
from models import Profile, Event
from dependencies import is_valid_signature
from core.config import (SECRET_KEY_WEBHOOK,
                            ACCESS_TOKEN_KIOTVIET, RETAILER,
                            )
from .tasks import (send_cdp_api_profile,
                    send_cdp_api_profile_request,
                    send_with_retries,
                    send_cdp_api_event)

signature = SECRET_KEY_WEBHOOK
retailer = RETAILER

router  = APIRouter(tags=['KiotViet'])


# [WEBHOOK] - Customer Update
@router.post("/kiotviet/customer/webhook/{secret}")
async def receive_webhook_customer(data: WebhookCustomer, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# [WEBHOOK] - Order Update
@router.post("/kiotviet/order/webhook/{secret}")
async def receive_webhook_order(data: WebhookOrder, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
 
 # [WEBHOOK] - Invoice Update
@router.post("/kiotviet/invoice/webhook/{secret}")
async def receive_webhook_invoice(data: WebHookInvoice, secret: str):
    if not is_valid_signature(secret, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        model_data = data.model_dump()
        return {"message": "Webhook received", "data": model_data}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
    
# [API-GET] Get information about customer
@router.get('/kiotviet/customer/{client_code}')
async def get_customer_info(client_code: str):
    """
    Retrieve information about a customer in KiotViet.

    Args:
        client_code (str): The client code of the customer.

    Returns:
        json: Information about the customer.
    """
    api_url = f"https://public.kiotapi.com/customers/code/{client_code}"
    access_token = ACCESS_TOKEN_KIOTVIET 
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            client_detail = response.json()
            return client_detail
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")


# [API-GET] Get the customer list
@router.get('/kiotviet/customers')
async def get_customers(
    code: str = None,
    name: str = None,
    contact_number: str = None,
    last_modified_from: str = None,
    page_size: int = 20,
    current_item: int = None,
    order_by: str = None,
    order_direction: str = 'Asc',
    include_remove_ids: bool = False,
    include_total: bool = False,
    include_customer_group: bool = False,
    birth_date: str = None,
    group_id: int = None
):
    """
    Retrieve the list of customers in KiotViet with specified parameters.

    Args:
        code (str, optional): The code of the customer.
        name (str, optional): The name of the customer.
        contact_number (str, optional): The contact number of the customer.
        last_modified_from (str, optional): The last modified datetime.
        page_size (int, optional): The number of items per page.
        current_item (int, optional): The current page.
        order_by (str, optional): The field to order by.
        order_direction (str, optional): The order direction ('Asc' or 'Desc').
        include_remove_ids (bool, optional): Include removed ids.
        include_total (bool, optional): Include total.
        include_customer_group (bool, optional): Include customer group.
        birth_date (str, optional): The birth date of the customer.
        group_id (int, optional): The group id.

    Returns:
        json: Information about the customer list.
    """
    api_url = "https://public.kiotapi.com/customers"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    params = {
        "code": code,
        "name": name,
        "contactNumber": contact_number,
        "lastModifiedFrom": last_modified_from,
        "pageSize": page_size,
        "currentItem": current_item,
        "orderBy": order_by,
        "orderDirection": order_direction,
        "includeRemoveIds": include_remove_ids,
        "includeTotal": include_total,
        "includeCustomerGroup": include_customer_group,
        "birthDate": birth_date,
        "groupId": group_id
    }
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            results = response.json()
            customers = RespCustomerList(**results)
            items = customers.data
            if items:
                for item in items:
                    send_with_retries(item)
            return results
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
    
    
# [API-GET] Get order list
@router.get('/kiotviet/orders/')
async def get_orders(
    branch_ids: Optional[List[int]] = None,
    customer_ids: List[int] = None,
    customer_code: str = None,
    status: List[int] = None,
    include_payment: bool = True,
    include_order_delivery: bool = True,
    last_modified_from: str = None,
    page_size: int = 20,
    current_item: int = None,
    to_date: str = None,
    order_by: str = None,
    order_direction: str = 'Asc',
    created_date: str = None
):
    """
    Retrieve orders with specified parameters.

    Args:
        branch_ids (List[int], optional): The branch IDs.
        customer_ids (List[int], optional): The customer IDs.
        customer_code (str, optional): The customer code.
        status (List[int], optional): The order status.
        include_payment (bool, optional): Include payment information.
        include_order_delivery (bool, optional): Include order delivery information.
        last_modified_from (str, optional): The last modified datetime.
        page_size (int, optional): The number of items per page.
        current_item (int, optional): The current page.
        to_date (str, optional): The datetime until which orders are modified.
        order_by (str, optional): The field to order by.
        order_direction (str, optional): The order direction ('Asc' or 'Desc').
        created_date (str, optional): The created datetime.

    Returns:
        json: Information about the orders.
    """
    api_url = "https://public.kiotapi.com/orders"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    params = {
        "branchIds": branch_ids,
        "customerIds": customer_ids,
        "customerCode": customer_code,
        "status": status,
        "includePayment": include_payment,
        "includeOrderDelivery": include_order_delivery,
        "lastModifiedFrom": last_modified_from,
        "pageSize": page_size,
        "currentItem": current_item,
        "toDate": to_date,
        "orderBy": order_by,
        "orderDirection": order_direction,
        "createdDate": created_date
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers, params=params)
            orders = response.json()
            orders_model = RespOrderList(**orders)
            items = orders_model.data
            if items:
                for item in items:
                    await send_cdp_api_event(item) 
            return orders
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")


# [API-GET] Get the invoice list 
@router.get('/kiotviet/invoices/')
async def get_invoices(
    branch_ids: List[int] = None,
    customer_ids: List[int] = None,
    customer_code: str = None,
    status: List[int] = None,
    include_payment: bool = True,
    include_invoice_delivery: bool = True,
    last_modified_from: str = None,
    page_size: int = 20,
    current_item: int = None,
    to_date: str = None,
    order_by: str = None,
    order_direction: str = 'Asc',
    invoice_id: int = None,
    created_date: str = None,
    from_purchase_date: str = None
):
    """
    Retrieve invoices with specified parameters.

    Args:
        branch_ids (List[int], optional): The branch IDs.
        customer_ids (List[int], optional): The customer IDs.
        customer_code (str, optional): The customer code.
        status (List[int], optional): The invoice status.
        include_payment (bool, optional): Include payment information.
        include_invoice_delivery (bool, optional): Include invoice delivery information.
        last_modified_from (str, optional): The last modified datetime.
        page_size (int, optional): The number of items per page.
        current_item (int, optional): The current page.
        to_date (str, optional): The datetime until which invoices are modified.
        order_by (str, optional): The field to order by.
        order_direction (str, optional): The order direction ('Asc' or 'Desc').
        invoice_id (int, optional): The invoice ID.
        created_date (str, optional): The created datetime.
        from_purchase_date (str, optional): The datetime from which the transaction occurred.

    Returns:
        json: Information about the invoices.
    """
    api_url = "https://public.kiotapi.com/invoices"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    params = {
        "branchIds": branch_ids,
        "customerIds": customer_ids,
        "customerCode": customer_code,
        "status": status,
        "includePayment": include_payment,
        "includeInvoiceDelivery": include_invoice_delivery,
        "lastModifiedFrom": last_modified_from,
        "pageSize": page_size,
        "currentItem": current_item,
        "toDate": to_date,
        "orderBy": order_by,
        "orderDirection": order_direction,
        "orderId": invoice_id,
        "createdDate": created_date,
        "fromPurchaseDate": from_purchase_date
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers, params=params)
            invoices = response.json()
            return invoices
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
    

















""" 
import requests
from datetime import datetime

# Cấu hình API
api_url = "https://api.example.com/customers"
page_size = 100
current_item = 0
all_customers = []

# Các tham số có thể được sử dụng để lọc và sắp xếp dữ liệu
params = {
    "pageSize": page_size,
    "orderBy": "name",
    "orderDirection": "Asc",
    "includeTotal": True,
    "includeCustomerGroup": True,
    "includeCustomerSocial": True
}

while True:
    # Cập nhật tham số phân trang
    params["currentItem"] = current_item
    
    # Gọi API để lấy dữ liệu khách hàng theo trang
    response = requests.get(api_url, params=params)
    data = response.json()
    
    # Lấy danh sách khách hàng từ phản hồi API
    customers = data.get("data", [])
    
    if not customers:
        # Nếu danh sách khách hàng rỗng, thoát khỏi vòng lặp
        break
    
    # Thêm khách hàng vào danh sách tổng
    all_customers.extend(customers)
    
    
    # Tăng số mục hiện tại lên để lấy dữ liệu trang tiếp theo
    current_item += len(customers)

print(f"Tổng số khách hàng đã lấy: {len(all_customers)}")

def save_to_database(customers):
    # Thực hiện lưu dữ liệu khách hàng vào database
    pass  # Cần triển khai cụ thể tùy theo cấu trúc database của bạn

"""