"""
Problem Domain:

Token Garbage represents a store to dump the used auth token
"""
from .. import db


class TokenGarbage(db.Model):
    """Represents store to dump used auth tokens"""

    __tablename__ = "tokengarbage"
    token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    dumped_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, token, dumped_on=None):
        """
        :param token: auth_token that is to be dumped
        :returns None:
        """
        self.token = token
        self.dumped_on = dumped_on

    def __repr__(self):
        """
        :param None:
        :return String:
        purpose:
        returns a String representation of the BlackListedToken class
        """
        return "<id token: {}".format(self.token)

    @staticmethod
    def is_dumped(auth_token):
        """
        :param auth_token: input auth_token to check
        :return Booleans:
        purpose:
        checks if the given auth_token is blacklisted_token returns True if blacklisted, False otherwise
        """
        res = TokenGarbage.query.filter_by(token=auth_token).first()

        return True if res else False
