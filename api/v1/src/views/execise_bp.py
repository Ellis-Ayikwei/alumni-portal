from flask import Flask, jsonify, request, abort
from models import storage
from models.exercise import Exercise

from api.v1.src.views import app_views

@app_views.route('/exercises', methods=['GET'])
def get_all_exercises():
    """Retrieve all exercises"""
    exercises = storage.all(Exercise).values()
    exercise_list = [exercise.to_dict() for exercise in exercises]
    return jsonify(exercise_list), 200


@app_views.route('/exercises/<exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """Retrieve a specific exercise by ID"""
    exercise = storage.get(Exercise, exercise_id)
    if exercise is None:
        abort(404, description="Exercise not found")
    return jsonify(exercise.to_dict()), 200


@app_views.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['name', 'gif_url', 'local_png', 'local_url', 'metric', 'target', 'equipment', 'body_part']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    new_exercise = Exercise(
        name=data['name'],
        gif_url=data['gif_url'],
        local_png=data['local_png'],
        local_url=data['local_url'],
        metric=data['metric'],
        target=data['target'],
        equipment=data['equipment'],
        body_part=data['body_part']
    )

    storage.new(new_exercise)
    storage.save()

    return jsonify(new_exercise.to_dict()), 201


@app_views.route('/exercises/<exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    """Update an existing exercise"""
    exercise = storage.get(Exercise, exercise_id)
    if exercise is None:
        abort(404, description="Exercise not found")

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    exercise.name = data.get('name', exercise.name)
    exercise.gif_url = data.get('gif_url', exercise.gif_url)
    exercise.local_png = data.get('local_png', exercise.local_png)
    exercise.local_url = data.get('local_url', exercise.local_url)
    exercise.metric = data.get('metric', exercise.metric)
    exercise.target = data.get('target', exercise.target)
    exercise.equipment = data.get('equipment', exercise.equipment)
    exercise.body_part = data.get('body_part', exercise.body_part)

    storage.save()
    return jsonify(exercise.to_dict()), 200


@app_views.route('/exercises/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """Delete an exercise"""
    exercise = storage.get(Exercise, exercise_id)
    if exercise is None:
        abort(404, description="Exercise not found")

    storage.delete(exercise)
    storage.save()
    return jsonify({}), 200

