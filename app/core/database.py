from pymongo import MongoClient
from app.core.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
user_collection = db["users"]
cv_collection = db["cvs"]