from flask import Flask
from config import config


from app.extensions import db, jwt, bcrypt

def create_app(config_name='default'):
    """Application factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
