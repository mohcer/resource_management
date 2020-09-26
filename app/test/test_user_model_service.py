"""
Problem Domain

Write sufficient test cases to test User model
"""

import unittest
import datetime
import uuid

from app.main import db
from app.main.model.user import User
from app.main.model.resource import CResource
from app.test.base import BaseTestCase
from app.main.service.user_service import (
    create_new_user,
    get_user_by_id,
    create_new_user_resource,
    set_new_user_quota,
)
from app.main.service.resource_service import (
    get_resource_by_id,
    get_user_resources,
    delete_user_resource,
)

from app.main.exceptions import UserAlreadyExists, ResourceLimitExceeded


class TestUserModel(BaseTestCase):
    def test_user_creation(self):

        data = dict()
        data["email"] = "test@gmail.com"
        data["password"] = "test123"

        new_user_id = create_new_user(data)

        user = get_user_by_id(new_user_id)
        # Test user created successfully
        self.assertTrue(user.email == "test@gmail.com")

    def test_duplicate_user_creation(self):
        try:
            data1 = dict()
            data2 = dict()

            data1["email"] = "test@gmail.com"
            data1["password"] = "test123"

            data2["email"] = "test@gmail.com"
            data2["password"] = "test123"

            new_user_1 = create_new_user(data1)

            new_user_2 = create_new_user(data2)

        except Exception as e:
            self.assertTrue(isinstance(e, UserAlreadyExists))
        else:
            self.assertTrue(new_user_1 != new_user_2)

    def test_default_user_quota(self):
        data = dict()
        data["email"] = "test@gmail.com"
        data["password"] = "test123"

        new_user_id = create_new_user(data)

        new_user = get_user_by_id(new_user_id)
        # Test by default new user can create as many resource as required

        self.assertTrue(new_user.user_quota == -1)

    def test_restrict_rescource_creation(self):
        data = dict()
        data["email"] = "test@gmail.com"
        data["password"] = "test123"

        new_user_id = create_new_user(data)

        user = get_user_by_id(new_user_id)

        set_new_user_quota(user, 1)

        try:
            resource_id_1 = create_new_user_resource(
                user.user_id, {"resource_name": "test_resource1"}
            )

            resource_id_2 = create_new_user_resource(
                user.user_id, {"resource_name": "test_resource2"}
            )

        except Exception as e:
            self.assertTrue(isinstance(e, ResourceLimitExceeded))

            # check if the first resource created is available
            user_resources = get_user_resources(new_user_id)

            self.assertTrue(len(user_resources) == 1)
        else:
            # else check the created resource is available
            resource_1 = get_resource_by_id(resource_id_1)
            resource_2 = get_resource_by_id(resource_id_2)

            self.assertTrue(resource_1.user_id == user.user_id)
            self.assertTrue(resource_2.user_id == user.user_id)

    def test_quota_increase_on_resource_delete(self):
        data = dict()
        data["email"] = "test@gmail.com"
        data["password"] = "test123"

        new_user_id = create_new_user(data)

        user = get_user_by_id(new_user_id)

        set_new_user_quota(user, 3)

        resource_id_1 = create_new_user_resource(
            user.user_id, {"resource_name": "test_resource1"}
        )

        resource_id_2 = create_new_user_resource(
            user.user_id, {"resource_name": "test_resource2"}
        )

        self.assertTrue(user.quota_remaining == 1)

        delete_user_resource(user, resource_id_1)

        self.assertTrue(user.quota_remaining == 2)

        # delete all resources of user and check user quota reset to original count
        delete_user_resource(user)

        self.assertTrue(user.quota_remaining == 3)
