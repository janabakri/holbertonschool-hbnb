"""
Application factory module
"""
from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    api = Api(app, 
              title="HBnB API", 
              version="1.0",
              description="HBnB Application REST API")
    
    # Create facade instance
    facade = HBnBFacade()
    
    # Inject facade into namespaces
    users_ns.facade = facade
    places_ns.facade = facade
    amenities_ns.facade = facade
    reviews_ns.facade = facade
    
    # Register namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    
    return app
