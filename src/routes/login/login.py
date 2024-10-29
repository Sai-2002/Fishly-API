from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
# import jsonify
import json
from hashlib import sha256

from src.db.user_db import getCred, addNewUser

login_blue = Blueprint("login", __name__)


# @login_blue.route("/check")
# @jwt_required()
# def check():

#     claims = get_jwt()
#     if claims['role'] != 'admin':
#         return jsonify({"msg": "Access forbidden: Admins only!"}), 403

#     return "Working"


# @login_blue.route('/authcheck')
# @jwt_required()
# def d():
#     claims = get_jwt()
#     if claims['role'] != 'customer':
#         return jsonify({"msg": "Access forbidden: Admins only!"}), 403
#     return "Good"

@login_blue.route("/login", methods = ["POST"])
def login():
    mobileNumber = request.form.get("mobile")
    password = request.form.get("password")

    user = getCred(mobileNumber)

    if not user or user["password"] != sha256(password.encode("utf-8")).hexdigest():
        return "Incorrect Password", 401
    
    user_role = user['role']

    access_token = create_access_token(identity=mobileNumber, additional_claims={"role": user_role})
    
    return json.dumps(access_token), 200


@login_blue.route("/signUp", methods = ["POST"])
def signUp():
    username = request.form.get("username")
    password = request.form.get("password")
    mobileNumber = request.form.get("mobile")

    try:
        user = addNewUser(username=username, password=password, mobileNumber=mobileNumber)
        print(user)
    except Exception as e:
        print(f"error {e}")
    # if not user or user["password"] != password:
        # return "Incorrect Password", 401
    
    return "Added New user", 200



