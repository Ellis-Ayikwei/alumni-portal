from flask import Blueprint, abort, flash, redirect, request, url_for
from api.v1.src.views.Authentication.user_validation import validate_user_data
from models.user import User
from api.v1.src.views import app_views
from api.v1.src.helpers.helper_functions import is_username_already_taken

@app_views.route("/register", methods=["GET", "POST"], strict_slashes=False)
def register():
    """Register a new user"""
    form_data = request.form
    if not form_data:
        abort(400, description="Not a JSON")

    try:
        validated_data = validate_user_data(form_data)
    except ValueError as e:
        abort(400, description=str(e))

    if is_username_already_taken(validated_data['username']):
        abort(400, description="Sorry, username already taken. Please choose another one.")

    new_user = User(**validated_data)
    new_user.save()

    flash("You have registered successfully. Please log in.", "success")
    return redirect(url_for("login"))  # Redirect to the login page
