from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import json


from src.db.products_db import insertProduct, updateProductById, deleteProduct
from src.db.orders_db import getAllOrders

admin = Blueprint("admin", __name__)

@admin.route("/addProduct", methods = ["POST"])
@jwt_required()
def addProduct():

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admins only!"}), 403

    if 'image' not in request.files and 'image1' not in request.files and 'image2' not in request.files:
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
    image1 = request.files["image1"]
    image2 = request.files["image2"]

    
    try:
        return insertProduct(product=product, image=image, image1=image1, image2=image2)
    
    except Exception as e:
        print(e)

@admin.route("/updateProduct/<id>", methods = ["POST"])
@jwt_required()
def updateProduct(id):

    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Access forbidden: Admins only!"}), 403

    if 'image' not in request.files and 'image1' not in request.files and 'image2' not in request.files:
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
    image2 = request.files["image1"]
    image1 = request.files["image2"]

    try:
        return updateProductById(id, product, image, image1, image2)
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

@admin.route("/viewCustomers")
def viewCustomers():
    pass

# @admin.route("")?