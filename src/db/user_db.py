from src.db.setup_db import db

from hashlib import sha256

# db = setup()

user = db['users']

user.create_index([("username", 1)], unique=True)

def addNewUser(username: str, password: str):

    cred = {
        "username": username,
        "password": sha256(password.encode("utf-8")).hexdigest(),
        "role": "customer"
    }

    result = user.insert_one(cred)

    return f"Created new user {result.inserted_id}"


def getCred(username):
    return user.find_one({"username":username})