from flask import Blueprint, request, abort, jsonify, g
from app.models.album import Album
from app import db, auth
import base64
from app.helpers.response import response_json
from app.repository import albums_repository

dashboard_api = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_api.route('/', methods=["GET"])
@auth.login_required
def get_dashboard():
    try:
        result = {
            "galleries": albums_repository.get_number_of_albums(),
            "images": albums_repository.get_number_of_images(),
            "runs": albums_repository.get_number_of_runs(),
            "notifications": albums_repository.get_notifications()
        }

        return response_json(result, 200)
    except Exception as ex:
        print(ex)
        return response_json("Exception occured", 500)
