from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import ValidationError
import httpx
import logging
from typing import List, Optional
import datetime
from .schema import (
                     WebhookCustomer, WebhookOrder, WebHookInvoice,
                     RespCustomerList,
                     RespOrderList,
                     RespInvoiceList,
                     RespProducts
                     )
from dependencies import is_valid_signature
from core.config import (SECRET_KEY_WEBHOOK, ACCESS_TOKEN_KIOTVIET, RETAILER,
                            )
from core.config_logs import ProcessedItemLoggerCustomers, ProcessedItemLoggerInvoices, ProcessedItemLoggerProducts

from .tasks import send_cdp_api_profile_retry, send_cdp_api_event_retry, import_cdp_csv_product

signature = SECRET_KEY_WEBHOOK
retailer = RETAILER
router  = APIRouter(tags=['KiotViet'])


# logging
logging.basicConfig(filename='everon_demo_etl_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger_customers = ProcessedItemLoggerCustomers()
logger_invoices = ProcessedItemLoggerInvoices()
logger_products = ProcessedItemLoggerProducts()

today = datetime.datetime.now().replace(hour=0, minute=0, second=0,microsecond=0).isoformat()


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

    if not headers["Retailer"] or not headers["Authorization"]:
        raise HTTPException(status_code=400, detail="Header Retailer hoặc Authorization bị thiếu hoặc không hợp lệ")
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
    page_size: int = 100,
    current_item: int = 0,
    order_by: str = 'id',
    order_direction: str = 'Asc',
    include_remove_ids: bool = False,
    include_total: bool = True,
    include_customer_group: bool = True,
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
    all_customers = []
    # total_records = 20
    last_processed_item = logger_customers.get_last_processed_item()
    current_item = 1

    logging.info(f"Starting from last processed item: {last_processed_item}")

    while True:
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
        try:
            async with httpx.AsyncClient() as client:
                print(current_item)
                response = await client.get(url=api_url, headers=headers, params=params)
                response.raise_for_status()
                response_result = response.json()
                customer_model = RespCustomerList(**response_result)
                items = customer_model.data
                # Uncomment the following line if total records need to be dynamically fetched
                total_records = customer_model.total
                if items:
                    for item in items:
                        print(current_item)
                        if current_item > last_processed_item:
                            await send_cdp_api_profile_retry(item)
                            logger_customers.log_processed_item(current_item)
                            logging.info(f'Processed item: {current_item}')
                        current_item += 1
                        
                if current_item > total_records:
                    break
                if current_item <= last_processed_item:
                    print("error current items")
                    break
        except httpx.RequestError as e:
            logging.error(f"Error connection with KiotViet: {e}")
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    
    return {"total": total_records, "data": all_customers}
    
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
                    await send_cdp_api_event_retry(item) 
            return orders
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")


# [API-GET] Get the invoice list 
@router.get('/kiotviet/invoices/')
async def get_invoices(
    # branch_ids: List[int] = None,
    # customer_ids: List[int] = None,
    customer_code: str = None,
    status_: int = 1,
    include_payment: bool = True,
    include_invoice_delivery: bool = True,
    last_modified_from: str = None,
    page_size: int = 100,
    current_item: int = None,
    to_date: str = None,
    order_by: str = "id",
    order_direction: str = 'Asc',
    # invoice_id: int = None,
    # created_date: str = None,
    # from_purchase_date: str = None
):

    api_url = "https://public.kiotapi.com/invoices"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": retailer,
        "Authorization": access_token
    }
    last_processed_item = logger_invoices.get_last_processed_item()
    # current_item = 1
    logging.info(f"Starting from last processed item: {last_processed_item}")
    while True:
        params = {
            # "branchIds": branch_ids,
            # "customerIds": customer_ids,
            # "customerCode": customer_code,
            "status": status_,
            "includePayment": include_payment,
            "includeInvoiceDelivery": include_invoice_delivery,
            "lastModifiedFrom": last_modified_from,
            "pageSize": page_size,
            "currentItem": current_item,
            "toDate": to_date,
            "orderBy": order_by,
            "orderDirection": order_direction,
            # "orderId": invoice_id,
            # "createdDate": created_date,
            # "fromPurchaseDate": from_purchase_date
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=headers, params=params)
                result = response.json()
                invoices = RespInvoiceList(**result)
                items = invoices.data
                total_records = invoices.total
                if items:
                    for item in items:
                        print(current_item)
                        if current_item > last_processed_item:
                            await send_cdp_api_event_retry(item)
                            logger_invoices.log_processed_item(current_item)
                            logging.info(f"Processed item: {current_item}")
                        current_item += 1
                if current_item > total_records:
                    break
                if current_item <= last_processed_item:
                    print('error current items')
            break        
                # return invoices
        except httpx.RequestError as e:
            logging.error(f"Error connection with KiotViet: {e}")
            raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
    return {"total": total_records, "data": current_item}



# [API-GET] Get the product list 
@router.get('/kiotviet/products/')
async def get_products(
    orderBy: str = "id",
    lastModifiedFrom: Optional[str] = None,
    pageSize: int = 100
):
    api_url = "https://public.kiotapi.com/products"
    access_token = ACCESS_TOKEN_KIOTVIET
    headers = {
        "Retailer": RETAILER,
        "Authorization": access_token
    }

    last_processed_item = logger_invoices.get_last_processed_item()
    logging.info(f"Starting from last processed item of product: {last_processed_item}")
    current_item_set = last_processed_item + 1
    total_records = 0

    while True:
        params = {
            "orderBy": orderBy,
            "lastModifiedFrom": lastModifiedFrom,
            "pageSize": pageSize,
            "currentItem": current_item_set
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=headers, params=params)
                response.raise_for_status()  # Check for HTTP request errors
                result = response.json()
                products = RespProducts(**result)
                items = products.data
                total_records = products.total
                if not items:
                    logging.info("No more items to process of product.")
                    break
                
                for item in items:
                    await import_cdp_csv_product(item)
                    logger_products.log_processed_item(current_item_set)
                    logging.info(f"Processed item of product: {current_item_set}")
                    current_item_set += 1
                    
                if current_item_set > total_records:
                    break
                
        except httpx.RequestError as e:
            logging.error(f"Connection error with KiotViet: {e}")
            raise HTTPException(status_code=500, detail=f"Connection error with KiotViet: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.text}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    return {"total": total_records, "data": current_item_set}
