"""
Problem Domain:

Resource Controller handles all the requests to fetch user resource related details
"""
from flask_restplus import Resource
from flask import request
from ..util.dto import ResourceDto
from ..exceptions import UserResourceNotFound, ResourceLimitExceeded, ResourceNotFound, UserNotFound
from ..service.resource_service import *
from ..service.user_service import create_new_user_resource

from flask import current_app
api = ResourceDto.api
parser = api.parser()
resource_req_data = ResourceDto.resource_req_data
resource_res_data = ResourceDto.resource_res_data

parser.add_argument('resource_id', required=False, default=None, location='args')


@api.route('/')
class AllPlatformResources(Resource):
    @api.doc('list of all platform resources')
    @api.marshal_list_with(resource_res_data, envelope='data')
    def get(self):
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

        except ResourceNotFound as e:
            resp_obj = dict()
            resp_obj['status'] = 'fail'
            resp_obj['message'] = str(e)

            return resp_obj, 404
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
    @api.marshal_list_with(resource_res_data, envelope='data')
    def get(self, user_id):
        """
        :purpose: Fetches the details of all the resources of a particular user

        Note:
        * Login Required
        * Current Logged in user is allowed to list only his resources and cannot access
          other users resource
        * Platform Admin can access any users all resources
        """
        try:
            resp_obj = dict()
            current_app.logger.info("Request to fetch a particular users all resources")
            res = get_user_resources(user_id=user_id)

            resp_obj['status'] = 'success'
            resp_obj['data'] = res
            if not res:
                resp_obj['message'] = 'currently user has not created any resource on this platform'

        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        else:
            return resp_obj, 200

    @api.expect(resource_req_data, validate=True)
    @api.response(201, 'user resource created successfully!')
    def post(self, user_id):
        """
        :purpose: creates a new user resource

        Note:
        * Login Required
        * Current Logged in user is allowed to create only his resources
          and cannot create resources for other users
        * Platform Admin can create a resource for any user
        * User can create multiple resources with same name but internally
          it is stored with a unique id
        """
        try:
            req_data = request.json

            create_new_user_resource(user_id, req_data)

            resp_obj = {
                'status': 'success',
                'message': 'user resource created successfully!'
            }
        except ResourceLimitExceeded as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        except Exception as e:
            resp_obj = {
                'status': 'fail',
                'message': str(e)
            }

            return resp_obj, 400
        else:
            return resp_obj

    @api.doc('delete a particular user resource')
    @api.expect(parser)
    @api.doc(params={'resource_id': 'resource id'})
    @api.response(201, 'user resource deleted successfully!')
    def delete(self, user_id):
        """
        :purpose: deletes a particular user resource

        Note:
        * Login Required
        * user can delete only his resources and cannot delete other users resources
        * if resource id is not provided it will delete all the user resources
        * Platform Admin can delete any users resource
        """
        try:
            args = parser.parse_args()
            resource_id = args['resource_id'] if 'resource_id' in args else None

            # check if the current logged in user is as the user_id
            delete_user_resource(user_id, resource_id)

            resp_obj = {
                'status': 'success',
                'message': 'user resource deleted successfully!'
            }

            return resp_obj
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