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
from app.main.service.user_service import create_new_user, get_user_by_id


class TestUserModel(BaseTestCase):
    def test_user_creation(self):

        data = dict()
        data['email'] = 'test@gmail.com'
        data['password'] = 'test123'

        new_user_id = create_new_user(data)

        # Test user created successfully
        self.assertTrue(new_user_id)

        new_user = get_user_by_id(new_user_id)
        # Test by default new user can create as many resource as required

        self.assertTrue(new_user.user_quota == -1)
