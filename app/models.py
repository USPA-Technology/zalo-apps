from pydantic import BaseModel
from typing import List, Dict, Optional

class Profile(BaseModel):
    journeyMapIds: str
    dataLabels: str
    crmRefId: str
    governmentIssuedIDs: str
    primaryAvatar: Optional[str] = None
    primaryEmail: str
    secondaryEmails: Optional[str] = None
    primaryPhone: str
    secondaryPhones: Optional[str] = None
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    gender: Optional[str] = None  # or female
    dateOfBirth: Optional[str] = None  # yyyy-MM-dd
    livingLocation: Optional[str] = None  # the address of customer
    livingCity: Optional[str] = None  # the city where customer is living
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

class Event(BaseModel):
    eventId: str
    eventType: str
    eventTime: str
    eventData: Dict[str, str]
