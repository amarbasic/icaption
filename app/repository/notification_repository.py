from app.models.notification import Notification
from app import db
from flask import g

def insert_notification(message, status):
    notification = Notification(message=message, status=status)
    db.session.add(notification)
    db.session.commit()
    return notification.serialize