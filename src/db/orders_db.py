from src.db.setup_db import db
import json

collections_orders = db['orders']


def SerializeOrders(order):

    return {
        "_id": str(order["_id"]),
        "customer_id": str(order["customer_id"]),
        "razorpay_order_id": order["razorpay_order_id"],
        "cost" : order["cost"],
        "status": order["status"],
        "order": order["order"]
    }


def getAllOrders():
    
    orders = collections_orders.find({})

    orders_list = [SerializeOrders(order=order) for order in orders]

    return json.dumps(orders_list), 200



def getOrdersByCId(id):
    pass

def updateStatusOfOrder(id):
    pass

def placeOrder(order):

    collections_orders.insert_one(order)
    return "Order Placed",200