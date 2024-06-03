from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

# [Truy xuất danh sách người dùng]
class UserID(BaseModel):
    user_id: Optional[str] = None


class DataListUser(BaseModel):
    total: Optional[int] = None
    count: Optional[int] = None
    offset: Optional[int] = None
    users: Optional[List[UserID]] = None


class ModelListUser(BaseModel):
    data: Optional[DataListUser] = None
    error: Optional[int] = None
    message: Optional[str] = None

# [Truy xuất chi tiết thông tin người dùng]
class Avatars(BaseModel):
    field_240: Optional[str] = Field(None, alias='240')
    field_120: Optional[str] = Field(None, alias='120')


class TagsAndNotesInfo(BaseModel):
    notes: Optional[List[str]] = None
    tag_names: Optional[List] = None


class SharedInfo(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    phone: Optional[int] = None
    name: Optional[str] = None


class DataUserDetail(BaseModel):
    user_id: Optional[str] = None 
    user_id_by_app: Optional[str] = None
    display_name: Optional[str] = None
    user_alias: Optional[str] = None
    is_sensitive: Optional[bool] = None
    user_last_interaction_date: Optional[str] = None
    user_is_follower: Optional[bool] = None
    avatar: Optional[str] = None
    avatars: Optional[Avatars] = None
    tags_and_notes_info: Optional[TagsAndNotesInfo] = None
    shared_info: Optional[SharedInfo] = None


class ModelUserDetail(BaseModel):
    data: Optional[DataUserDetail] = None
    error: Optional[int] = None
    message: Optional[str] = None 