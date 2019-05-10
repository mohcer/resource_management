"""
Problem Domain

Design a User Service class that handles all the services related to platform users
"""

from datetime import datetime

from ...main import db
from ...main.model.user import User
from ...main.model.resource import Resource
from ...main.exceptions import UserAlreadyExists

from .resource_service import create_new_resource
from ...main.exceptions import ResourceLimitExceeded


def commit_changes(data):
    db.session.add(data)
    db.session.commit()


def create_new_user(data: dict) -> bool:
    """
    :param data: input user parameters
    :return bool:
    :purpose: create and saves a new user in db
    """
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        new_user = User(
            email=data['email'],
            password=data['password'],
            user_registered_on=datetime.utcnow()
        )

        commit_changes(new_user)

        return new_user.user_id
    else:
        raise UserAlreadyExists('Sorry! User Already Exists')


"""TODO admin access required"""


def get_all_platform_users():
    """
    :purpose:
    return all the platform users
    """
    return User.query.all()


def get_user_by_id(user_id: int) -> User:
    """
    :param user_id: input user id
    :return User:
    :purpose:
    for the given user_id return the User Object
    """
    return User.query.filter_by(user_id=user_id).first()


"""TODO admin previlage required """


def set_user_quota(user_id: int, quota: int):
    """
    :param user_id: input user_id
    :param quota: input quota value
    :return bool:
    :purpose: sets new quota for the given user id
    """
    user = get_user_by_id(user_id)

    user.user_quota = quota


def create_new_user_resource(user_id: int, resource_name: str) -> bool:
    user = get_user_by_id(user_id)

    if user.check_quota_available():
        # user can create resource
        resource = Resource(
            resource_name=resource_name,
            user_id=user_id
        )

        commit_changes(resource)

        user.resources.append(resource)

        #commit_changes(user)
    else:
        # quota limit exceeded user cannot create resource
        raise ResourceLimitExceeded('Sorry! cannot create more resource '
                                    'quota limit exceeded please contact admin to increase quota')

    return resource.resource_id
