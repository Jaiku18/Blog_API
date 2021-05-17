from db import db


class UserModel(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    postId = db.Column(db.String(800))
    emailID = db.Column(db.String(80), unique=True)
    phoneNumber = db.Column(db.String(80), unique=True)

    def __init__(self, username, password, postId, emailID, phoneNumber):
        self.username = username
        self.password = password
        self.postId = postId
        self.emailID = emailID
        self.phoneNumber = phoneNumber

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_emailID(cls, emailID):
        return cls.query.filter_by(emailID=emailID).first()

    @classmethod
    def find_by_phoneNumber(cls, phoneNumber):
        return cls.query.filter_by(phoneNumber=phoneNumber).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()