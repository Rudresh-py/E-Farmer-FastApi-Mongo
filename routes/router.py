from typing import List
from fastapi import APIRouter
from jwt.exceptions import DecodeError
import jwt
from fastapi.security import HTTPBasic
from models.models import UserRegisterModel, UserLogin, ProductModel
from database.db import user_register_collection, product_collection
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register", response_model=UserRegisterModel)
def register_user(user: UserRegisterModel):
    email_exist = user_register_collection.find_one({"email": user.email})
    username_exist = user_register_collection.find_one({"username": user.username})
    if email_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    elif username_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    user.password = get_password_hash(password=user.password)
    user_dict = user.dict()
    result = user_register_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/users", response_model=List[UserRegisterModel])
def get_users():
    users = []
    for document in user_register_collection.find({}):
        user_data = UserRegisterModel(**document)
        users.append(user_data)
    return users


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str):
    user = user_register_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        user = user_register_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return user
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/login")
def login(user: UserLogin):
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/products", status_code=201)
def create_post(product: ProductModel, user: UserRegisterModel = Depends(get_current_user)):
    post_data = product.dict()
    post_data["user_id"] = user["_id"]  # Assuming the User model has an "id" field representing the user ID
    post_id = product_collection.insert_one(post_data).inserted_id
    return {"post_id": str(post_id)}

