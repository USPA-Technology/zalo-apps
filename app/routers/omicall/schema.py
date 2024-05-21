from __future__ import annotations

from typing import List, Optional

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
