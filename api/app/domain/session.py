from app import auth
from app.models.user import User

@auth.verify_token
def verify_password(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    return True
