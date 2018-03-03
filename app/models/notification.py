from app import db
from app.models.base import Base
from app.helpers.response import json_date


class Notification(Base, db.Model):
    __tablename__ = 'notifications'
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(128), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'message': self.message,
            'status': self.status,
            'created_at': json_date(self.created_at)
        }