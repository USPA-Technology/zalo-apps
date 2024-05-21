from fastapi import APIRouter, Depends, HTTPException
from ..core.config import ACCESS_TOKEN_KIOTVIET
import httpx
import json
from typing import Annotated, List, Optional

router = APIRouter(tags=['KiotViet'])
retailer = 'bigdatavietnam'



# Get information about customer in KiotViet
@router.get('/getCustomerInfo/{client_code}')
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
    # params={"code": client_code} 
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


#[API-GET] Get the customer list in KiotViet
@router.get('/getCustomerList/')
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
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers, params=params)
            customer_list = response.json()
            return customer_list
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")
    
    
#[API-GET] Get order list in KiotViet
@router.get('/getOrdersList/')
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
            return orders
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connection with KiotViet: {e}")


@router.get('/getInvoiceList/')
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
    
    
