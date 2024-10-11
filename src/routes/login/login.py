from flask import Blueprint
from flask import request
import jwt
import jsonify
from hashlib import sha256


from src.db.user_db import getCred, addNewUser
from datetime import datetime, timedelta

login_blue = Blueprint("login", __name__)


@login_blue.route("/login", methods = ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = getCred(username=username)

    if not user or user["password"] != sha256(password.encode("utf-8")).hexdigest():
        return "Incorrect Password", 401
    
    token = jwt.encode({
        "username": user['username'],
        "expiration": str(datetime.now() + timedelta(hours=72))
    }, "Temporary Secret")


    print(user['role'])

    return jsonify({"token" : token.decode("utf-8")})

@login_blue.route("/signUp", methods = ["POST"])
def signUp():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        user = addNewUser(username=username, password=password)
        print(user)
    except Exception as e:
        print(f"error {e}")
    # if not user or user["password"] != password:
        # return "Incorrect Password", 401
    
    return "Added New user", 200



