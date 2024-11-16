from src.db.setup_db import db
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


def getAllOrders():
    
    orders = collections_orders.find({})

    orders_list = [SerializeOrders(order=order) for order in orders]

    return json.dumps(orders_list), 200



def getOrdersByCId(id):
    result = collections_orders.find({"customer_id": ObjectId(id), "status": {"$ne":"Delivered"}})


    orders_list = [SerializeOrders(order=order) for order in result]

    print(orders_list)
    return orders_list,200

def updateStatusOfOrder(id):
    pass

def placeOrder(order):

    collections_orders.insert_one(order)
    return "Order Placed",200