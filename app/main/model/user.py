"""
Problem Domain

Design a User model that represents the chainstack_platform users
"""
import datetime
import jwt
import flask_bcrypt
from ..model.token_garbage import TokenGarbage
from .. import db, flask_bcrypt
from ..config import key


class User(db.Model):
    """User Model represents chainstack_platform users"""
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    platform_admin = db.Column(db.Boolean, nullable=False, default=False)
    user_registered_on = db.Column(db.DateTime, nullable=False)
    user_quota = db.Column(db.Integer, nullable=False, default=-1)
    quota_remaining = db.Column(db.Integer, nullable=False, default=-1)
    resources = db.relationship('CResource', backref="user", cascade="all, delete-orphan", lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('sorry password id write only ')

    @password.setter
    def password(self, password: str):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def user_quota_set(self):
        """
        :purpose: checks if the user quota is set or not
        """
        return self.user_quota >= 0

    def check_quota_available(self):
        """
        :purpose: check if user quota is available to create more resources
        """
        quota_set = self.user_quota_set()

        if not quota_set or (quota_set and self.quota_remaining <= self.user_quota and self.quota_remaining > 0):
            status = True
        else:
            status = False

        return status

    @staticmethod
    def encode_auth_token(user_id):
        """
        :param user_id: user id of the user
        :returns String: String encoded auth token
        :raise Exception: if unable to encode auth_token
        purpose: Generates the auth token for the given user_id along with other information
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': str(user_id)
            }

            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            raise e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        :param auth_token:
        :returns String: decoded auth token
        :raises:
        ExpiredSignatureError: If the signature has expired
        InvalidTokenError: If the token has expired
        purpose: Decodes the given auth token and returns the string payload value, raises Exception otherwise
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_token_dumped = TokenGarbage.is_dumped(auth_token)

            if is_token_dumped:
                raise jwt.InvalidTokenError('Received Invalid Token login again')
            else:
                return payload['sub']

        except jwt.ExpiredSignatureError as e:
            raise e
        except jwt.InvalidTokenError as e:
            raise e

    def __repr__(self):
        return "<User '{}'>".format(self.email)