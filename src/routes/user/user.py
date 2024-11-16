from flask import Blueprint, request, jsonify
from bson import ObjectId

from src.db.user_db import updateAddress, getAddr, getUser
from src.db.orders_db import placeOrder, getOrdersByCId

user = Blueprint("user",__name__)

@user.route("/updateAddress/<id>", methods = ["POST"])
def addAddress(id):

    response = request.get_json()

    address = response["address"]

    return jsonify({
        "Result": updateAddress(id=id, address=address)
    })


@user.route("/getAddress/<id>", methods = ["GET"])
def getAddress(id):

    return jsonify({
        "Address": getAddr(id)} 
    )


@user.route("/addOrder", methods = ["POST"])
def addOrder():
    response = request.get_json()

    response["customer_id"] = ObjectId(response["customer_id"])

    return jsonify({
    
    "Result": placeOrder(response),
    "Success": "Order placed Successfully",
    })
    

@user.route("/getUserDetails/<id>", methods = ["GET"])
def getUserDetails(id):
    result = getUser(id)

    result["_id"] = str(result["_id"])
    return result


@user.route("/getOrders/<id>", methods = ["GET"])
def getOrders(id):
    return getOrdersByCId(id)
        