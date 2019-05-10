"""
Problem Domain

Write sufficient test cases to test User model
"""

import unittest
import datetime
import uuid

from app.main import db
from app.main.model.user import User
from app.main.model.resource import Resource
from app.test.base import BaseTestCase
from app.main.service.user_service import create_new_user, get_user_by_id, create_new_user_resource
from app.main.service.resource_service import create_new_resource, get_resource_by_id
from app.main.exceptions import UserAlreadyExists, ResourceLimitExceeded


class TestUserModel(BaseTestCase):
    def test_user_creation(self):

        data = dict()
        data['email'] = 'test@gmail.com'
        data['password'] = 'test123'

        new_user_id = create_new_user(data)

        user = get_user_by_id(new_user_id)
        # Test user created successfully
        self.assertTrue(user.email == 'test@gmail.com')

    def test_duplicate_user_creation(self):
        try:
            data1 = dict()
            data2 = dict()

            data1['email'] = 'test@gmail.com'
            data1['password'] = 'test123'

            data2['email'] = 'test@gmail.com'
            data2['password'] = 'test123'

            new_user_1 = create_new_user(data1)

            new_user_2 = create_new_user(data2)

        except Exception as e:
            self.assertTrue(isinstance(e, UserAlreadyExists))
        else:
            self.assertTrue(new_user_1 != new_user_2)

    def test_default_user_quota(self):
        data = dict()
        data['email'] = 'test@gmail.com'
        data['password'] = 'test123'

        new_user_id = create_new_user(data)

        new_user = get_user_by_id(new_user_id)
        # Test by default new user can create as many resource as required

        self.assertTrue(new_user.user_quota == -1)

    def test_restrict_rescource_creation(self):
        data = dict()
        data['email'] = 'test@gmail.com'
        data['password'] = 'test123'

        new_user_id = create_new_user(data)

        user = get_user_by_id(new_user_id)

        user.quota = 1

        try:
            resource_id_1 = create_new_user_resource(user.user_id, "test_resource1")

            #resource_id_2 = create_new_user_resource(user.user_id, "test_resource2")

        except Exception as e:
            print('e')
            self.assertTrue(isinstance(e, ResourceLimitExceeded))
        else:
            resource_1 = get_resource_by_id(resource_id_1)
            #resource_2 = get_resource_by_id(resource_id_2)

            self.assertTrue(resource_1.user_id == user.user_id)


