from db import  db
from model.userModel import UserModel

class CommentModel(db.Model):
    __tablename__ = 'comment_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post_table.id'))
    comment = db.Column(db.String(800))

    post = db.relationship('postModel')
    user = db.relationship('UserModel')

    def __init__(self, user_id, post_id, comment):
        self.user_id = user_id
        self.post_id = post_id
        self.comment = comment
        self.username = ''


    def json(self):
        return {'user_id': self.user_id, 'post_id': self.post_id, 'comment': self.comment, 'username': self.username}

    @classmethod
    def find_by_comment(cls, comment):
        return cls.query.filter_by(comment=comment)

    @classmethod
    def find_by_postID(cls, post_id):
        return cls.query.filter_by(post_id= post_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getComment(cls, post_id, post_userID):
        return UserModel.query.filter(CommentModel.post_id == post_id and UserModel.user_id == post_userID).join(CommentModel,
                                                                                                         UserModel.id == CommentModel.user_id).add_columns(
            CommentModel.id,
            UserModel.username,
            CommentModel.comment
            ).all()