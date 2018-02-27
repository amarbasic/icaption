from app import db
from app.models.base import Base
from app.models.user import User
from app.helpers.response import json_date


class Album(Base, db.Model):
    __tablename__ = 'albums'
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='image', cascade="all,delete")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'number_of_images': len(self.images),
            'created_at': json_date(self.created_at),
            'modified_at': json_date(self.modified_at)
        }
