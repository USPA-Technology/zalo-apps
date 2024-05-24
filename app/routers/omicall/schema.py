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


class ItemCustomer(BaseModel):
    id: str
    contact_type: str
    create_by: CreateBy
    last_update_by: LastUpdateBy
    created_date: int
    last_updated_date: int
    tenant_id: Optional[str] = None
    source_contact_id: Optional[str] = None
    public_id: Optional[str] = None
    user_owner_id: str
    attribute_structure: List[AttributeStructureItem]
    tags: Optional[List] = None
    business_type: List
    contact_categories: List[str]
    filter_contacts: Optional[List] = None
    total_interactive: int
    related_employee: Optional[List] = None
    ref_id: str
    ref_code: str
    tags_view: Optional[List] = None
    business_type_view: Optional[List] = None
    contact_categories_view: List[ContactCategoriesViewItem]


class PayloadCustomer(BaseModel):
    items: List[ItemCustomer]
    page_number: Optional[int] = None
    page_size: Optional[int] = None
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    has_next: bool
    next_page: Optional[int] = None
    has_previous: bool
    previous_page: Optional[int] = None
    extension: Any


class ModelCustomers(BaseModel):
    instance_id: Optional[str] = None
    payload: Optional[PayloadCustomer] = None
    instance_version: Optional[str] = None
    key_enabled: Optional[bool] = None
    status_code: Optional[int] = None



#[Response Model Validator] - Receive a list of call history
class UserItemCallHistory(BaseModel):
    full_name: str
    full_name_unsigned: str
    note: Any
    tag: Any


class CreateByCallHistory(BaseModel):
    id: Any
    name: str
    contact_id: Any
    avatar: Any
    gender: Any
    uuid: Any
    type: Any


class ItemCallHistory(BaseModel):
    transaction_id: str
    tenant_id: str
    direction: str
    source_number: str
    destination_number: str
    disposition: str
    bill_sec: int
    record_seconds: int
    time_start_to_answer: int
    recording_file: Any
    recording_file_url: Any
    recording_data: Any
    sip_user: str
    created_date: int
    last_updated_date: Any
    is_auto_call: bool
    ivr: str
    provider: str
    duration: int
    user: List[UserItemCallHistory]
    customer: Any
    state: Any
    call_uuid: Any
    from_number: str
    to_number: str
    hotline: str
    is_have_forward_out: bool
    bill_sec_forward_out: Any
    call_out_price: Optional[int] = None 
    note: str
    tag: List
    invite_failure_status: Any
    answer_sec: int
    autocall_uuid: Any
    sip_number: str
    phone_number: str
    create_by: CreateByCallHistory
    transfer_histories: List
    user_data_str: Any
    user_ref_code: Any
    endby_name: str
    hangup_cause: str
    sip_hangup_disposition: str
    hangup_cause_q850: int
    is_voicemail: bool
    recording_file_voicemail: Any
    domain_fusion: str
    send_num_retry: int
    time_start_call: int
    time_end_call: int
    out_of_working_time: bool
    sip_number_tags: Any
    evaluations: Any
    total_evaluate: Any
    internal_destination: Any
    classifies: Any


class PayloadCallHistory(BaseModel):
    next_page: int
    page_number: int
    has_previous: bool
    has_next: bool
    total_pages: int
    previous_page: int
    items: List[ItemCallHistory]
    total_items: int
    page_size: int


class ModelCallHistory(BaseModel):
    instance_id: Optional[str] = None
    payload: Optional[PayloadCallHistory] = None
    instance_version: Optional[str] = None
    key_enabled: Optional[bool] = None
    status_code: Optional[int] = None

