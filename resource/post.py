from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from model.postModel import postModel
from model.commentModule import CommentModel
from model.userModel import UserModel
from db import db
import base64
import os

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="Every post needs a title, cannot left blank."
                        )
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="Every post needs a content, cannot left blank."
                        )
    parser.add_argument('image',
                        type=str,
                        required=True,
                        help="Every post needs a image, cannot left blank."
                        )
    parser.add_argument('hashtag',
                        type=str,
                        required=True,
                        help="Every item needs a atleast one hashtag."
                        )

    @jwt_required()
    def get(self, name):
        item = postModel.find_by_title(name)
        if item:
            return item.json(), 201
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        data = Post.parser.parse_args()

        if postModel.find_by_title(data['title']):
            return {'message': "An item with name '{}' already exists.".format(data['title'])}, 400
        post = postModel(**data)

        try:
            if post.image:
                post.save_to_db()
                #post.image = os.getcwd() + "\images\\" + str(post.id) + ".png"
                #with open(os.getcwd() + "\images\\" + str(post.id) + ".png", "wb") as fh:
                    #fh.write(base64.decodebytes(data["image"].encode()))
                user = UserModel.find_by_id(post.user_id)
                post.save_to_db()
                user.postId = user.postId + str(post.id) + ","
                user.save_to_db()
                print(user.postId)
            return {"message": "post created successfully.", 'id': post.id}, 201
        except Exception as e:
            return {"message": "An error occurred inserting the item."+ str(e), }, 500

        return post.json(), 201

    @jwt_required()
    def delete(self, name):
        data = Post.parser.parse_args()
        post = postModel.find_by_title(data['title'])

        user = UserModel.find_by_id(post.user_id)

        userList = user.postId.split(',')
        userList = [x.strip() for x in userList]
        print(userList, post.id)
        userList.remove(str(post.id))
        strin = ', '.join(userList)
        print(strin)
        user.postId = strin
        user.save_to_db()
        print(user.postId)
        if post:
            comment = CommentModel.find_by_postID(post.id)
            post.delete_from_db()

            if comment:
                comment.delete_from_db()
            return {'message': 'post and Comment also  deleted.'}
        return {'message': 'post not found.'}, 404

    @jwt_required()
    def put(self, name):
        data = Post.parser.parse_args()

        if postModel.find_by_title(data['title']):
            post = postModel(**data)

        post.save_to_db()

        return post.json(), 201


class getPost(Resource):
    @jwt_required()
    def get(self, name):
        data = Post.parser.parse_args()
        post = postModel.find_by_title(name)
        if post:
            posti = postModel(**data)
            #comment = CommentModel.find_by_postID(posti.id)
            print(post.id)
            #userList = UserModel.query.join(postModel, UserModel.id == postModel.user_id).add_columns(postModel.id, UserModel.username, postModel.title, postModel.content, postModel.hashtag).filter(UserModel.id == post.user_id)
            userList = postModel.get(post.id, post.user_id)
            print(userList)
            post.username =userList[0][2]
            print(post.username)

            return {'item' :post.json()}, 201
            #return {'item': post.json(), 'comment': list(map(lambda x: x.json(), CommentModel.query.filter_by(post_id= post.id).all())) }
        return {'message': 'Item not found'}, 404

class PostList(Resource):

    def get(self):
        return {'post': list(map(lambda x: x.json(), postModel.query.all()))}