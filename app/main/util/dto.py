"""
Problem Domain

DTO contains all the input data validation expected data and how data is to be marshalled while
sending the response
"""
from flask_restplus import fields, Namespace


class AuthDto:
    """DTO of Auth Model"""
    api = Namespace('auth', description='User Login authentication details')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='user name'),
        'password': fields.String(required=True, description='user password')
    })


class UserDto:
    """DTO of User Model"""
    api = Namespace('user', description='request object to create platform Users')
    user_req_model = api.model('user_req_details', {
        'email': fields.String(required=True, description='unique user email'),
        'password': fields.String(required=True, description='user password')
    })

    user_res = api.model('user_res', {
        'user_id': fields.Integer(required=True, description='user id'),
        'email': fields.String(required=True, description='unique user email'),
        'user_registered_on': fields.DateTime(required=True, description='user registered on'),
        'user_quota': fields.Integer(required=True, description='user quota'),
        'quota_remaining': fields.Integer(required=True, description='user quota remaining')
    })

    user_res_model = api.model('user_res_details', {
        'status': fields.String(required=True, description='status of response'),
        'message': fields.String(required=False, description='action message'),
        'data': fields.List(fields.Nested(user_res), required=False)
    })


class ResourceDto:
    """DTO of Resource Model"""
    api = Namespace('resource', description='request object to create platform User Resources')

    resource_req_data = api.model('resource_req_data', {
        'resource_name': fields.String(required=True, description='Resource name')
    })

    resource_res = api.model('resource_res', {
        'user_id': fields.Integer(required=True, description='user id'),
        'resource_id': fields.Integer(required=True, description='resource id'),
        'resource_name': fields.String(required=True, description='resource name')
    })

    resource_res_data = api.model('resource_res_data', {
        'status': fields.String(required=True, description='status of response'),
        'message': fields.String(required=False, description='action message'),
        'data': fields.List(fields.Nested(resource_res), required=False)
    })

