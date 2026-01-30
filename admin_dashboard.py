
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables from .env
MONGO_URI="mongodb+srv://fedy_db_user:L86y7uoxNC5JGcH1@clusterauth.tuzgk0g.mongodb.net/?appName=Clusterauth"
DB_NAME = "auth_db"
COLLECTION_NAME = "oryzon"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Helper functions
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def get_all_users():
    return list(collection.find({}, {"username": 1}))

def add_user(username, password):
    if collection.find_one({"username": username}):
        return False, "Username already exists."
    hashed = hash_password(password)
    collection.insert_one({"username": username, "password": hashed})
    return True, "User added."

def update_user(user_id, new_username, new_password):
    hashed = hash_password(new_password)
    collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"username": new_username, "password": hashed}})
    return True, "User updated."

def delete_user(user_id):
    collection.delete_one({"_id": ObjectId(user_id)})
    return True, "User deleted."

def authenticate(username, password):
    user = collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True
    return False

# Streamlit UI
st.title("Admin Dashboard - User Management")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.success("Logged in!")
        else:
            st.error("Invalid credentials.")
    st.stop()

st.subheader("Manage Users")
users = get_all_users()
usernames = [u["username"] for u in users]
user_ids = [str(u["_id"]) for u in users]

# Add user
with st.form("add_user_form"):
    st.write("Add New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    submitted = st.form_submit_button("Add User")
    if submitted:
        ok, msg = add_user(new_username, new_password)
        if ok:
            st.success(msg)
            st.experimental_rerun()
        else:
            st.error(msg)

# Edit user
selected_user = st.selectbox("Select user to edit", options=usernames, index=0 if usernames else None)
if selected_user:
    user_idx = usernames.index(selected_user)
    user_id = user_ids[user_idx]
    with st.form("edit_user_form"):
        st.write(f"Edit User: {selected_user}")
        edit_username = st.text_input("Username", value=selected_user)
        edit_password = st.text_input("New Password", type="password")
        update = st.form_submit_button("Update User")
        if update:
            ok, msg = update_user(user_id, edit_username, edit_password)
            if ok:
                st.success(msg)
                st.experimental_rerun()
            else:
                st.error(msg)

# Delete user
selected_user_del = st.selectbox("Select user to delete", options=usernames, index=0 if usernames else None, key="delete")
if selected_user_del:
    user_idx_del = usernames.index(selected_user_del)
    user_id_del = user_ids[user_idx_del]
    if st.button(f"Delete {selected_user_del}"):
        ok, msg = delete_user(user_id_del)
        if ok:
            st.success(msg)
            st.experimental_rerun()
        else:
            st.error(msg)
