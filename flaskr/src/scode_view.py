from flask import Blueprint, request

scode = Blueprint("scode", __name__, url_prefix="/scode")

@scode.route("/hello")
def getHello():
    return "Hello"