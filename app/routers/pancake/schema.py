from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


# [PanCake - Danh sách khách hàng]
class ShopCustomerAddress(BaseModel):
    address: Optional[str] = None
    commune_id: Optional[str] = None
    country_code: Optional[int] = None
    district_id: Optional[str] = None
    full_address: Optional[str] = None
    full_name: Optional[str] = None
    id: Optional[str] = None
    phone_number: Optional[str] = None
    province_id: Optional[str] = None

class DatumCustomer(BaseModel):
    purchased_amount: Optional[int] = None
    tags: Optional[List[str]] = None
    list_voucher: Optional[List] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    currency: Optional[Any] = None
    order_count: Optional[int] = None
    shop_customer_addresses: Optional[List[ShopCustomerAddress]] = None
    user_block_id: Optional[Any] = None
    last_order_at: Optional[str] = None
    conversation_tags: Optional[List[str]] = None
    assigned_user_id: Optional[str] = None
    date_of_birth: Optional[Any] = None
    used_reward_point: Optional[Any] = None
    reward_point: Optional[float] = None
    id: Optional[str] = None
    count_referrals: Optional[int] = None
    current_debts: Optional[int] = None
    is_adjust_debts: Optional[Any] = None
    creator_id: Optional[Any] = None
    shop_id: Optional[int] = None
    customer_id: Optional[str] = None
    is_block: Optional[bool] = None
    returned_order_count: Optional[int] = None
    referral_code: Optional[str] = None
    total_amount_referred: Optional[Any] = None
    notes: Optional[List] = None
    inserted_at: Optional[str] = None
    level: Optional[Any] = None
    gender: Optional[str] = None
    is_discount_by_level: Optional[bool] = None
    creator: Optional[Any] = None
    order_sources: Optional[List[str]] = None
    fb_id: Optional[str] = None
    username: Optional[Any] = None
    active_levera_pay: Optional[bool] = None
    phone_numbers: Optional[List[str]] = None
    succeed_order_count: Optional[int] = None
    emails: Optional[List] = None


class ModelCustomer(BaseModel):
    data: Optional[List[DatumCustomer]] = None
    page_number: Optional[int] = None
    page_size: Optional[int] = None
    success: Optional[bool] = None
    total_entries: Optional[int] = None
    total_pages: Optional[int] = None
