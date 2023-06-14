from pymongo import MongoClient

MONGO_URI = "mongodb+srv://rudreshcg:Softsuave123@pythonmongo.bo5uu2w.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["e-farmer_db"]
# collection = db["your_collection_name"]
user_register_collection = db["user_register"]
product_collection = db["products"]
order_collection = db["orders"]

