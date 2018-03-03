from app.models.image import Image
from app import db
from flask import g

def get_image_by_id(image_id):
    return Image.query.get(image_id)


def update_image_caption(image_id, caption):
    image = Image.query.get(image_id)
    image.caption = caption
    db.session.commit()