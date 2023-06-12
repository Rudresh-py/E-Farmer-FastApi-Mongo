from fastapi import FastAPI
from routes.router import router

app = FastAPI()

app.include_router(router)

# from passlib.context import CryptContext
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# # Hashing a password
# password = "password"
# hashed_password = pwd_context.hash(password)
# print("Hashed Password:", hashed_password)
#
# # Verifying a password
# plain_password = "password"
# is_valid = pwd_context.verify(plain_password, hashed_password)
# print("Password Verification:", is_valid)
#
# # --- Authentication ---
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def authenticate_user(username: str, password: str):
#     user = user_register_collection.find_one({username: username})
#     if user and verify_password(password, get_password_hash(password)):
#         return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
#         # Retrieve the user based on the username (e.g., from the database)
#         user = authenticate_user(username, None)
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#         return user
#     except DecodeError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#
#
# # --- Database Connection ---
# mongo_url = "mongodb://localhost:27017/"
# db_name = "your_database_name"
# client = MongoClient(mongo_url)
# db: Database = client[db_name]
#
#
# # --- Models ---
# class User(BaseModel):
#     username: str
#     password: str
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# class Post(BaseModel):
#     title: str
#     content: str
#     user_id: ObjectId = Field(..., alias="user_id")
#
#     class Post(BaseModel):
#         title: str
#         content: str
#         user_id: ObjectId = Field(..., alias="user_id")
#
#         @validator("user_id")
#         def validate_object_id(cls, value):
#             if not isinstance(value, ObjectId):
#                 raise ValueError("Invalid ObjectId")
#             return str(value)
#
#
# # --- FastAPI App ---
# app = FastAPI()
#
#
# @app.post("/token")
# def login(user: User):
#     authenticated_user = authenticate_user(user.username, user.password)
#     if not authenticated_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": authenticated_user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.post("/posts", status_code=201)
# def create_post(post: Post, user: User = Depends(get_current_user)):
#     post_data = post.dict()
#     post_data["user_id"] = user.id  # Assuming the User model has an "id" field representing the user ID
#     post_id = db["posts"].insert_one(post_data).inserted_id
#     return {"post_id": str(post_id)}