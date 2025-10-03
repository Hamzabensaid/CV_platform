# app/core/config.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "cv_database")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
user_collection = db["users"]
cv_collection = db["cvs"]
