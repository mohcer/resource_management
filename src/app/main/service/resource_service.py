"""
Problem Domain

Design Resource Service class that handles all the user platform related services
"""

from datetime import datetime

from app.main import db
from app.main.model.resource import Resource


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def create_new_resource(resource_name: str) -> Resource:
    """
    :param user_id: id of the user to whom this resource belongs to
    :param resource_name: input new resource name
    :return bool:
    :purpose:
    creates and saves a new resource in the backend db
    """
    resource = Resource(
        resource_name=resource_name
    )

    commit_changes(resource)

    return resource
