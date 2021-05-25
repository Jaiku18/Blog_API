from flask import Flask, jsonify
from flask_restful import Api
from resource.user import UserRegister, UserLogin, UserConfirm
from resource.post import Post, getPost
from resource.comment import Comment, CommentList, getComment
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
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

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

jwt = JWTManager(app)

api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(Post, '/addPost/<string:name>')
api.add_resource(Comment, '/addComment')
api.add_resource(getPost, '/getPost/<string:name>')
api.add_resource(CommentList, '/getComment/<string:name>')
api.add_resource(getComment, '/getPostComment/<string:name>')
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)