from flask import Blueprint, jsonify
from src.db.products_db import getAll, getProductById
from flask_jwt_extended import get_jwt, jwt_required
# import json

products = Blueprint("products",__name__)


@products.route("/getAll", methods = ["GET"])
@jwt_required()
def listAll():
    claims = get_jwt()
    if claims['role'] != 'customer':
        return jsonify({"msg": "Access forbidden: Customer only!"}), 403
    return getAll()
    # return "Returning all Listed products"

@products.route("/getProduct/<id>", methods = ["GET"])
@jwt_required()
def getProductbyId(id):
    claims = get_jwt()
    if claims['role'] != 'customer':
        return jsonify({"msg": "Access forbidden: Customer only!"}), 403
    return getProductById(id)
    # print("The id is ",id)

