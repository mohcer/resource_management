"""
Problem Domain

Design Resource Service class that handles all the user platform related services
"""

from datetime import datetime

from ...main import db
from ...main.model.resource import Resource


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def get_resource_by_id(resource_id: int) -> Resource:
    """
    :param resource_id: input resource id
    :return Resource:
    :purpose : fetches the resource from the backend for the given reource_id
    """
    return Resource.query.filter_by(resource_id=resource_id).first()


"""TODO only platform admin can access """


def get_all_platform_resources() -> list:
    """
    :purpose:
    returns all platform resources
    """
    return Resource.query.all()


def get_all_user_resources(user_id: int) -> list:
    """
    :param user_id: input user id
    :return list:
    :purpose:
    fetches and returns all the user resources
    """
    return Resource.query.filter_by(user_id=user_id).all()

