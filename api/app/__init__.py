import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

auth = HTTPTokenAuth()

from app.controllers.users_controllers import users_bp
app.register_blueprint(users_bp)

db.create_all()
