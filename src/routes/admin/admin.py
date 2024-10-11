from flask import Blueprint, request
import json


from src.db.products_db import insertProduct, updateProductById, deleteProduct

admin = Blueprint("admin", __name__)

@admin.route("/addProduct", methods = ["POST"])
def addProduct():

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
    }

    image = request.files['image']

    try:
        return insertProduct(product=product, image=image)
    except Exception as e:
        print(e)

@admin.route("/updateProduct/<id>", methods = ["POST"])
def updateProduct(id):

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
    }

    image = request.files["image"]

    try:
        return updateProductById(id, product, image)
    except Exception as e:
        print(e)

@admin.route("/deleteProduct/<id>")
def deleteProductById(id):
      return deleteProduct(id)

@admin.route("/viewCustomers")
def viewCustomers():
    pass

# @admin.route("")?