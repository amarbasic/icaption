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
    try:
        albums = albums_repository.get_albums(g.user)
        return response_json(albums, 200)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Exception occured"}, 500)

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

@albums_api.route('/<int:id>/new', methods=["POST"])
@auth.login_required
def new_image(id):
    try:
        images = albums_repository.insert_album_images(id, request.json['images'])
        return response_json(images, status=200)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Bad params"}, 400)

@albums_api.route('/<int:id>', methods=["DELETE"])
@auth.login_required
def delete_album(id):
    try:
        albums_repository.delete_album(id)
        return response_json({"message": "Album deleted" }, status=200)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Bad params"}, 400)


@albums_api.route('/images/<int:id>', methods=["DELETE"])
@auth.login_required
def delete_image(id):
    try:
        albums_repository.delete_image(id)
        return response_json({"message": "Image deleted" }, status=200)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Bad params"}, 400)

