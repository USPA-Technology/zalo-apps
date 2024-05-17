from __future__ import annotations

from typing import List

from pydantic import BaseModel


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

