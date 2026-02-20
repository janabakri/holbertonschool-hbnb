from flask import Flask
from flask_restx import Api
from config import Config
from app.api.v1 import api as api_v1

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize API
    api_v1.init_app(app)
    
    return app
