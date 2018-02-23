from flask import Blueprint, request, abort, jsonify, g
from app.models.user import User
from app import db, auth
import base64
from app.helpers.response import response_json

users_api = Blueprint('users', __name__, url_prefix='/api/users')

@users_api.route('/', methods=["GET"])
@auth.login_required
def get_users():
    users = User.query.all()
    return response_json([u.serialize for u in users], 200)

@users_api.route('/<int:id>', methods=["GET"])
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        return response_json({"message": "User not found"}, 404)
    return response_json(user.serialize, 200)


@users_api.route('/new', methods=['POST'])
def new_user():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        password = base64.b64decode(request.json.get('password'))
        if name is None or email is None or password is None or (password != base64.b64decode(request.json.get('password_confirmation'))):
            response_json({"error": "Bad params"}, 400)
        if User.query.filter_by(email=email).first() is not None:
            response_json({"error": "User exists"}, 400)
        user = User(email=email, name=name)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return response_json(user.serialize, 201)
    except Exception as ex:
        print(ex)
        return response_json({"error": "Exception occured"}, 500)

@users_api.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = base64.b64decode(request.json.get('password'))

        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            return response_json({"error": "Wrong email or password"}, status=400)
        
        g.user = user
        token = user.generate_token(60*60*24)
        return response_json({'token': token.decode('ascii'), 'duration': 600})
    except Exception as ex:
        return response_json({"error": "Bad params"}, status=400)

    
@auth.verify_token
def verify_password(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
