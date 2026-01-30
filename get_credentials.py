from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "auth_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "oryzon")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Fetch all credentials
for user in collection.find({}, {"username": 1, "password": 1, "_id": 0}):
    print(user)
