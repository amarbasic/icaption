import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object('config')

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
db.init_app(app)

auth = HTTPTokenAuth()

from app.controllers.users_controllers import users_api
from app.controllers.albums_controllers import albums_api
from app.controllers.images_controllers import images_api
app.register_blueprint(users_api)
app.register_blueprint(albums_api)
app.register_blueprint(images_api)

db.create_all()
