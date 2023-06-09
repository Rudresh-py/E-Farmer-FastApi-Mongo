from pydantic import BaseModel
from typing import List
from models.models import UserRegisterModel


class UserRegisterSchema(BaseModel):
    data: UserRegisterModel


class UserListSchema(BaseModel):
    data: UserRegisterModel
