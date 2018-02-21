from flask import Blueprint, request, abort, jsonify, g
from app.models.album import Album
from app import db, auth
import base64
from app.helpers.response import response_json
from app.repository import albums_repository

albums_api = Blueprint('albums', __name__, url_prefix='/api/albums')


@albums_api.route('/', methods=["GET"])
@auth.login_required
def get_albums_for_logged_user():
    albums = albums_repository.get_albums(g.user)
    return response_json(albums, 200)

@albums_api.route('/<int:id>', methods=["GET"])
@auth.login_required
def get_images_for_logged_album(id):
    images = albums_repository.get_album_images(id)
    return response_json(images, 200)

@albums_api.route('/new', methods=["POST"])
@auth.login_required
def new_album():
    try:
        name = request.json.get('name')
        album = albums_repository.insert_album(name)
        return response_json(album, 201)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Bad params"}, 400)

