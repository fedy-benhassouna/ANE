
from pymongo import MongoClient
import bcrypt
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

def add_user(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    collection.insert_one({"username": username, "password": hashed})
    print(f"Inserted: {username}, Hashed Password: {hashed}")



# Prompt for desired password
password = input("Enter password for all users: ")
users = ["YasmineB", "FedyB", "JonathanC"]
for user in users:
    add_user(user, password)

print("Users added successfully.")
