"""
Problem Domain

Design a User Service class that handles all the services related to platform users
"""

from datetime import datetime

from ...main import db
from ...main.model.user import User
from ...main.model.resource import CResource
from ...main.exceptions import UserAlreadyExists, UserNotFound

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

        return True
    else:
        raise UserAlreadyExists('Sorry! User Already Exists')


def delete_platform_user(user_id: int) -> bool:
    """
    :param user_id: input user id whose account has to be deleted from this platform
    :return bool:
    :purpose: Deletes the given user from this platform
    """
    db.session.delete(User.query.filter_by(user_id=user_id).one())
    # commit the change to the backend
    db.session.commit()

    return True


def get_all_platform_users():
    """
    :purpose:
    return all the platform users

    Note: only platform admin can access all platform users
    """
    return User.query.all()


def get_user_by_id(user_id: int) -> User:
    """
    :param user_id: input user id
    :return User:
    :purpose:
    for the given user_id return the User Object
    """
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        raise UserNotFound('Sorry User Does not exists!')
    else:
        return user


def get_user_by_email(user_email: str) -> User:
    """
    :param user_email: input user id
    :return User:
    :purpose:
    for the given user_email return the User Object
    """
    user = User.query.filter_by(email=user_email).first()

    if not user:
        raise UserNotFound('Sorry User Does not exists!')
    else:
        return user


def create_new_user_resource(user_id: int, req_data: dict):
    resource_name = req_data['resource_name']
    user = get_user_by_id(user_id)

    if user.check_quota_available():
        # user can create resource
        resource = CResource(
            resource_name=resource_name,
            user_id=user_id
        )

        commit_changes(resource)

        user.resources.append(resource)

        # decrease the quota remaining for this user by 1
        if user.user_quota_set():
            user.quota_remaining -= 1

        # commit the quota remaining to db
        commit_changes(user)
    else:
        # quota limit exceeded user cannot create resource
        raise ResourceLimitExceeded('Sorry! cannot create more resource '
                                    'quota limit exceeded please contact admin to increase quota')

    return resource.resource_id


def set_new_user_quota(user: User, new_user_quota: int) -> bool:
    """
    :param user: user object whose quota is to be updated
    :param new_user_quota: new quota
    :return:
    """
    user.user_quota = new_user_quota
    user.quota_remaining = new_user_quota

    db.session.commit()

    return True

