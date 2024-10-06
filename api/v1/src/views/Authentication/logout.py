

from venv import logger
from flask import make_response,jsonify
from v1.src.views import app_views


@app_views.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({'message': 'Logged out successfully!'}))
    resp.set_cookie('access_token', '', expires=0)
    resp.set_cookie('refresh_token', '', expires=0)
    logger.info('User logged out')
    return resp