# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from .main.controller.auth_controller import api as user_auth_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.resource_controller import api as resource_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Chainstack Platform API\'s',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_auth_ns, path='/auth')
api.add_namespace(user_ns, path='/users')
api.add_namespace(resource_ns, path='/resources')

