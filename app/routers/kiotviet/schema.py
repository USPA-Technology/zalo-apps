from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


# ResponseModel return customer list
""" 
Response from GET of model ReqCustomerList
"""
class DatumCustomers(BaseModel):
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
    data: List[DatumCustomers]
    removeId: List[int]



# ResponseModel return order list
""" 
Response from GET of model ReqOrderList
"""
class OrderPayment(BaseModel):
    id: int
    code: str
    amount: float
    method: str
    status: int
    statusValue: str
    transDate: str
    bankAccount: str
    accountId: int


class OrderDetails(BaseModel):
    productId: int
    productCode: str
    productName: str
    isMaster: bool
    quantity: float
    price: float
    discountRatio: float
    discount: float
    note: str


class OrderPartnerDelivery(BaseModel):
    code: str
    name: str
    address: str
    contactNumber: str
    email: str


class OrderDelivery(BaseModel):
    deliveryCode: str
    type: int
    price: float
    receiver: str
    contactNumber: str
    address: str
    locationId: int
    locationName: str
    weight: float
    length: float
    width: float
    height: float
    partnerDeliveryId: int
    partnerDelivery: OrderPartnerDelivery


class DatumOrders(BaseModel):
    id: int
    code: str
    purchaseDate: str
    branchId: int
    branchName: str
    soldById: int
    soldByName: str
    customerId: int
    customerCode: str
    customerName: str
    total: float
    totalPayment: float
    discountRatio: float
    discount: float
    status: int
    statusValue: str
    description: str
    usingCod: bool
    payments: List[OrderPayment]
    orderDetails: OrderDetails
    orderDelivery: OrderDelivery
    retailerId: int
    modifiedDate: str
    createdDate: str


class RespOrderList(BaseModel):
    total: int
    pageSize: int
    data: List[DatumOrders]


# ResponseModel return invoices list
""" 
Response from GET of model ReqInvoiceList
"""
class InvoicePayment(BaseModel):
    id: int
    code: str
    amount: float
    method: str
    status: int
    statusValue: str
    transDate: str
    bankAccount: str
    accountId: int


class InvoiceOrderSurcharge(BaseModel):
    id: int
    invoiceId: int
    surchargeId: int
    surchargeName: str
    surValue: float
    price: float
    createdDate: str


class ProductBatchExpire(BaseModel):
    id: int
    productId: int
    batchName: str
    fullNameVirgule: str
    createdDate: str
    expireDate: str


class InvoiceDetails(BaseModel):
    productId: int
    productCode: str
    productName: str
    quantity: float
    price: float
    discountRatio: float
    discount: float
    note: str
    serialNumbers: str
    productBatchExpire: ProductBatchExpire


class SaleChannel(BaseModel):
    IsNotDelete: bool
    RetailerId: int
    Position: int
    IsActivate: bool
    CreatedBy: int
    CreatedDate: str
    Id: int
    Name: str


class InvoicePartnerDelivery(BaseModel):
    code: str
    name: str
    address: str
    contactNumber: str
    email: str


class InvoiceDelivery(BaseModel):
    deliveryCode: str
    type: int
    status: int
    statusValue: str
    price: float
    receiver: str
    contactNumber: str
    address: str
    locationId: int
    locationName: str
    usingPriceCod: bool
    priceCodPayment: float
    weight: float
    length: float
    width: float
    height: float
    partnerDeliveryId: int
    partnerDelivery: InvoicePartnerDelivery


class DatumInvoices(BaseModel):
    id: int
    code: str
    purchaseDate: str
    branchId: int
    branchName: str
    soldById: int
    soldByName: str
    customerId: int
    customerCode: str
    customerName: str
    total: float
    totalPayment: float
    status: int
    statusValue: str
    usingCod: bool
    createdDate: str
    modifiedDate: str
    payments: List[InvoicePayment]
    invoiceOrderSurcharges: List[InvoiceOrderSurcharge]
    invoiceDetails: InvoiceDetails
    SaleChannel: SaleChannel
    invoiceDelivery: InvoiceDelivery


class RespInvoiceList(BaseModel):
    total: int
    pageSize: int
    data: List[DatumInvoices]



























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

