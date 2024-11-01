from flask import Blueprint, request, jsonify

from src.db.user_db import updateAddress, getAddr

user = Blueprint("user",__name__)

@user.route("/updateAddress/<id>/", methods = ["POST"])
def addAddress(id):

    response = request.get_json()

    address = response["address"]

    return jsonify({
        "Result": updateAddress(id=id, address=address)
    })


@user.route("/getAddress/<id>", methods = ["GET"])
def getAddress(id):

    return jsonify({
        "Address": getAddr(id)} 
    )