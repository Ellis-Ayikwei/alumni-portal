from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage
from api.v1.src.views import app_views
from models.workout import Workout


@app_views.route('/workouts', methods=['GET'])
def get_all_workouts():
    """Retrieve all workouts"""
    workouts = storage.all(Workout).values()
    workouts_list = [workout.to_dict() for workout in workouts]
    return jsonify(workouts_list), 200


@app_views.route('/workouts/<workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Retrieve a specific workout by ID"""
    workout = storage.get(Workout, workout_id)
    if workout is None:
        abort(404, description="Workout not found")
    return jsonify(workout.to_dict()), 200


@app_views.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout"""
    from api.v1.app import uploaded_files

    if not request.form:
        abort(400, description="No form data received")

    # Extract data from form
    form_data = request.form
    required_fields = ['title', 'description', 'duration_minutes', 'muscle_group_id', 'sub_muscle_group_id']
    for field in required_fields:
        if field not in form_data:
            abort(400, description=f"Missing {field}")

    # Create the Workout object
    try:
        new_workout = Workout(
            title=form_data["title"],
            description=form_data['description'],
            duration_minutes=int(form_data['duration_minutes']),
            muscle_group_id=int(form_data['muscle_group_id']),
            sub_muscle_group_id=int(form_data['sub_muscle_group_id'])
        )
    except ValueError as error:
        abort(400, description=f"Invalid data: {str(error)}")

    # Save the object
    new_workout.save()

    return jsonify(new_workout.to_dict()), 201


@app_views.route('/workouts/<workout_id>', methods=['PUT'])
def update_workout(workout_id):
    """Update an existing workout"""
    workout = storage.get(Workout, workout_id)
    if workout is None:
        abort(404, description="Workout not found")

    if not request.form:
        abort(400, description="Not a JSON or form data")

    data = request.form
    ignore = ['id', 'created_at', 'updated_at', '__class__', 'workout']
    for key, value in data.items():
        if key not in ignore:
            setattr(workout, key, value)

    storage.save()
    return jsonify(workout.to_dict()), 200


@app_views.route('/workouts/<workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout"""
    workout = storage.get(Workout, workout_id)
    if workout is None:
        abort(404, description="Workout not found")

    storage.delete(workout)
    storage.save()
    return jsonify({}), 200


