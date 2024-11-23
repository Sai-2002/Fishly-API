from src.db.setup_db import db
from src.db.user_db import getUser, user
import json
from bson import ObjectId

collections_orders = db['orders']


def SerializeOrders(order):

    return {
        "_id": str(order["_id"]),
        "customer_id": str(order["customer_id"]),
        "transaction_id": order["transaction_id"],
        "cost" : order["cost"],
        "status": order["status"],
        "order": order["order"],
        "cuttingMethod": order["cuttingMethod"],
        "paymentMethod": order["paymentMethod"],
    }


def getOrderWithCustomer(id):

    userD = getUser(id=id)

    if not userD:
        return "No user found", 404

    orders = list(collections_orders.find({"customer_id": ObjectId(id)}))

    # print("ORder data from db : ", orders)
    
    # Serialize the user and their orders
    user_data = {
        "_id": str(userD["_id"]),
        "username": userD.get("username", ""),  # Ensure there's no KeyError if 'username' is missing
        "address": userD.get("address", ""),  # Default to empty string if 'address' is missing
        "mobile": userD.get("mobile", ""),  # Default to empty string if 'mobile' is missing
        "orders": [
            # {
            #     "_id": str(order["_id"]),
            #     "order": order.get("order", ""),  # Default to empty string if 'product' is missing
            #     "cuttingMethod": order.get("cuttingMethod",""),
            #     "paymentMethod": order["paymentMethod"],
            #     "transaction_id": order["transaction_id"],  # Default to 0 if 'quantity' is missing
            #     "cost": order.get("cost", 0.0),  # Default to 0.0 if 'price' is missing
            #     "status": order.get("status", "Order Placed"),  # Use 'pending' if 'status' is missing
            # }

            SerializeOrders(order) for order in orders
        ]
    }

    return user_data


def getAllUserWithOrders():
    
    users = list(user.find())
    
    # Fetch orders for each user and serialize their data
    all_users_data = []
    for us in users:
        user_data = getOrderWithCustomer(str(us["_id"]))
        all_users_data.append(user_data)
    
    return all_users_data

def getAllOrders():
    
    orders = collections_orders.find({})

    orders_list = [SerializeOrders(order=order) for order in orders]

    return json.dumps(orders_list), 200



def getOrdersByCId(id):
    result = collections_orders.find({"customer_id": ObjectId(id), "status": {"$ne":"Delivered"}})


    orders_list = [SerializeOrders(order=order) for order in result]

    print(orders_list)
    return orders_list,200

def updateStatusOfOrder(id, newStatus):
    
    results = collections_orders.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status":newStatus}}
    )

    print(results)

    if results.matched_count > 0:
        return "Status Update Successfully"
    
    else:
        return "Order Not found"


def placeOrder(order):

    collections_orders.insert_one(order)
    return "Order Placed",200