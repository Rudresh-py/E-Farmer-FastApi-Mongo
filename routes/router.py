from typing import List
from fastapi import APIRouter
from jwt.exceptions import DecodeError
import jwt
from fastapi.security import HTTPBasic
from models.models import UserRegisterModel, UserLogin, ProductModel, Order, OrderStatus
from database.db import user_register_collection, product_collection, order_collection
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from bson import ObjectId
import shortuuid
import stripe

stripe.api_key = "YOUR_STRIPE_API_KEY"
router = APIRouter()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 500

stripe.api_key = "sk_test_51Lk2oZSHQ3xxH3ruXe6LsemyQQSTjHI0hV9a5VoOmzJTtJ282vK1Akfv7XW69183ignQaxI8hnGpyYzKJ0xpR5go00ufAE8rim"

STRIPE_WEBHOOK_SECRET = "pk_test_51Lk2oZSHQ3xxH3rupasgG1mBVxYEVP3Jfi4AW4jzlIWdGEEcGcT6raWKbwZWPUZf4fmovfSVXGKzPVlutRSH1bnb00e1sLwMqt"


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
    generate_role_id(user)
    user.password = get_password_hash(password=user.password)
    user_dict = user.dict()
    result = user_register_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


def generate_role_id(user: UserRegisterModel):
    s = shortuuid.ShortUUID(alphabet="0123456789")
    if user.is_farmer:
        farmer_id = "FARM" + s.random(length=5)
        user.farmerid = farmer_id
    elif user.is_aggregator:
        aggregator_id = "AGGR" + s.random(length=5)
        user.aggreid = aggregator_id


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
def create_product(product: ProductModel, user: UserRegisterModel = Depends(get_current_user)):
    product.created_at = datetime.utcnow()
    product.updated_at = datetime.utcnow()
    product = product.dict()
    product["user_id"] = user["_id"]
    product_id = product_collection.insert_one(product).inserted_id
    return {"post_id": str(product_id)}


@router.put("/products/{product_id}")
def update_product(product_id: str, product: ProductModel):
    product.updated_at = datetime.utcnow()
    product_dict = product.dict()
    updated_product = product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_dict})
    if updated_product.modified_count > 0:
        return {"message": "Product updated successfully"}
    else:
        return {"message": "Product not found"}


@router.get("/products", response_model=List[ProductModel])
def get_products():
    products = []
    for document in product_collection.find({}):
        document["user_id"] = str(document["user_id"])
        product_data = ProductModel(**document)
        products.append(product_data)
    return products


@router.get("/products/{product_id}")
def get_products(product_id: str):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product["user_id"] = str(product["user_id"])
        product = ProductModel(**product)
        return product
    else:
        return {"message": "Product not found"}


@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    product = product_collection.delete_one({"_id": ObjectId(product_id)})
    if product.deleted_count > 0:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.post("/payment_intent/{product_id}")
def create_payment_intent(product_id: str, user: UserRegisterModel = Depends(get_current_user)):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    intent = stripe.PaymentIntent.create(
        amount=int(product["price"]),
        currency="usd",
        description=f"Order: {product_id}",
        payment_method_types=["card"]  # Specify the payment method types
    )
    payment_intent_id = intent["id"]

    if intent.status == "requires_payment_method":
        return {"client_secret": intent.client_secret}

    if intent.status == "succeeded":
        # Process the payment and create the order
        order = Order()
        order_dict = order.dict()
        order_dict["user_id"] = str(user["_id"])
        order_dict["order_id"] = str(product["user_id"])
        order_dict["product_id"] = str(product["_id"])
        order_dict["product_name"] = product["name"]
        order_dict["price"] = str(product["price"])
        order_dict["payment_id"] = payment_intent_id
        order_dict["created_at"] = datetime.utcnow()
        order_dict["updated_at"] = datetime.utcnow()
        order_id = order_collection.insert_one(order_dict).inserted_id
        return {"message": f"Payment successful for Order_id: {str(order_id)}"}
    else:
        return {"message": "Payment failed"}

