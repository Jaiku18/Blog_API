from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from model.commentModule import CommentModel
from model.postModel import postModel
from model.userModel import UserModel


class Comment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('post_id',
                        type=int,
                        required=True,
                        help="Every post needs a title, cannot left blank."
                        )
    parser.add_argument('comment',
                        type=str,
                        required=True,
                        help="Every post needs a content, cannot left blank."
                        )

    @jwt_required()
    def post(self):
        data = Comment.parser.parse_args()
        # if CommentModel.find_by_title(data['title']):
        #     return {'message': "An item with name '{}' already exists.".format(data['title'])}, 400
        comment = CommentModel(**data)

        try:
            comment.save_to_db()
            return {"message": "comment created successfully.", 'id': comment.id}, 201

        except:
            return {"message": "An error occurred inserting the comment."}, 500

        return comment.json(), 201

    @jwt_required()
    def delete(self):
        data = Comment.parser.parse_args()
        comment = CommentModel.find_by_comment(data['comment'])
        if comment:
            comment.delete_from_db()
            return {'message': 'comment deleted.'}, 201
        return {'message': 'comment not found.'}, 404


class getComment(Resource):
    @jwt_required()
    def get(self, name):
        post = postModel.find_by_id(name)
        comment = CommentModel.query.filter_by(post_id=name).all()

        lis = []
        if comment:
            for i in comment:
                print(i.user_id)
                i.username = ''
                user = UserModel.find_by_id(i.user_id)
                i.username = user.username
                lis.append(i.json())
            return {'comment': lis}
        return {"message" : "No Comment Found for the requested post"}, 404


