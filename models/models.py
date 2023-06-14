from pydantic import BaseModel, EmailStr
from fastapi import UploadFile
from typing import Optional
from datetime import datetime

from pydantic.config import Enum


class UserRegisterModel(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str]
    password: str
    email: EmailStr = None
    address: Optional[str] = None
    pincode: Optional[str] = None
    farmerid: Optional[str] = None
    aggreid: Optional[str] = None
    photo: Optional[bytes] = None
    is_farmer: Optional[bool] = None
    is_aggregator: Optional[bool] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProductModel(BaseModel):
    name: Optional[str]
    desc: Optional[str]
    image: Optional[bytes] = None
    is_aggregator: Optional[bool] = None
    price: Optional[float] = None
    category: Optional[str]
    user_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class OrderStatus(str, Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    Delivered = "Delivered"


class Order(BaseModel):
    user_id: Optional[str]
    order_id: Optional[str]
    payment_id: Optional[str]
    product_id: Optional[str]
    product_name: Optional[str]
    price: Optional[str]
    # status: OrderStatus
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
