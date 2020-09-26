"""
Problem Domain

Design Resource Service class that handles all the user platform related services
"""

from datetime import datetime

from ...main import db
from ...main.model.resource import CResource
from ..model.user import User


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def get_resource_by_id(resource_id: int) -> CResource:
    """
    :param resource_id: input resource id
    :return Resource:
    :purpose : fetches the resource from the backend for the given reource_id
    """
    return CResource.query.filter_by(resource_id=resource_id).first()


"""TODO only platform admin can access """


def get_all_platform_resources() -> list:
    """
    :purpose:
    returns all platform resources
    """
    return CResource.query.all()


def get_user_resources(user_id: int, resource_id: int = None) -> list:
    """
    :param user_id: input user id
    :param resource_id: optional resource id
    :return list:
    :purpose:
    fetches and returns all the user resources if resource_id is present then just return that user resource
    """
    if resource_id:
        res = CResource.query.filter_by(
            user_id=user_id, resource_id=resource_id
        ).first()
    else:
        res = CResource.query.filter_by(user_id=user_id).all()

    return res


def delete_user_resource(user: User, resource_id: int = None) -> bool:
    """
    :param user: user object
    :param resource_id: input resource id
    :return bool:
    :purpose: deletes a particular user resource from the platform
    """

    if resource_id is None:
        db.session.query(CResource).filter(CResource.user_id == user.user_id).delete()

        # increment the user remaining quota by available user quota
        user.quota_remaining = user.user_quota
    else:
        db.session.delete(
            CResource.query.filter_by(
                user_id=user.user_id, resource_id=resource_id
            ).one()
        )

        # increment the user remaining quota by one
        user.quota_remaining += 1

    # commit the change to the backend
    db.session.commit()

    return True
