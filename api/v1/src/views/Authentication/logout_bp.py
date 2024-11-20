from venv import logger
from flask import make_response, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
import redis
from api.v1.src.views import app_auth




# @app_auth.route("/logout", methods=["POST"], strict_slashes=False)
# def logout():
#     print("the haaders", request.headers)
#     return jsonify({"logout": "ok"})



@app_auth.route("/logout", methods=["POST"], strict_slashes=False)
@jwt_required()
def logout():
    from api.v1.app import ACCESS_EXPIRES, jwt_redis_blocklist
    try:
        token = get_jwt()
        logger.info(f"Logging out token: {token}")
        print("JWT Data:", token)
        jti = token["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify(msg="Access token revoked"), 202
    except Exception as e:
        logger.error(f"Error in logout: {str(e)}")
        return jsonify(msg="Token not found or invalid"), 400
