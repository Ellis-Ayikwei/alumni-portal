import os
from flask import Flask, jsonify, request, make_response, abort, session, url_for
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect, generate_csrf
import logging

app = Flask(__name__)
from flask_cors import CORS

cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "*", "allow_headers": ["Content-Type", "X-CSRF-Token"]}})

# Load the secret key from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret')
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent CSRF
app.config['SESSION_TYPE'] = 'filesystem'

# Configure rate limiting (e.g., 10 requests per minute per IP)
#limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# CSRF Protection
csrf = CSRFProtect(app)



@app.route('/csrf-token', methods=['GET'])
@csrf.exempt
def csrf_token():
    token = generate_csrf()
    session['csrf_token'] = token
    response = make_response(jsonify({'csrf_token': token}))
    response.set_cookie('csrf_token', token)  # Set the CSRF token in a cookie
    logger.info(f"Generated CSRF Token: {token}")  # Log the CSRF token
    return response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Utility function to generate tokens
def generate_tokens(username):
    access_token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    refresh_token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return access_token, refresh_token

# Token decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            logger.info('Access token missing')
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.warning('Access token expired')
            return jsonify({'message': 'Token expired, refresh required'}), 401
        except jwt.InvalidTokenError:
            logger.warning('Invalid access token')
            return jsonify({'message': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    return decorated

# Route for login
@app.route('/login', methods=['POST'])
@csrf.exempt  # Exclude this route from CSRF protection
def login():
    auth = request.json
    csrf_token = generate_csrf()  # Generate CSRF token here

    if auth and auth['username'] == 'test' and auth['password'] == 'test':
        access_token, refresh_token = generate_tokens(auth['username'])

        # Set tokens in secure, HttpOnly cookies
        resp = make_response(jsonify({'message': 'Logged in successfully!'}))
        resp.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')
        resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax')

        # Send the CSRF token in a cookie
        resp.set_cookie('csrf_token', csrf_token, httponly=False, secure=True, samesite='Lax')  # Allow JS access
        logger.info(f"User '{auth['username']}' logged in")
        return resp

    logger.warning('Invalid login attempt')
    return jsonify({'message': 'Invalid credentials'}), 401




# Route to refresh the access token
@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        logger.info('Refresh token missing')
        return jsonify({'message': 'Refresh token is missing!'}), 401

    try:
        data = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
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

# Protected route
@app.route('/protected', methods=['GET'])
@login_required
def protected():
    logger.info('Access to protected route')
    return jsonify({'message': 'This is a protected route'})

# Route to log out and clear tokens
@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({'message': 'Logged out successfully!'}))
    resp.set_cookie('access_token', '', expires=0)
    resp.set_cookie('refresh_token', '', expires=0)
    logger.info('User logged out')
    return resp

# Custom error handler for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning('Rate limit exceeded')
    return jsonify(error="ratelimit exceeded", message="Too many requests. Please try again later."), 429

if __name__ == '__main__':
    # Run the app in production mode with debug=False
    # app.run(debug=True, threaded=True, use_reloader=False, ssl_context='adhoc')  # `ssl_context='adhoc'` for self-signed SSL in development
    #csrf.exempt(login)

    app.run(debug=True)