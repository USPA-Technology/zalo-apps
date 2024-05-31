from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

# [Truy xuất danh sách người dùng]
class UserID(BaseModel):
    user_id: str


class DataListUser(BaseModel):
    total: int
    count: int
    offset: int
    users: List[UserID]


class ModelListUser(BaseModel):
    data: Optional[DataListUser] = None
    error: Optional[int] = None
    message: Optional[str] = None

# [Truy xuất chi tiết thông tin người dùng]
class Avatars(BaseModel):
    field_240: str = Field(..., alias='240')
    field_120: str = Field(..., alias='120')


class TagsAndNotesInfo(BaseModel):
    notes: List[str]
    tag_names: List


class SharedInfo(BaseModel):
    address: str
    city: str
    district: str
    phone: str
    name: str


class DataUserDetail(BaseModel):
    user_id: str
    user_id_by_app: str
    display_name: str
    user_alias: str
    is_sensitive: bool
    user_last_interaction_date: str
    user_is_follower: bool
    avatar: str
    avatars: Avatars
    tags_and_notes_info: TagsAndNotesInfo
    shared_info: SharedInfo


class ModelUserDetail(BaseModel):
    data: Optional[DataUserDetail] = None
    error: Optional[int] = None
    message: Optional[str] = None 














class Avatars(BaseModel):
    field_240: str = Field(..., alias='240')
    field_120: str = Field(..., alias='120')


class TagsAndNotesInfo(BaseModel):
    notes: List[str]
    tag_names: List


class SharedInfo(BaseModel):
    address: str
    city: str
    district: str
    phone: str
    name: str


class Data(BaseModel):
    user_id: str
    user_id_by_app: str
    display_name: str
    user_alias: str
    is_sensitive: bool
    user_last_interaction_date: str
    user_is_follower: bool
    avatar: str
    avatars: Avatars
    tags_and_notes_info: TagsAndNotesInfo
    shared_info: SharedInfo


class Model(BaseModel):
    data: Optional[Data] = None
    error: Optional[int] = None
    message: Optional[str] = None
    
    
