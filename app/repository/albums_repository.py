from app.models.album import Album
from app.models.user import User
from app import db
from flask import g
import random


def get_albums(user):
    albums = Album.query.filter_by(user_id=user.id)
    result = []
    for album in albums:
        preview = random.choice(album.images) if len(album.images) > 0 else None
        album = album.serialize
        album['preview'] = preview.serialize if preview else None
        result.append(album)
    return result

def get_albums_users():
    albums = Album.query.all()
    result = []
    for album in albums:
        user = User.query.get(album.user_id)
        album = album.serialize
        album['user'] = user.serialize
        del album['user_id']
        result.append(album)
    return result

def insert_album(name):
    album = Album(name=name, user_id=g.user.id)
    db.session.add(album)
    db.session.commit()
    return album.serialize

def get_album_images(album_id):
    album = Album.query.get(album_id)
    result = []
    for image in album.images:
        result.append(image.serialize)
    return result