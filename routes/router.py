from typing import List

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.schemas import UserRegisterSchema, UserListSchema
from models.models import UserRegisterModel
from database.db import collection

router = APIRouter()


@router.post("/register", response_model=UserRegisterModel)
def register_user(user: UserRegisterModel):
    user_dict = user.dict()
    result = collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


@router.get("/users", response_model=List[UserRegisterModel])
def get_users():
    users = []
    for document in collection.find():
        user_data = UserRegisterModel(**document)
        users.append(user_data)
    return users


# @router.get("/users", response_model=List[UserRegisterModel])
# async def get_users():
#     users = []
#     cursor = collection.find()
#     async for document in await cursor.to_list(length=None):
#         user = UserRegisterModel(**document)
#         users.append(user)
#     return users

# @router.post("/register", response_model=UserRegisterSchema)
# async def register_user(item: UserRegisterSchema):
#     # Convert the FastAPI model to a dictionary
#     data = item.data.dict()
#
#     # Insert the data into MongoDB
#     inserted_data = collection.insert_one(data)
#
#     # Fetch the inserted data from MongoDB
#     registered_user = collection.find_one({"_id": inserted_data.inserted_id})
#
#     # Convert MongoDB document to FastAPI model
#     user = UserRegisterModel(**registered_user)
#
#     return UserRegisterSchema(data=user)
#
#
# @router.get("/users")
# async def get_users():
#     users = collection.find({})
#     # user_list = [UserRegisterModel(**user) for user in users]
#     newDocs = []
#     for doc in users:
#         newDocs.append({
#             "id": doc["_id"],
#             "username": doc["username"],
#             "password": doc["password"],
#         })
#         return newDocs
# return UserListSchema(data=user_list)
