from db import db
from flask import request, url_for
from requests import post, Response


MAILGUN_DOMAIN = 'sandbox0aa56920053f483099ad264d89585cb9.mailgun.org'
MAILGUN_API_KEY = 'bcd1b6a684669f42420ffda38edbb7bb-6ae2ecad-04580d93'
FROM_TITLE = 'From BLog API'
FROM_EMAIL = 'postmaster@sandbox0aa56920053f483099ad264d89585cb9.mailgun.org'


class UserModel(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    postId = db.Column(db.String(800))
    emailID = db.Column(db.String(80), unique=True)
    phoneNumber = db.Column(db.String(80), unique=True)
    isActive = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, postId, emailID, phoneNumber):
        self.username = username
        self.password = password
        self.postId = postId
        self.emailID = emailID
        self.phoneNumber = phoneNumber
        self.isActive = False

    def json(self):
        return {'username': self.username, 'postId' : self.postId, 'emailID': self.emailID, 'phoneNumber': self.phoneNumber, 'IsActive': self.isActive}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all_username(cls):
        return cls.query.all()

    @classmethod
    def find_by_emailID(cls, emailID):
        return cls.query.filter_by(emailID=emailID).first()

    @classmethod
    def find_by_phoneNumber(cls, phoneNumber):
        return cls.query.filter_by(phoneNumber=phoneNumber).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:

        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.emailID,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm your registration: {link}",
            },
        )

