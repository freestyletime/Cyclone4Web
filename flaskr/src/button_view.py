from flask import Blueprint, request

button = Blueprint("button", __name__, url_prefix="/button")

@button.route("/hello")
def getHello():
    return "Hello"