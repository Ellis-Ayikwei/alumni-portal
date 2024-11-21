#!/usr/bin/env python3
"""The Flask app for Sprout Collab"""

import datetime
import json
import os
import sys
from colorama import Fore
from flask import Flask, make_response, jsonify, request
from flask_mail import Mail
import redis

from api.v1.src.services.auditslogging.logginFn import (log_audit,
                                                        app_views_info_logger,
                                                        app_views_debug_logger,
                                                        app_views_error_logger,
                                                        app_auth_info_logger,
                                                        app_auth_error_logger)

from .src.views import app_views, app_auth
from models import storage
from flasgger import Swagger
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models.user import User

# Initialize Bcrypt and CSRF globally
bcrypt = Bcrypt()
mail = Mail()
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

ACCESS_EXPIRES = datetime.timedelta(hours=1)

def create_app():
    app = Flask(__name__)
    jwt =JWTManager(app)
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['FLASK_MAIL_DEBUG'] = True
    
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')


    print(os.getenv('MAIL_USERNAME'))
    print(os.getenv('MAIL_PASSWORD'))
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  
    mail.init_app(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None
    
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config['JWT_HEADER_NAME']  = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"


    app.config["CORS_HEADERS"] = ["Content-Type", "Authorization", "X-Refresh-Token"]
    app.config["JWT_SECRET_KEY"] = "super-secret"


    # Initialize extensions
    bcrypt.init_app(app)

    CORS(app,
        resources={r"/*": {"origins": ["http://localhost:5173"]}},
        supports_credentials=True,
        expose_headers=["Authorization", "X-Refresh-Token"],
        allow_headers=["Content-Type", "Authorization", "X-Refresh-Token"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    
    print(app.url_map)
    

    # Register blueprints
    app.register_blueprint(app_views)
    app.register_blueprint(app_auth)


    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Refresh-Token"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response, 204

    @app.after_request
    def after_request(response):
        origin = request.headers.get("Origin")
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Refresh-Token"
        response.headers["Access-Control-Expose-Headers"] = "Authorization, X-Refresh-Token"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
        
    
    
    

    @app.after_request
    def log_audit_trail(response):
        from models.audit_trails import Status
        methods_to_audit = ["POST", "PUT", "DELETE"]
        success_status_codes = [200, 201, 204]
        
        # Skip logging for non-auditable methods
        if request.method not in methods_to_audit:
            return response
        
        try:
            # Set the action based on the request method
            action = request.method

            # Parse response data
            try:
                response_data = json.loads(response.data.decode('utf-8'))
            except (ValueError, AttributeError):
                response_data = {}

            # Parse request data
            request_data = json.loads(request.data.decode('utf-8'))

            # Determine the user_id from response or request data
            user_id = (
                response_data.get("id") if "__class__" in response_data and response_data["__class__"] == "User" else
                request_data.get("user_id")
            )

            # Determine the status based on response status code
            status =  Status.COMPLETED if response.status_code in success_status_codes else Status.FAILED

            # Additional audit details
            details = {
                "status_code": response.status_code,
                "ip_address": request.remote_addr,
                "method": request.method,
                "url": request.url,
            }

            # Skip logging if status code is not 204
            if response.status_code == 204:
                return response

            # Item audited
            item_audited = response_data.get("id") or response_data.get("name")

            # Log the audit
            user_name = log_audit(user_id, action, status, details, item_audited=item_audited)

            # Log audit trail info
            app_views_info_logger.info(f"User: {user_name}, Action: {action}, Status: {status}, Item Audited: {item_audited}")
        except Exception as e:
            # Log errors
            app_views_error_logger.error(f"Failed to log audit trail: {str(e)}")

        return response





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
    app = create_app()
    app.run(host="0.0.0.0", port=5004, threaded=True, debug=True)

