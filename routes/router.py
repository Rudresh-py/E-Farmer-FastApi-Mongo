from typing import List

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient
from passlib.context import CryptContext

from models.models import UserRegisterModel, FertilizersModel
from database.db import user_register_collection, fertilizers_collection

router = APIRouter()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserRegisterModel)
def register_user(user: UserRegisterModel):
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    user_dict = user.dict()
    result = user_register_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


@router.get("/users", response_model=List[UserRegisterModel])
def get_users():
    users = []
    for document in user_register_collection.find():
        user_data = UserRegisterModel(**document)
        users.append(user_data)
    return users


@router.post("/fertilizers", response_model=FertilizersModel)
def add_fertilizers(fertilizer: FertilizersModel):
    fertilizer.created_at = datetime.utcnow()
    fertilizer.updated_at = datetime.utcnow()
    fertilizer_dict = fertilizer.dict()
    result = fertilizers_collection.insert_one(fertilizer_dict)
    fertilizer_dict["_id"] = str(result.inserted_id)
    return fertilizer_dict


@router.get("/fertilizers", response_model=List[FertilizersModel])
def get_fertilizers():
    fertilizers = []
    for document in fertilizers_collection.find():
        fertilizer_data = FertilizersModel(**document)
        fertilizers.append(fertilizer_data)
    return fertilizers

#
#
# # Create Fertilizer
# @app.post("/fertilizers")
# async def create_fertilizer(fertilizer: FertilizersModel):
#     fertilizer.created_at = datetime.utcnow()
#     fertilizer.updated_at = datetime.utcnow()
#     result = await collection.insert_one(fertilizer.dict())
#     return {"id": str(result.inserted_id)}
#
# # Get Fertilizer
# @app.get("/fertilizers/{fertilizer_id}")
# async def get_fertilizer(fertilizer_id: str):
#     fertilizer = await collection.find_one({"_id": fertilizer_id})
#     if fertilizer:
#         return fertilizer
#     else:
#         return {"message": "Fertilizer not found"}
#
# # Update Fertilizer
# @app.put("/fertilizers/{fertilizer_id}")
# async def update_fertilizer(fertilizer_id: str, fertilizer: FertilizersModel):
#     fertilizer.updated_at = datetime.utcnow()
#     result = await collection.update_one({"_id": fertilizer_id}, {"$set": fertilizer.dict()})
#     if result.modified_count == 1:
#         return {"message": "Fertilizer updated successfully"}
#     else:
#         return {"message": "Fertilizer not found"}
#
# # Delete Fertilizer
# @app.delete("/fertilizers/{fertilizer_id}")
# async def delete_fertilizer(fertilizer_id: str):
#     result = await collection.delete_one({"_id": fertilizer_id})
#     if result.deleted_count == 1:
#         return {"message": "Fertilizer deleted successfully"}
#     else:
#         return {"message": "Fertilizer not found"}
#
# # Get All Fertilizers
# @app.get("/fertilizers")
# async def get_all_fertilizers():
#     fertilizers = await collection.find().to_list(length=None)
#     return fertilizers
