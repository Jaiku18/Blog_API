from werkzeug.security import safe_str_cmp
from model.userModel import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token
               },
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)