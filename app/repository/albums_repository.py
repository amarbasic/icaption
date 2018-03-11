from app.models.album import Album
from app.models.user import User
from app.models.image import Image
from app.models.notification import Notification
from app.models.captions import Captions
import nltk

nltk.download('all')

from sqlalchemy import or_

from app import db
from flask import g
import random
from sqlalchemy import desc


def get_albums(user):
    albums = Album.query.filter_by(user_id=user.id)
    result = []
    for album in albums:
        preview = random.choice(album.images) if len(album.images) > 0 else None
        album = album.serialize
        album['preview'] = preview.serialize if preview else { "data": "http://placehold.it/400x300" }
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

    album =  album.serialize
    album['preview'] = { "data": "http://placehold.it/400x300" }
    return album


def get_album_images(album_id):
    album = Album.query.get(album_id)
    result = []
    for image in album.images:
        result.append(image.serialize)
    return {
        'name': album.name,
        'images': result
    }

def insert_album_images(album_id, images):
    result = []
    for image in images:
        data = bytes(image, "ascii")
        entity = Image(data=data, album_id=album_id, name="No name")
        db.session.add(entity)
        db.session.commit()
        result.append(entity.serialize)
    return result

def delete_album(album_id):
    db.session.delete(Album.query.get(album_id))
    db.session.commit()

def delete_image(image_id):
    db.session.delete(Image.query.get(image_id))
    db.session.commit()


def get_number_of_albums():
    return len(Album.query.all())

def get_number_of_images():
    return sum([len(album.images) for album in Album.query.all()])

def get_number_of_runs():
    runs = Notification.query.filter(Notification.status == "In progress").count() - Notification.query.filter(or_(Notification.status == "Done", Notification.status == "Error")).count()
    return runs

def get_notifications():
    result = []
    for notification in Notification.query.order_by(desc(Notification.created_at)).all():
        result.append(notification.serialize)
    return result

def get_pos_for_captions(captions, image_id):
    tokenized = nltk.word_tokenize(captions)
    for (word, pos_t) in nltk.pos_tag(tokenized):
        print(word, pos_t)
        entity = Captions(pos=word, pos_type=pos_t, image_id=image_id)
        db.session.add(entity)
    
    db.session.commit()