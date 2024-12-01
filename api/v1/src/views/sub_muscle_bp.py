from flask import jsonify, request, abort
from models import storage
from models.sub_muscle import SubMuscle
from api.v1.src.views import app_views

@app_views.route('/sub_muscles', methods=['GET'], strict_slashes=False)
def get_all_sub_muscles():
    """Retrieve all sub muscles"""
    sub_muscles = storage.all(SubMuscle).values()
    sub_muscles_list = [sub_muscle.to_dict() for sub_muscle in sub_muscles]
    return jsonify(sub_muscles_list), 200

@app_views.route('/sub_muscles/<sub_muscle_id>', methods=['GET'])
def get_sub_muscle_by_id(sub_muscle_id):
    """Retrieve a specific sub muscle by ID"""
    sub_muscle = storage.get(SubMuscle, sub_muscle_id)
    if sub_muscle is None:
        abort(404, description="Sub muscle not found")
    return jsonify(sub_muscle.to_dict()), 200

@app_views.route('/sub_muscles', methods=['POST'])
def create_sub_muscle():
    """Create a new sub muscle"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    new_sub_muscle = SubMuscle(**data)
    new_sub_muscle.save()
    return jsonify(new_sub_muscle.to_dict()), 201

@app_views.route('/sub_muscles/<sub_muscle_id>', methods=['PUT'])
def update_sub_muscle(sub_muscle_id):
    """Update an existing sub muscle"""
    sub_muscle = storage.get(SubMuscle, sub_muscle_id)
    if sub_muscle is None:
        abort(404, description="Sub muscle not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at', '__class__']
    for key, value in data.items():
        if key not in ignore:
            setattr(sub_muscle, key, value)
    sub_muscle.save()
    return jsonify(sub_muscle.to_dict()), 200

@app_views.route('/sub_muscles/<sub_muscle_id>', methods=['DELETE'])
def delete_sub_muscle(sub_muscle_id):
    """Delete a sub muscle"""
    sub_muscle = storage.get(SubMuscle, sub_muscle_id)
    if sub_muscle is None:
        abort(404, description="Sub muscle not found")
    storage.delete(sub_muscle)
    storage.save()
    return jsonify({}), 200

