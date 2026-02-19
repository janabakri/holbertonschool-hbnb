from flask_restx import Api
from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(bp, version='1.0', title='HBnB API', description='HBnB RESTful API v1')

from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns
from .amenities import api as amenities_ns

api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')

__all__ = ['bp']
