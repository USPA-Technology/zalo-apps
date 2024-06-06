from __future__ import annotations

from typing import List, Optional, Any , Dict

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
    data: List[DatumCustomers] = None
    removeId: Optional[List[int]] = None



# ResponseModel return order list
""" 
Response from GET of model ReqOrderList
"""
class OrderPayment(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[int] = None
    statusValue: Optional[str] = None
    transDate: Optional[str] = None
    bankAccount: Optional[str] = None
    accountId: Optional[int] = None

class OrderDetails(BaseModel):
    productId: Optional[int] = None
    productCode: Optional[str] = None
    productName: Optional[str] = None
    isMaster: Optional[bool] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    discountRatio: Optional[float] = None
    discount: Optional[float] = None
    note: Optional[str] = None



class OrderPartnerDelivery(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    contactNumber: Optional[str] = None
    email: Optional[str] = None


class OrderDelivery(BaseModel):
    deliveryCode: Optional[str] = None
    type: Optional[int] = None
    price: Optional[float] = None
    receiver: Optional[str] = None
    contactNumber: Optional[str] = None
    address: Optional[str] = None
    locationId: Optional[int] = None
    locationName: Optional[str] = None
    weight: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    partnerDeliveryId: Optional[int] = None
    partnerDelivery: Optional[OrderPartnerDelivery] = None


class DatumOrders(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    purchaseDate: Optional[str] = None
    branchId: Optional[int] = None
    branchName: Optional[str] = None
    soldById: Optional[int] = None
    soldByName: Optional[str] = None
    customerId: Optional[int] = None
    customerCode: Optional[str] = None
    customerName: Optional[str] = None
    total: Optional[float] = None
    totalPayment: Optional[float] = None
    discountRatio: Optional[float] = None
    discount: Optional[float] = None
    status: Optional[int] = None
    statusValue: Optional[str] = None
    description: Optional[str] = None
    usingCod: Optional[bool] = None
    payments: Optional[List[OrderPayment]] = None
    orderDetails: Optional[List[OrderDetails]] = None
    orderDelivery: Optional[OrderDelivery] = None
    retailerId: Optional[int] = None
    modifiedDate: Optional[str] = None
    createdDate: Optional[str] = None


class RespOrderList(BaseModel):
    total: Optional[int] = None 
    pageSize: Optional[int] = None
    data: Optional[List[DatumOrders]] = None

# ResponseModel return invoices list
""" 
Response from GET of model ReqInvoiceList
"""
class InvoicePayment(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[int] = None
    statusValue: Optional[str] = None
    transDate: Optional[str] = None
    bankAccount: Optional[str] = None
    accountId: Optional[int] = None

class InvoiceOrderSurcharge(BaseModel):
    id: Optional[int] = None
    invoiceId: Optional[int] = None
    surchargeId: Optional[int] = None
    surchargeName: Optional[str] = None
    surValue: Optional[float] = None
    price: Optional[float] = None
    createdDate: Optional[str] = None

class ProductBatchExpire(BaseModel):
    id: Optional[int] = None
    productId: Optional[int] = None
    batchName: Optional[str] = None
    fullNameVirgule: Optional[str] = None
    createdDate: Optional[str] = None
    expireDate: Optional[str] = None

class InvoiceDetails(BaseModel):
    productId: Optional[int] = None
    productCode: Optional[str] = None
    productName: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    discountRatio: Optional[float] = None
    discount: Optional[float] = None
    note: Optional[str] = None
    serialNumbers: Optional[str] = None
    productBatchExpire: Optional[ProductBatchExpire] = None

class SaleChannel(BaseModel):
    IsNotDelete: Optional[bool] = None
    RetailerId: Optional[int] = None
    Position: Optional[int] = None
    IsActivate: Optional[bool] = None
    CreatedBy: Optional[int] = None
    CreatedDate: Optional[str] = None
    Id: Optional[int] = None
    Name: Optional[str] = None

class InvoicePartnerDelivery(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    contactNumber: Optional[str] = None
    email: Optional[str] = None

class InvoiceDelivery(BaseModel):
    deliveryCode: Optional[str] = None
    type: Optional[int] = None
    status: Optional[int] = None
    statusValue: Optional[str] = None
    price: Optional[float] = None
    receiver: Optional[str] = None
    contactNumber: Optional[str] = None
    address: Optional[str] = None
    locationId: Optional[int] = None
    locationName: Optional[str] = None
    usingPriceCod: Optional[bool] = None
    priceCodPayment: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    partnerDeliveryId: Optional[int] = None
    partnerDelivery: Optional[InvoicePartnerDelivery] = None

class DatumInvoices(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    purchaseDate: Optional[str] = None
    branchId: Optional[int] = None
    branchName: Optional[str] = None
    soldById: Optional[int] = None
    soldByName: Optional[str] = None
    customerId: Optional[int] = None
    customerCode: Optional[str] = None
    customerName: Optional[str] = None
    total: Optional[float] = None
    totalPayment: Optional[float] = None
    status: Optional[int] = None
    statusValue: Optional[str] = None
    usingCod: Optional[bool] = None
    createdDate: Optional[str] = None
    modifiedDate: Optional[str] = None
    payments: Optional[List[InvoicePayment]] = None
    invoiceOrderSurcharges: Optional[List[InvoiceOrderSurcharge]] = None
    invoiceDetails: Optional[List[InvoiceDetails]] = None
    SaleChannel: Optional[SaleChannel] = None
    invoiceDelivery: Optional[InvoiceDelivery] = None


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
    Id: Optional[int] = None
    Code: Optional[str] = None
    Name: Optional[str] = None
    Gender: Optional[bool] = None
    BirthDate: Optional[str] = None
    ContactNumber: Optional[str] = None
    Address: Optional[str] = None
    LocationName: Optional[str] = None
    Email: Optional[str] = None
    ModifiedDate: Optional[str] = None
    Type: Optional[int] = None
    Organization: Optional[str] = None
    TaxCode: Optional[str] = None
    Comments: Optional[str] = None


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