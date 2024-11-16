from src.db.setup_db import db
from bson import ObjectId
from flask import jsonify

from hashlib import sha256

# db = setup()

user = db['users']

user.create_index([("username", 1)], unique=True)

def SerializeOrders(user):

    return {
        "_id": str(user["_id"]),
        "username": user["username"],
        "address": user.get("address",""),
        "mobile": user["mobile"]
    }


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

def getUser(id):
    return user.find_one({"_id": ObjectId(id)}, {'password': 0,'role':0})

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


def getAllUser():
    customers = user.find({}, {'password': 0, 'role':0})

    customer_list = [SerializeOrders(customer) for customer in customers]

    return jsonify({
        "customer":customer_list,
    },200)



def getAddr(id):
    result = user.find_one({"_id": ObjectId(id), "address": {"$exists": True}})

    if result:
        return result["address"]
    else:
        return ""