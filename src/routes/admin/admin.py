from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import json

from src.db.user_db import getAllUser
from src.db.products_db import insertProduct, updateProductById, deleteProduct
from src.db.orders_db import getAllOrders, getAllUserWithOrders, updateStatusOfOrder

admin = Blueprint("admin", __name__)

@admin.route("/addProduct", methods = ["POST"])
@jwt_required()
def addProduct():

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admins only!"}), 403

    if 'image' not in request.files:
        return json.dumps({"error":"No image available"}), 400

    product = {
    "name": request.form.get("name"),
    "weight": request.form.get("weight"),
    "servings": request.form.get("servings"),
    "pieces": request.form.get("pieces"),
    "description": request.form.get("description"),
    "macros":request.form.get("macros"),
    "price" : request.form.get("price"),
    "gravy": request.form.get("gravy"),
    "fry": request.form.get("fry"),
    "barbeque": request.form.get("barbeque")
    }

    image = request.files["image"]

    
    try:
        return insertProduct(product=product, image=image)
    
    except Exception as e:
        print(e)

@admin.route("/updateProduct/<id>", methods = ["POST"])
@jwt_required()
def updateProduct(id):

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admins only!"}), 403

    if 'image' not in request.files:
        return json.dumps({"error":"No image available"}), 400

    product = {
    "name": request.form.get("name"),
    "weight": request.form.get("weight"),
    "servings": request.form.get("servings"),
    "pieces": request.form.get("pieces"),
    "description": request.form.get("description"),
    "macros":request.form.get("macros"),
    "price" : request.form.get("price"),
    "gravy": request.form.get("gravy"),
    "fry": request.form.get("fry"),
    "barbeque": request.form.get("barbeque")
    }

    image = request.files["image"]

    try:
        return updateProductById(id, product, image)
    except Exception as e:
        print(e)

@admin.route("/deleteProduct/<id>")
@jwt_required()
def deleteProductById(id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admins only!"}), 403
    
    return deleteProduct(id)


@admin.route("/getAllOrders", methods = ["POST"])
@jwt_required()
def getOrders():

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admin only!"}), 403

    return getAllOrders()


@admin.route("/updateStatusOrder/<id>", methods = ["POST"])
@jwt_required()
def statusUpdate(id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admin only!"}), 403

    status = request.form.get("status")

    try:
        print("Updating status")
        return updateStatusOfOrder(id=id, newStatus=status)
    except Exception as e:
        return "Could not find the Order"

@admin.route("/getAllCustomersWithOrders", methods=["POST"])
@jwt_required()
def getAllCustomersWithOrders():

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admin only!"}), 403

    return getAllUserWithOrders()

@admin.route("/getAllCustomers")
@jwt_required()
def viewCustomers():
    
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admin only!"}), 403

    return getAllUser()
# @admin.route("")?