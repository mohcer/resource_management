"""
Problem Domain

Design a User model that represents the chainstack_platform users
"""
from ...main.exceptions import ResourceLimitExceeded
from .. import db, flask_bcrypt
from .resource import Resource


class User(db.Model):
    """User Model represents chainstack_platform users"""
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    platform_admin = db.Column(db.Boolean, nullable=False, default=False)
    user_registered_on = db.Column(db.DateTime, nullable=False)
    user_quota = db.Column(db.Integer, nullable=False, default=-1)

    resources = db.relationship('Resource', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('sorry password id write only ')

    @password.setter
    def password(self, password: str):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str):
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    def check_quota_available(self):
        """
        :purpose: check if user quota is available to create more resources
        """
        current_user_resource_count = len(self.resources)

        def user_quota_set():
            return self.user_quota != -1

        quota_set = user_quota_set()

        status = True if not quota_set or current_user_resource_count < self.user_quota else False

        return status

    def __repr__(self):
        return "<User '{}'>".format(self.username)