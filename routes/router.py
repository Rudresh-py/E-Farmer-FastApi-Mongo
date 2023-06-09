from typing import List

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.models import UserRegisterModel
from schemas.schemas import UserRegisterSchema, UserListSchema
from database.db import collection

router = APIRouter()


# @router.post("/register", response_model=UserRegisterModel)
# def register_user(user: UserRegisterModel):
#     user_dict = user.dict()
#     print(user_dict)
#     result = collection.insert_one(user_dict)
#     user_dict["_id"] = str(result.inserted_id)
#     return user_dict

@router.post("/register")
def register_user(user_data: UserRegisterSchema):
    user = user_data.data
    collection.insert_one(user.dict())  # Insert user data into MongoDB
    return {"message": "User registered successfully"}


@router.get("/users", response_model=List[UserRegisterModel])
def get_users():
    users = collection.find()
    return list(users)

#
# @router.get("/users", response_model=List[UserListSchema])
# def get_users():
#     users = []
#     for document in collection.find():
#         user_data = UserListSchema(data=document)
#         users.append(user_data)
#     return users
