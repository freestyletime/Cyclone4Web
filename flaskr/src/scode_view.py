from flask import Blueprint, request, render_template, jsonify

scode = Blueprint("scode", __name__, url_prefix="/scode")
