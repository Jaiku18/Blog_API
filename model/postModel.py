from db import db
from model.userModel import UserModel

class postModel(db.Model):
    __tablename__ = 'post_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    content = db.Column(db.String(800))
    image = db.Column(db.String(800))
    hashtag = db.Column(db.String(80))

    user = db.relationship('UserModel')

    def __init__(self, user_id, title, content,image, hashtag):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.image = image
        self.hashtag = hashtag
        self.username = ''

    def json(self):
        return {'id': self.id, 'user_id': self.user_id, 'title': self.title, 'content': self.content, 'image': self.image, 'hashtag': self.hashtag, 'username': self.username}

    @classmethod
    def find_by_title(cls, title):

        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get(cls, post_id, post_userID):
        return UserModel.query.filter(postModel.id ==post_id and postModel.user_id == post_userID ).join(postModel, UserModel.id == postModel.user_id).add_columns(postModel.id,
                                                                                                  UserModel.username,
                                                                                                  postModel.title,
                                                                                                  postModel.content,
                                                                                                  postModel.image,
                                                                                                  postModel.hashtag).all()

