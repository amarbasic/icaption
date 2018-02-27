from app import db
from app.models.base import Base
from app.helpers.response import json_date


class Image(Base, db.Model):
    __tablename__ = 'images'
    name = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary(), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'album_id': self.album_id,
            'data': self.data.decode("utf-8") ,
            'created_at': json_date(self.created_at),
            'modified_at': json_date(self.modified_at)
        }
