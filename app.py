from flask import Flask
from flask_restful import Api
from resource.user import UserRegister, UserLogin, UserConfirm, UserList, UserRefresh
from resource.post import Post, getPost,  getallPost
from resource.comment import Comment,  getComment
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'jai'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(UserRefresh, "/refresh")
api.add_resource(UserList, "/getAllUsers")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

api.add_resource(Post, '/addPost/<string:name>')
api.add_resource(getallPost, "/getAllPost")
api.add_resource(getPost, '/getPost/<string:name>')


api.add_resource(getComment, '/getPostComment/<string:name>')
api.add_resource(Comment, '/addComment')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)