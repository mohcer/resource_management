"""
Problem Domain:

Design generic decorators to implement auth and idm
"""

from functools import wraps
from functools import partial
from flask import request

from ..service.auth_service import *
current_logged_in_user = None
is_loggedin_user_admin = False


def login_required(func):
    """
    :param func: input function on which this decorator wraps
    :return : input function call
    purpose:
    calls the input function if the user is logged in, returns failure response otherwise
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        global current_logged_in_user, is_loggedin_user_admin

        data, status = get_logged_in_user(request)

        if status is 200:
            user_dict = data.get('data')
            current_logged_in_user = user_dict['user_id']
            is_loggedin_user_admin = user_dict['platform_admin']
            if not user_dict:
                resp_obj = {
                    'status': 'fail',
                    'message': 'invalid token recieved'
                }
                return resp_obj, status

            return func(user_data=user_dict, *args, **kwargs)
        else:
            return data, status

    return decorated


def admin_required(func):
    """
    :param func: input function on which this decorator wraps
    :return : input function call
    assumption: this decorator assumes the user is logged in
    purpose:  calls the input function if the logged in user is super user, returns failure response otherwise
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        global is_loggedin_user_admin
        global current_logged_in_user

        # if logged in user is super user call the input function
        if is_loggedin_user_admin:
            return func(*args, **kwargs)
        else:
            # the logged in user is not a super user return failure response
            resp_obj = {
                'status': 'fail',
                'message': 'Sorry need admin privileges for this operation!'
            }

            return resp_obj, 401

    return decorated