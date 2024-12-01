from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage
from api.v1.src.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User Object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    from api.v1.src.helpers.helper_functions import is_username_already_taken, is_email_already_registered

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'username' not in data or not isinstance(data['username'], str):
        abort(400, description="Invalid or missing username")

    if is_username_already_taken(data):
        abort(400, description="Sorry, username already taken. Please choose another one.")
    if is_email_already_registered(data):
        abort(400, description="Sorry, email has been registered. Please use another one.")
    if 'password' not in data or not isinstance(data['password'], str):
        abort(400, description="Invalid or missing password")

    new_user = User(**data)
    new_user.save()

    # Logging user creation attempt
    # if new_user.id:
    #     logging.info(f"User created successfully with id: {new_user.id}")
    # else:
    #     logging.error("Failed to create user")

    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    # new_user_id = get_user_id_from_all_user(username=data.get('username'), email=data.get('email'))
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    ignore = ['id', 'created_at', 'updated_at', '__class__']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)



@app_views.route('/users/reset_password/<user_id>', methods=['PUT'], strict_slashes=False)
def reset_user_password(user_id):
    """Resets a user's password"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not current_password or not new_password:
        abort(400, description="Missing current password or new password")

    if not user.verify_password(current_password):
        abort(403, description="Invalid current_password")

    if current_password == new_password:
        abort(400, description="new password cannot be the same as the old password")

    user.reset_password(current_password, new_password)
    user.save()

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/my_profile/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_profile(user_id):
    """Retrieves a user's profile information"""
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)

    return make_response(jsonify(user_instance.to_dict()), 200)



@app_views.route('/users/user_profile_completion/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_profile_completion(user_id):
    """Calculate the completion percentage of a user's profile."""
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "middle_names",
        "gender",
        "dob",
        "occupation",
        "address",
        "other_names",
    ]

    completed_fields = [
        field for field in required_fields if getattr(user_instance, field)
    ]

    completion_percentage = int((len(completed_fields) / len(required_fields)) * 100)

    return jsonify({"completion_percentage": completion_percentage})
