from src.db.setup_db import db

from hashlib import sha256

# db = setup()

user = db['users']

user.create_index([("username", 1)], unique=True)

def addNewUser(username: str, password: str, mobileNumber: str):

    cred = {
        "username": username,
        "mobile": mobileNumber,
        "password": sha256(password.encode("utf-8")).hexdigest(),
        "role": "customer"
    }

    result = user.insert_one(cred)

    return result.inserted_id


def getCred(mobileNumber):
    return user.find_one({"mobile":mobileNumber})