from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Optional


class UserRegisterModel(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: str
    password: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    farmerid: Optional[str] = None
    aggreid: Optional[str] = None
    photo: Optional[bytes] = None
    is_farmer: Optional[bool] = None
    is_aggregator: Optional[bool] = None
    created: Optional[str] = None
    updated: Optional[str] = None
