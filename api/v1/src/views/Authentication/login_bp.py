import logging
from flask import Flask, current_app, jsonify, request, make_response, abort, session, url_for
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_wtf.csrf import CSRFProtect, generate_csrf
from api.v1.src.views import app_auth
from api.v1.app import bcrypt, csrf
from models import storage
from models.user import User
from .auth_utility import generate_tokens

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles login requests."""
    from api.v1.src.helpers.helper_functions import get_user_id_from_all_user
    data = request.get_json()

    # Check if the data is None or does not contain the required keys
    if not data or ('username' not in data and 'email' not in data) or 'password' not in data:
        return jsonify({'message': 'Missing username/email or password'}), 400

    user_id = None

    # Determine if we should use username or email
    if 'username' in data:
        user_id = get_user_id_from_all_user(username=data['username'])
    elif 'email' in data:
        user_id = get_user_id_from_all_user(email=data['email'])

    if user_id is None:
        return jsonify({'message': 'User not found'}), 404

    user = storage.get(User, user_id)

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token, refresh_token = generate_tokens(user.username)

        response = make_response(jsonify({'message': 'Logged in successfully!'}))
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax')

        csrf_token = generate_csrf()
        response.set_cookie('csrf_token', csrf_token, httponly=True, secure=True, samesite='Lax')

        return response

    return jsonify({'message': 'Invalid credentials'}), 401

def csrf_token():
    """
    Generates a CSRF token, saves it in the session and sets it as a cookie
    on the response. The token is also returned as a JSON response.

    Returns:
        flask.Response: JSON response containing the CSRF token.
    """
    token = generate_csrf()
    session['csrf_token'] = token
    response = make_response(jsonify({'csrf_token': token}))
    response.set_cookie('csrf_token', token)
    logger.info(f"Generated CSRF Token: {token}")
    return response
# Set up logging

# Route to refresh the access token
@app_auth.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        logger.info('Refresh token missing')
        return jsonify({'message': 'Refresh token is missing!'}), 401

    try:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        new_access_token, new_refresh_token = generate_tokens(data['user'])

        # Refresh both tokens, rotate refresh token
        resp = make_response(jsonify({'message': 'Token refreshed!'}))
        resp.set_cookie('access_token', new_access_token, httponly=True, secure=True, samesite='Lax')
        resp.set_cookie('refresh_token', new_refresh_token, httponly=True, secure=True, samesite='Lax')

        # Generate and send CSRF token
        csrf_token = generate_csrf()
        resp.set_cookie('csrf_token', csrf_token, httponly=False, secure=True, samesite='Lax')  # Allow JS access
        logger.info(f"Access token refreshed for user '{data['user']}'")
        return resp
    except jwt.ExpiredSignatureError:
        logger.warning('Refresh token expired')
        return jsonify({'message': 'Refresh token expired!'}), 401
    except jwt.InvalidTokenError:
        logger.warning('Invalid refresh token')
        return jsonify({'message': 'Invalid refresh token!'}), 401
