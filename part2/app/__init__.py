from flask import Flask
from flask_restx import Api
from config import Config
from app.services.facade import HBnBFacade

# Create a single instance of the facade
facade = HBnBFacade()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Store facade in app config for sharing
    app.config['facade'] = facade
    
    # Import and initialize API
    from app.api.v1 import api as api_v1
    api_v1.init_app(app)
    
    return app
