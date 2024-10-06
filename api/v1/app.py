#!/usr/bin/env python3
"""The Flask app for Sprout Collab"""

import os
from flask import Flask, make_response, jsonify


from .src.views import app_views, app_auth
from models import storage
from flasgger import Swagger
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Initialize Bcrypt and CSRF globally
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret')
    app.config['SESSION_COOKIE_SECURE'] = True  # Ensure HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize extensions
    bcrypt.init_app(app)
    CORS(app, supports_credentials=True)
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(app_views)
    app.register_blueprint(app_auth)

    # Configure Swagger
    app.config['SWAGGER'] = {
        'title': 'Sprout Collab Restful API',
        'uiversion': 3
    }
    Swagger(app)

    @app.teardown_appcontext
    def close_db(error):
        """Close Storage"""
        storage.close()

    @app.errorhandler(404)
    def not_found(error):
        """404 Error
        ---
        responses:
          404:
            description: a resource was not found
        """
        return make_response(jsonify({'error': "Not found"}), 404)

    return app

if __name__ == "__main__":
    from api.v1.src.views.Authentication.login_bp import login

    app = create_app()
    csrf.exempt(login)
    app.run(host="0.0.0.0", port=5004, threaded=True, debug=True)
