"""
Problem Domain:
Auth Service provides login and logout service
assumptions:
When the user logs out then he cannot use the same token to login again and hence added to black listed token
"""
from datetime import datetime
from ..model.user import User
from .user_service import get_user_by_email, get_user_by_id
from ..service.token_garbage_service import dump_token
from ...main.exceptions import UserNotFound


def login_user(data):
    """ logs in user """
    email = data['email']
    password = data['password']

    user = get_user_by_email(email)

    if user and user.check_password(password):
        auth_token = User.encode_auth_token(user.user_id)
        if auth_token:
            res_obj = {
                'status': 'success',
                'message': 'successfully logged in',
                'Authorization': auth_token.decode()
            }

            return res_obj, 200
    else:
        raise UserNotFound('Sorry! Credentials does not match or User is not registered with the platform.')


def logout_user(data):
    """
    :param data: user Authorization details
    :return: logout response
    :purpose: logout current user and invalidate auth token
    """
    try:
        auth_token = data if data else ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                # dump this token as user has logout
                return dump_token(auth_token)
            else:
                resp_obj = {
                    'status': 'fail',
                    'message': resp
                }
                return resp_obj, 401
        else:
            resp_obj = {
                'status': 'fail',
                'message': 'Provide a valid auth Token'
            }
            return resp_obj, 403
    except Exception as e:
        resp_obj = {
            'status': 'fail',
            'message': str(e)
        }
        return resp_obj, 403


def get_logged_in_user(user_request):
    """
    :param user_request: Http request object
    :return resp_obj: logged in user object as part of the resp_obj
    purpose:
    returns the current logged in user from the request header authorization token, failure response otherwise
    """
    try:
        # get the auth token from the request headers
        auth_token = user_request.headers.get('Authorization')
        if auth_token:
            user_id = User.decode_auth_token(auth_token)
            user = get_user_by_id(user_id)

            resp_obj = {
                'status': 'success',
                'data': {
                    'user_id': str(user.user_id),
                    'email': user.email,
                    'registered_on': datetime.strftime(user.user_registered_on, "%Y-%m-%d %H:%M:%S"),
                    'platform_admin': user.platform_admin
                }
            }
            return resp_obj, 200
        else:
            resp_obj = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }

            return resp_obj, 401
    except Exception as e:
        resp_obj = {
            'status': 'fail',
            'message': str(e)
        }

        return resp_obj, 401


def is_same_as_loggedin_user(requested_user_id, loggedin_user_id):
    """
    :param requested_user: user requested
    :param loggedin_user: current loggedin user
    :purpose: checks wheather the requested user is same as logged in user
    """
    return requested_user_id == loggedin_user_id