"""
Problem Domain

Design a Resource model class that represents chainstack_platform Resources
"""

from .. import db


class CResource(db.Model):
    """represents chainstack_platform resource"""

    __tablename__ = "resource"

    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_name = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
