from __future__ import annotations

from typing import List, Optional, Any  

from pydantic import BaseModel


# ResponseModel return customer list
""" 
Response from GET of model ReqCustomerList
"""
class DatumCustomers(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[bool | str] = None
    birthDate: Optional[str] = None
    contactNumber: Optional[str] = None
    address: Optional[str] = None
    locationName: Optional[str] = None
    wardName: Optional[str] = None
    email: Optional[str] = None
    organization: Optional[str] = None
    comments: Optional[str] = None
    taxCode: Optional[str] = None
    debt: Optional[float] = None
    totalInvoiced: Optional[float] = None
    totalPoint: Optional[float] = None
    totalRevenue: Optional[float] = None
    retailerId: Optional[int] = None
    modifiedDate: Optional[str] = None
    createdDate: Optional[str] = None
    rewardPoint: Optional[int] = None
    psidFacebook: Optional[int] = None

class RespCustomerList(BaseModel):
    total: Optional[int] = None
    pageSize: Optional[int] = None
    data: List[DatumCustomers]
    removeId: Optional[List[int]] = None



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


# [WEBHOOK] Response Model Order Update KiotViet
class WebhookOrderDetail(BaseModel):
    ProductId: str
    ProductCode: str
    ProductName: str
    Quantity: str
    Price: str
    Discount: str
    DiscountRatio: str

class WebhookDatumOrder(BaseModel):
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
    OrderDetails: List[WebhookOrderDetail]


class WebhookNotificationOrder(BaseModel):
    Action: str
    Data: List[WebhookDatumOrder]


class WebhookOrder(BaseModel):
    Id: str
    Attempt: str
    Notifications: List[WebhookNotificationOrder]


# [WEBHOOK] Response Model Customer Update KiotViet
class WebhookDatumCustomer(BaseModel):
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


class WebhookNotificationCustomer(BaseModel):
    Action: str
    Data: List[WebhookDatumCustomer]


class WebhookCustomer(BaseModel):
    Id: str
    Attempt: int
    Notifications: List[WebhookNotificationCustomer]

# [WEBHOOK] Response Model Invoice Update KiotViet
class WebhookPartnerDelivery(BaseModel):
    Code: str
    Name: str
    ContactNumber: str
    Address: str
    Email: str


class WebhookInvoiceDelivery(BaseModel):
    DeliveryCode: str
    Status: int
    StatusValue: str
    Type: Any
    Price: float
    Receiver: str
    ContactNumber: str
    Address: str
    LocationId: Any
    LocationName: str
    Weight: float
    Length: float
    Width: float
    Height: float
    PartnerDeliveryId: Any
    PartnerDelivery: WebhookPartnerDelivery


class WebhookInvoiceDetail(BaseModel):
    ProductId: int
    ProductCode: str
    ProductName: str
    Quantity: float
    Price: float
    Discount: Any
    DiscountRatio: float


class WebhookPayment(BaseModel):
    Id: int
    Code: str
    Amount: float
    AccountId: Any
    BankAccount: str
    Description: str
    Method: str
    Status: Any
    StatusValue: str
    TransDate: str


class WebhookDatumInvoice(BaseModel):
    Id: int
    Code: str
    PurchaseDate: str
    BranchId: int
    BranchName: str
    SoldById: int
    SoldByName: str
    CustomerId: Any
    CustomerCode: str
    CustomerName: str
    Total: float
    TotalPayment: float
    Discount: Any
    DiscountRatio: float
    Status: int
    StatusValue: str
    Description: str
    UsingCod: bool
    ModifiedDate: Any
    InvoiceDelivery: WebhookInvoiceDelivery
    InvoiceDetails: List[WebhookInvoiceDetail]
    Payments: List[WebhookPayment]


class WebHookNotificationInvoice(BaseModel):
    Action: str
    Data: List[WebhookDatumInvoice]


class WebHookInvoice(BaseModel):
    Id: str
    Attempt: int
    Notifications: List[WebHookNotificationInvoice]