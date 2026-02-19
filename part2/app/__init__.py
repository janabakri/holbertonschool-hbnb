#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

def create_app():
    app = Flask(__name__)
    api = Api(app, title='HBnB API', version='1.0', description='HBnB Application API')
    
    from app.api.v1 import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app
