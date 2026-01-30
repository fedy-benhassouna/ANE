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

# Delete all documents in the collection
result = collection.delete_many({})
print(f"Deleted {result.deleted_count} documents from '{COLLECTION_NAME}' collection in '{DB_NAME}' database.")
