from app import db
from app.models.base import Base
from app.helpers.response import json_date


class Captions(Base, db.Model):
    __tablename__ = 'captions'
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    pos = db.Column(db.String(128))
    pos_type = db.Column(db.String(128))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'image_id': self.image_id,
            'pos': self.pos,
            'pos_type': self.pos_type,
            'created_at': json_date(self.created_at),
            'modified_at': json_date(self.modified_at)
        }