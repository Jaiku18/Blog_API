from flask_restful import Resource, reqparse
from model.userModel import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import safe_str_cmp
import os

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('emailID',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('phoneNumber',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.find_by_emailID(data['emailID']):
            return {"message": "A user with that emailID already exists"}, 400

        if UserModel.find_by_phoneNumber(data['phoneNumber']):
            return {"message": "A user with that phoneNumber already exists"}, 400

        user = UserModel(data['username'], data['password'], '', data['emailID'], data['phoneNumber'])
        user.save_to_db()
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {"message": "User created successfully.", 'id': user.id,'access_token': access_token,
                   'refresh_token': refresh_token }, 201

class UserLogin(Resource):
    parsers = reqparse.RequestParser()
    parsers.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parsers.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserLogin.parsers.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            print(os.getcwd())
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   },


    def identity(payload):
        user_id = payload['identity']
        return UserModel.find_by_id(user_id)