from flask import Blueprint, request, abort, jsonify, g
from app.models.album import Album
from app import db, auth
import base64
from app.helpers.response import response_json
from app.repository import albums_repository, notification_repository
from app.algorithm.predict import CaptionGenerator

albums_api = Blueprint('albums', __name__, url_prefix='/api/albums')


@albums_api.route('/', methods=["GET"])
@auth.login_required
def get_albums_for_logged_user():
    try:
        albums = albums_repository.get_albums(g.user)
        return response_json(albums, 200)
    except Exception as ex:
        print(ex)
        return response_json("Exception occured", 500)

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
        return response_json("Bad params", 400)

@albums_api.route('/<int:id>/new', methods=["POST"])
@auth.login_required
def new_image(id):
    try:
        images = albums_repository.insert_album_images(id, request.json['images'])
        return response_json(images, status=200)
    except Exception as ex:
        print(ex)
        return response_json("Bad params", 400)

@albums_api.route('/<int:id>', methods=["DELETE"])
@auth.login_required
def delete_album(id):
    try:
        albums_repository.delete_album(id)
        return response_json({"message": "Album deleted" }, status=200)
    except Exception as ex:
        print(ex)
        return response_json("Bad params", 400)


@albums_api.route('/images/<int:id>', methods=["DELETE"])
@auth.login_required
def delete_image(id):
    try:
        albums_repository.delete_image(id)
        return response_json({"message": "Image deleted" }, status=200)
    except Exception as ex:
        print(ex)
        return response_json("Bad params", 400)


from multiprocessing import Process

def process_captions(album_id):
    try:
        notification_repository.insert_notification("Algorithm started with album {}".format(album_id), "In progress")
        result = {}
        images = albums_repository.get_album_images(album_id)['images']
        for image in images:
            image_id = image['id']
            caption = CaptionGenerator.Instance().generate_caption(image_id)
            result[str(image_id)] = caption
        notification_repository.insert_notification("Algorithm done with album {}".format(album_id), "Done")
    except Exception as ex:
        notification_repository.insert_notification("Algorithm erros with album {}. {}".format(album_id, ex), "Error")

@albums_api.route('/algorithm/<int:id>', methods=["GET"])
@auth.login_required
def algorithm_album(id):
    try:
        p = Process(target=process_captions, args=(id,))
        p.start()
        return response_json({"message": "Processing started"}, status=200)
    except Exception as ex:
        print(ex)
        return response_json("Bad params", 400)


def process_caption_image(image_id):
    try:
        notification_repository.insert_notification("Algorithm started with image {}".format(image_id), "In progress")
        CaptionGenerator.Instance().generate_caption(image_id)
        notification_repository.insert_notification("Algorithm done with image {}".format(image_id), "Done")
    except Exception as ex:
        notification_repository.insert_notification("Algorithm error with image {}. {}".format(image_id, ex), "Error")

@albums_api.route('/algorithm/image/<int:id>', methods=["GET"])
@auth.login_required
def algorithm_image(id):
    try:
        p = Process(target=process_caption_image, args=(id,))
        p.start()
        return response_json({"message": "Processing started"}, status=200)
    except Exception as ex:
        print(ex)
        return response_json("Bad params", 400)