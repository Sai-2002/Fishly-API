from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

@admin.route("/getNotification", methods=["POST"])
def getNotification():

    data = request.get_json()

    sender_email = "rajkumar210303@gmail.com"
    receiver_email = "rajkumar210303@gmail.com"
    password = "gtra wvat gigh enco"

    subject = data["SUBJECT"]
    body = data["BODY"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
    # Connect to the SMTP server (Gmail example)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Login to the email account
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
            return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"