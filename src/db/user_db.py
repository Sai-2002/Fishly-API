from src.db.setup_db import db
from bson import ObjectId


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

def updateAddress(id, address):
    filter_query = {"_id": ObjectId(id)}

    update_query = {
    "$set": {
        "address": address  # Replace 'new_key' and 'new_value' as needed
    }
    }

    result = user.update_one(filter_query, update_query)

    if result.modified_count > 0:
        return "Address Added Succefully!"
    else:
        return "No user found."


def getAddr(id):
    result = user.find_one({"_id": ObjectId(id), "address": {"$exists": True}})

    if result:
        return result["address"]
    else:
        return ""