"""
Problem Domain:

Resource Controller handles all the requests to fetch user resource related details
"""
from flask_restplus import Resource
from flask import request
from ..util.dto import ResourceDto
from ..exceptions import UserResourceNotFound, ResourceLimitExceeded, ResourceNotFound, UserNotFound
from ..exceptions import InvalidAction
from ..service.resource_service import *
from ..service.user_service import create_new_user_resource
from ..service.auth_service import is_same_as_loggedin_user
from ..util.decorator import login_required, admin_required
from flask import current_app
api = ResourceDto.api
parser_one = api.parser()
parser_two = api.parser()
resource_req_data = ResourceDto.resource_req_data
resource_res_data = ResourceDto.resource_res_data

parser_one.add_argument('resource_id', required=False, default=None, location='args')
parser_two.add_argument('Authorization', required=True, help="Valid Auth token is required", location='headers')


@api.route('/')
class AllPlatformResources(Resource):
    @api.doc('list of all platform resources')
    @login_required
    @admin_required
    @api.expect(parser_two)
    @api.marshal_list_with(resource_res_data, envelope='data')
    def get(self, user_data=None, *args, **kwargs):
        """
        :purpose: Fetches the details of all the platform resources

        Note: Only Platform Admin is allowed to access the list of all platform resource
        """
        try:
            resp_obj = dict()

            current_app.logger.info("Request to fetch all platform resources")

            res = get_all_platform_resources()
            resp_obj['status'] = 'success'
            resp_obj['message'] = 'Total of ' + str(len(res)) + ' Resources exists on the platform!'
            resp_obj['data'] = res

            if not res:
                resp_obj['message'] = 'currently no user has created any resource on this platform'
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        else:
            return resp_obj, 200


@api.route('/<user_id>')
class AllUserResources(Resource):
    @api.doc('list of all user resources')
    @login_required
    @api.expect(parser_two)
    @api.marshal_list_with(resource_res_data, envelope='data')
    def get(self, user_id, user_data=None, *args, **kwargs):
        """
        :purpose: Fetches the details of all the resources of a particular user

        Note:
        * Login Required
        * Current Logged in user is allowed to list only his resources and cannot access
          other users resource
        * Platform Admin can access any users all resources
        """
        try:
            current_loggedin_user = user_data['user_id']
            is_loggedin_user_admin= user_data['platform_admin']
            resp_obj = dict()
            if is_same_as_loggedin_user(user_id, current_loggedin_user) or is_loggedin_user_admin:
                current_app.logger.info("Request to fetch a particular users all resources")
                res = get_user_resources(user_id=user_id)

                resp_obj['status'] = 'success'
                resp_obj['data'] = res
                if not res:
                    resp_obj['message'] = 'currently user has not created any resource on this platform'
            else:
                raise InvalidAction('Permission Denied')
        except InvalidAction as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 401
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        else:
            return resp_obj, 200

    @login_required
    @api.expect(resource_req_data, parser_two, validate=True)
    @api.response(201, 'user resource created successfully!')
    def post(self, user_id, user_data=None, *args, **kwargs):
        """
        :purpose: creates a new user resource

        Note:
        * Login Required
        * Current Logged in user is allowed to create only his resources
          and cannot create resources for other users
        * Platform Admin can create a resource for any user
        * If platform Admin creates a resource for some user and the quota is over then Platform
          admin has to increase the user quota first
        * User can create multiple resources with same name but internally
          it is stored with a unique id
        """
        try:
            current_loggedin_user = user_data['user_id']
            is_loggedin_user_admin = user_data['platform_admin']

            if is_same_as_loggedin_user(user_id, current_loggedin_user) or is_loggedin_user_admin:
                req_data = request.json

                create_new_user_resource(user_id, req_data)

                resp_obj = {
                    'status': 'success',
                    'message': 'user resource created successfully!'
                }
            else:
                raise InvalidAction('Permission Denied!')
        except InvalidAction as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 401
        except ResourceLimitExceeded as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 422
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        else:
            return resp_obj

    @login_required
    @api.doc('delete a particular user resource')
    @api.expect(parser_one, parser_two, validate=True)
    @api.doc(params={'resource_id': 'resource id'})
    @api.response(201, 'user resource deleted successfully!')
    def delete(self, user_id, user_data=None, *args, **kwargs):
        """
        :purpose: deletes a particular user resource

        Note:
        * Login Required
        * user can delete only his resources and cannot delete other users resources
        * if resource id is not provided it will delete all the user resources
        * Platform Admin can delete any users resource
        """
        try:
            current_loggedin_user = user_data['user_id']
            is_loggedin_user_admin = user_data['platform_admin']

            if is_same_as_loggedin_user(user_id, current_loggedin_user) or is_loggedin_user_admin:
                args = parser_one.parse_args()
                resource_id = args['resource_id'] if 'resource_id' in args else None

                # check if the current logged in user is as the user_id
                delete_user_resource(user_id, resource_id)

                resp_obj = {
                    'status': 'success',
                    'message': 'user resource deleted successfully!'
                }

                return resp_obj
            else:
                raise InvalidAction('Permission Denied!')
        except InvalidAction as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 401
        except UserNotFound or UserResourceNotFound as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 404
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400