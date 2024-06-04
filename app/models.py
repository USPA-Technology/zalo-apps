""" 
Using Pydantic define Model of Customer Data
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Annotated


class Profile(BaseModel):
    journeyMapIds: str
    dataLabels: str
    crmRefId: Optional[str] = None
    governmentIssuedIDs: str = None
    primaryAvatar: Optional[str] = None
    primaryEmail: Optional[str] = None
    secondaryEmails: Optional[str] = None
    primaryPhone: Optional[str | None] = None
    secondaryPhones: Optional[str] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    gender: Optional[str | bool] = None
    dateOfBirth: Optional[str] = None  # yyyy-MM-dd
    livingLocation: Optional[str] = None  # the address of customer
    livingCity: Optional[str] = None  # the city where customer is living
    livingDistrict: Optional[str] = None
    livingWard: Optional[str] = None 
    jobTitles: Optional[str] = None  # the Job Title, e.g: CEO; Manager; Head of Sales
    workingHistory: Optional[str] = None
    mediaChannels: Optional[str] = None  # reachable media channels, E.g: facebook; linkedin; chat
    personalInterests: Optional[str] = None
    contentKeywords: Optional[str] = None
    productKeywords: Optional[str] = None
    totalCLV: Optional[float] = None  # this is example data
    totalCAC: Optional[float] = None  # this is example data
    totalTransactionValue: Optional[float] = None  # this is example data
    saleAgencies: Optional[str] = None  # the list of sales sources
    saleAgents: Optional[str] = None  # the list of sales persons
    notes: Optional[str] = None
    extAttributes: Optional[Dict[str, str]] = None
    incomeHistory: Optional[Dict[str, int]] = None
    socialMediaProfiles: Optional[Dict[str, str]] = None
    # applicationIDs: Optional[Dict[str, str]] = None

# class EventData(BaseModel):
#     itemtId: Optional[str] = None
#     idType: Optional[str] = None
#     quantity: Optional[str] = None


class Event(BaseModel):
    eventTime: Optional[str] = None
    targetUpdateEmail: Optional[str] = None
    targetUpdatePhone: Optional[str] = None
    tpname: Optional[str] = None
    tpurl: Optional[str] = None
    tprefurl: Optional[str] = None
    # eventdata: Optional[Dict] = None
    eventdata: Optional[str] = None
    imageUrls: Optional[str] = None
    metric: Optional[str] = None


class EventDataCall(BaseModel):
    transaction_id: Optional[str] = None
    tenant_id: Optional[str] = None
    direction: Optional[str] = None
    source_number: Optional[str] = None
    destination_number: Optional[str] = None
    disposition: Optional[str] = None
    duration: Optional[str] = None
    time_start_to_answer: Optional[str] = None
    provider: Optional[str] = None
    created_date: Optional[str] = None
    endby_name: Optional[str] = None
    hangup_cause: Optional[str] = None
    
    
    
    