
from flask import Flask, jsonify, request, abort
from models.workout_level import WorkoutLevel
from models import storage


from api.v1.src.views import app_views
@app_views.route('/workout_levels', methods=['GET'])
def get_all_workout_levels():
    """Retrieve all workout levels"""
    workout_levels = storage.all(WorkoutLevel).values()
    workout_levels_list = [workout_level.to_dict() for workout_level in workout_levels]
    return jsonify(workout_levels_list), 200


@app_views.route('/workout_levels/<int:workout_level_id>', methods=['GET'])
def get_workout_level(workout_level_id):
    """Retrieve a specific workout level by ID"""
    workout_level = storage.get(WorkoutLevel, workout_level_id)
    if workout_level is None:
        abort(404, description="Workout level not found")
    return jsonify(workout_level.to_dict()), 200


@app_views.route('/workout_levels', methods=['POST'])
def create_workout_level():
    """Create a new workout level"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['description', 'level_name', 'suitable_for_female', 'suitable_for_male', 'image']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create new WorkoutLevel object
    new_workout_level = WorkoutLevel(
        **data
    )
    
    new_workout_level.save()

    return jsonify(new_workout_level.to_dict()), 201


@app_views.route('/workout_levels/<int:workout_level_id>', methods=['PUT'])
def update_workout_level(workout_level_id):
    """Update an existing workout level"""
    workout_level = storage.get(WorkoutLevel, workout_level_id)
    if workout_level is None:
        abort(404, description="Workout level not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    workout_level.description = data.get('description', workout_level.description)
    workout_level.level_name = data.get('level_name', workout_level.level_name)
    workout_level.suitable_for_female = data.get('suitable_for_female', workout_level.suitable_for_female)
    workout_level.suitable_for_male = data.get('suitable_for_male', workout_level.suitable_for_male)
    workout_level.image = data.get('image', workout_level.image)

    storage.save()
    return jsonify(workout_level.to_dict()), 200


@app_views.route('/workout_levels/<int:workout_level_id>', methods=['DELETE'])
def delete_workout_level(workout_level_id):
    """Delete a workout level"""
    workout_level = storage.get(WorkoutLevel, workout_level_id)
    if workout_level is None:
        abort(404, description="Workout level not found")

    storage.delete(workout_level)
    storage.save()
    return jsonify({}), 200


