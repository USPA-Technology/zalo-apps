from __future__ import annotations

from typing import List

from pydantic import BaseModel


# RequestModel get customer list
""" 
GET: https://public.kiotapi.com/customers
"""
class ReqCustomerList(BaseModel):
    code: str | None = None
    name: str | None = None
    contactNumber: str | None = None
    lastModifiedFrom: str | None = None 
    pageSize: int | None = None
    currentItem: int | None = None
    orderBy: str
    orderDirection: str
    includeRemoveIds: bool
    includeTotal: bool
    includeCustomerGroup: bool
    birthDate: str
    groupId: int
    includeCustomerSocial: bool

# ResponseModel return customer list
""" 
Response from GET of model ReqCustomerList
"""
class RespDataCustomerList(BaseModel):
    id: str
    code: str
    name: str
    gender: bool
    birthDate: str
    contactNumber: str
    address: str
    locationName: str
    wardName: str
    email: str
    organization: str
    comments: str
    taxCode: str
    debt: float
    totalInvoiced: float
    totalPoint: float
    totalRevenue: float
    retailerId: int
    modifiedDate: str
    createdDate: str
    rewardPoint: int
    psidFacebook: int

class RespCustomerList(BaseModel):
    total: int
    pageSize: int
    data: List[RespDataCustomerList]
    removeId: List[int]

































class OrderDetail(BaseModel):
    ProductId: str
    ProductCode: str
    ProductName: str
    Quantity: str
    Price: str
    Discount: str
    DiscountRatio: str

class Datum(BaseModel):
    Id: str
    Code: str
    PurchaseDate: str
    BranchId: str
    SoldById: str
    SoldByName: str
    CustomerId: str
    CustomerCode: str
    CustomerName: str
    Total: str
    TotalPayment: str
    Discount: str
    DiscountRatio: float | None = None
    Status: str
    StatusValue: str
    Description: str
    UsingCod: str
    ModifiedDate: str
    OrderDetails: List[OrderDetail]


class Notification(BaseModel):
    Action: str
    Data: List[Datum]


class ModelKiotViet(BaseModel):
    Id: str
    Attempt: str
    Notifications: List[Notification]


# Model Customer KiotViet

class DatumCustomer(BaseModel):
    Id: int
    Code: str
    Name: str
    Gender: bool
    BirthDate: str
    ContactNumber: str
    Address: str
    LocationName: str
    Email: str
    ModifiedDate: str
    Type: int
    Organization: str
    TaxCode: str
    Comments: str


class Notification(BaseModel):
    Action: str
    Data: List[DatumCustomer]


class ModelCustomer(BaseModel):
    Id: str
    Attempt: int
    Notifications: List[Notification]

