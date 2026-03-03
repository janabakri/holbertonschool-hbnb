from flask import Flask
from config import config_dict
from app.extensions import db, jwt, bcrypt

# Import your API blueprints
from app.api.v1.users import users_bp
from app.api.v1.places import places_bp
from app.api.v1.amenities import amenities_bp
from app.api.v1.reviews import reviews_bp
from app.api.v1.auth import auth_bp  # <- auth blueprint

def create_app(config_name="development"):
    """Factory to create Flask app with all extensions and blueprints"""
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register API blueprints
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(places_bp, url_prefix="/api/v1/places")
    app.register_blueprint(amenities_bp, url_prefix="/api/v1/amenities")
    app.register_blueprint(reviews_bp, url_prefix="/api/v1/reviews")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")  # <- login/register

    return app
