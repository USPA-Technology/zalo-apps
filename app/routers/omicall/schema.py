from __future__ import annotations

from typing import List, Optional, Any

from pydantic import BaseModel


class CreateBy(BaseModel):
    contact_id: str
    id: str
    name: str


class Customer(BaseModel):
    full_name: str
    full_name_unsigned: str


class UserItem(BaseModel):
    full_name: str
    full_name_unsigned: str


class WebhookModelCall(BaseModel):
    """ 
    Nhận dữ liệu cuộc gọi từ Webhook trả về:
    """
    answer_sec: Optional[int] = None
    bill_sec: Optional[int] = None
    call_out_price: Optional[float] = None
    create_by: Optional[CreateBy] = None
    created_date: Optional[int] = None
    customer: Optional[Customer] = None
    destination_number: Optional[str] = None
    direction: Optional[str] = None
    domain_fusion: Optional[str] = None
    duration: Optional[int] = None
    endby_name: Optional[str] = None
    from_number: Optional[str] = None
    hotline: Optional[str] = None
    is_auto_call: Optional[bool] = None
    is_have_forward_out: Optional[bool] = None
    ivr: Optional[str] = None
    last_updated_date: Optional[int] = None
    note: Optional[str] = None
    phone_number: Optional[str] = None
    provider: Optional[str] = None
    record_seconds: Optional[int] = None
    recording_file_url: Optional[str] = None
    send_num_retry: Optional[int] = None
    sip_number: Optional[str] = None
    sip_user: Optional[str] = None
    source_number: Optional[str] = None
    state: Optional[str] = None
    tag: Optional[List] = None
    tenant_id: Optional[str] = None
    time_end_call: Optional[int] = None
    time_start_call: Optional[int] = None
    time_start_to_answer: Optional[int] = None
    to_number: Optional[str] = None
    transaction_id: Optional[str] = None
    transfer_histories: Optional[List] = None
    user: Optional[List[UserItem]] = None



#[Response Model Validator] - Receive a list of customers 
class CreateBy(BaseModel):
    id: str
    name: str


class LastUpdateBy(BaseModel):
    id: str
    name: str
    action: str


class ValueItem(BaseModel):
    value_id: str
    display_value: Optional[str]
    data_type: str
    value_type: str
    actual_value: Any
    quantity_value: Any
    currency: Any
    ref_id: Any
    list_evaluation: Any
    country_code: Any


class AttributeStructureItem(BaseModel):
    identify: bool
    attribute_id: str
    field_code: str
    field_type: str
    function: Any
    formula: Any
    data_format: Any
    value: List[ValueItem]
    is_memory: Any


class ContactCategoriesViewItem(BaseModel):
    id: str
    name: str
    type: str
    types: Any
    parent_id: Any
    parent_name: Any
    level: int
    color: Any
    ref_id: Any


class Item(BaseModel):
    id: str
    contact_type: str
    create_by: CreateBy
    last_update_by: LastUpdateBy
    created_date: int
    last_updated_date: int
    tenant_id: str
    source_contact_id: str
    public_id: str
    user_owner_id: str
    attribute_structure: List[AttributeStructureItem]
    tags: List
    business_type: List
    contact_categories: List[str]
    filter_contacts: List
    total_interactive: int
    related_employee: List
    ref_id: str
    ref_code: str
    tags_view: List
    business_type_view: List
    contact_categories_view: List[ContactCategoriesViewItem]


class Payload(BaseModel):
    items: List[Item]
    page_number: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    next_page: int
    has_previous: bool
    previous_page: int
    extension: Any


class ModelCustomers(BaseModel):
    instance_id: Optional[str] = None
    payload: Optional[Payload] = None
    instance_version: Optional[str] = None
    key_enabled: Optional[bool] = None
    status_code: Optional[int] = None

# import json

# # Dữ liệu JSON response
# data = {
#     "instance_id": "stg",
#     "payload": {
#         "items": [
#             {
#                 "id": "622178ce7c56273236e79983",
#                 "contact_type": "contact",
#                 "create_by": {"id": "61adb1732108e22624a508cc", "name": "Ms.Vân"},
#                 "last_update_by": {"id": "61adb1732108e22624a508cc", "name": "Ms.Vân", "action": "excel"},
#                 "created_date": 1646360352433,
#                 "last_updated_date": 1665480003022,
#                 "tenant_id": "61adb1732108e22624a508c9",
#                 "source_contact_id": "61adb81c69e1322e7cef45c4",
#                 "public_id": "40722396-d239-4dc6-b2f9-737913f19d7e1647011523532",
#                 "user_owner_id": "61adb81c69e1322e7cef45b9",
#                 "attribute_structure": [
#                     {
#                         "identify": False,
#                         "attribute_id": "664d57c89748c37d2b35c258",
#                         "field_code": "full_name",
#                         "field_type": "single_text",
#                         "function": None,
#                         "formula": None,
#                         "data_format": None,
#                         "value": [
#                             {
#                                 "value_id": "664d57c89748c37d2b35c259",
#                                 "display_value": "Nguyễn Thị Hải Yến",
#                                 "data_type": "",
#                                 "value_type": "",
#                                 "actual_value": None,
#                                 "quantity_value": None,
#                                 "currency": None,
#                                 "ref_id": None,
#                                 "list_evaluation": None,
#                                 "country_code": None
#                             }
#                         ],
#                         "is_memory": None
#                     },
#                     {
#                         "identify": False,
#                         "attribute_id": "664d57c89748c37d2b35c25e",
#                         "field_code": "phone_number",
#                         "field_type": "phone",
#                         "function": None,
#                         "formula": None,
#                         "data_format": None,
#                         "value": [
#                             {
#                                 "value_id": "664d57c89748c37d2b35c25f",
#                                 "display_value": "0376817493",
#                                 "data_type": "personal",
#                                 "value_type": "Cá nhân",
#                                 "actual_value": None,
#                                 "quantity_value": None,
#                                 "currency": None,
#                                 "ref_id": None,
#                                 "list_evaluation": None,
#                                 "country_code": None
#                             }
#                         ],
#                         "is_memory": None
#                     },
#                     {
#                         "identify": False,
#                         "attribute_id": "664d57c89748c37d2b35c262",
#                         "field_code": "address",
#                         "field_type": "single_text",
#                         "function": None,
#                         "formula": None,
#                         "data_format": None,
#                         "value": [
#                             {
#                                 "value_id": "664d57c89748c37d2b35c263",
#                                 "display_value": "162 phương liệt ,thanh xuân,hà nôi, Phường Phương Liệt, Quận Thanh Xuân, Hà Nội",
#                                 "data_type": "",
#                                 "value_type": "",
#                                 "actual_value": None,
#                                 "quantity_value": None,
#                                 "currency": None,
#                                 "ref_id": None,
#                                 "list_evaluation": None,
#                                 "country_code": None
#                             }
#                         ],
#                         "is_memory": None
#                     }
#                 ],
#                 "tags": [],
#                 "business_type": [],
#                 "contact_categories": ["622060447c56273236dafb40"],
#                 "filter_contacts": [],
#                 "total_interactive": 0,
#                 "related_employee": [],
#                 "ref_id": "7306356",
#                 "ref_code": "KHSPE211015VCFH95WP",
#                 "tags_view": [],
#                 "business_type_view": [],
#                 "contact_categories_view": [
#                     {
#                         "id": "622060447c56273236dafb40",
#                         "name": "Online",
#                         "type": "contact",
#                         "types": None,
#                         "parent_id": None,
#                         "parent_name": None,
#                         "level": 1,
#                         "color": None,
#                         "ref_id": None
#                     }
#                 ]
#             }
#         ],
#         "page_number": 1,
#         "page_size": 50,
#         "total_items": 53615,
#         "total_pages": 1073,
#         "has_next": True,
#         "next_page": 2,
#         "has_previous": False,
#         "previous_page": 1,
#         "extension": None
#     },
#     "instance_version": "1.2.164",
#     "key_enabled": False,
#     "status_code": 9999
# }

# def get_contact_info(item):
#     info = {}
#     for attribute in item['attribute_structure']:
#         field_code = attribute['field_code']
#         if attribute['value']:
#             info[field_code] = attribute['value'][0]['display_value']
#         else:
#             info[field_code] = None
#     return info

# # Lấy thông tin từ items
# contacts = data['payload']['items']
# for contact in contacts:
#     contact_info = get_contact_info(contact)
#     print(contact_info)

# # Hàm get_contact_info sẽ trích xuất thông tin từ một mục liên hệ
# def get_contact_info(item):
#     info = {}
#     for attribute in item['attribute_structure']:
#         field_code = attribute['field_code']
#         if attribute['value']:
#             info[field_code] = attribute['value'][0]['display_value']
#         else:
#             info[field_code] = None
#     return info

# # Lấy thông tin từ items
# contacts = data['payload']['items']
# for contact in contacts:
#     contact_info = get_contact_info(contact)
#     print(contact_info)
    
    
    
# model = ModelCustomers(**data)
# print(model.model_dump())