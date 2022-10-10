from flask import Blueprint, request

editor = Blueprint("editor", __name__, url_prefix="/editor")

@editor.route("/hello")
def getHello():
    return "Hello"