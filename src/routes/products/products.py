from flask import Blueprint, jsonify
from src.db.products_db import getAll, getProductById
# import json

products = Blueprint("products",__name__)


@products.route("/getAll", methods = ["GET"])
def listAll():
    return getAll()
    # return "Returning all Listed products"

@products.route("/getProduct/<id>", methods = ["GET"])
def getProductbyId(id):
    return getProductById(id)
    # print("The id is ",id)

