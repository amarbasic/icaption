from flask import Blueprint, request, abort, jsonify, g
from app.models.image import Image
from app import db, auth
from app.helpers.response import response_json

images_api = Blueprint('images', __name__, url_prefix='/api/images')

@images_api.route('/', methods=["GET"])
@auth.login_required
def get_images():
    users = Image.query.all()
    return response_json([u.serialize for u in users], 200)