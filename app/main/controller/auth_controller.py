"""
Problem Domain:

Auth Controller handles user authentication
"""
from flask import request, Response
from flask import current_app
from flask_restplus import Resource, reqparse
from ..service.auth_service import *
from ..util.dto import AuthDto
# from ..util.decorator import login_required
from .. import flask_bcrypt
api = AuthDto.api
user_auth = AuthDto.user_auth

parser = reqparse.RequestParser()
# add location as args to search in queryString
parser.add_argument('Authorization', required=True, help="Valid Auth token is required", location='headers')


@api.route('/login')
class UserLogin(Resource):
    """ User Login Resource """
    @api.doc('User Login')
    @api.expect(user_auth, validate=True)
    def post(self):
        """
        :purpose: User Login that generates auth token

        Note:
        * Every api on this platform requires a Login first
        * Every User including Platform Admin has to Login first to recieve the auth token
          which identifies the user and gives restricted access to this platform
        * It generates an authentication token which user can further use to create/delete/list resources on this platform
        * the auth token is valid for some time and user have to regenerate auth token once this time elapses
        * User cannot use already used auth token as these will be dumped
        """
        try:
            req_data = request.json
            res, http_status = login_user(req_data)
            return res, http_status
        except UserNotFound as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 404


@api.route('/logout')
class UserLogout(Resource):
    """ User Logout Resource """
    @api.doc('User Logout')
    @api.expect(parser, validate=True)
    def post(self):
        """
        :purpose: Logout User and invalidate auth token

        Note:
        * User has to Login first and send valid auth token in header to Logout
        * Once the User Logs out the auth token will be dumped

        **Important
        * Copy the auth token from login operation above and paste it in the Authorization header field below
        """
        try:
            auth_header = request.headers.get('Authorization')

            if auth_header:
                res, http_status = logout_user(auth_header)

                return res, http_status
            else:
                resp_obj = {
                    'status': 'fail',
                    'message': 'Please Provide a Valid Auth Token!'
                }

                return resp_obj, 403
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 200

