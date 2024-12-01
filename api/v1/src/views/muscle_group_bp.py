from flask import jsonify, request, abort
from models import storage
from models.muscle_group import MuscleGroup
from api.v1.src.views import app_views

@app_views.route('/muscle_groups', methods=['GET'])
def get_all_muscle_groups():
    """Retrieve all muscle groups"""
    muscle_groups = storage.all(MuscleGroup).values()
    muscle_groups_list = [muscle_group.to_dict() for muscle_group in muscle_groups]
    return jsonify(muscle_groups_list), 200


@app_views.route('/muscle_groups/<muscle_group_id>', methods=['GET'])
def get_muscle_group(muscle_group_id):
    """Retrieve a specific muscle group by ID"""
    muscle_group = storage.get(MuscleGroup, muscle_group_id)
    if muscle_group is None:
        abort(404, description="Muscle group not found")
    return jsonify(muscle_group.to_dict()), 200


@app_views.route('/muscle_groups', methods=['POST'], strict_slashes=False)
def create_muscle_group():
    """Create a new muscle group"""

    if not request.get_json():
        abort(400, description="No form data received")

    # Extract data from form
    form_data = request.get_json()
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in form_data:
            abort(400, description=f"Missing {field}")

    # Create the MuscleGroup object
    try:
        new_muscle_group = MuscleGroup(**form_data)
    except ValueError as error:
        abort(400, description=f"Invalid data: {str(error)}")

    new_muscle_group.save()

    return jsonify(new_muscle_group.to_dict()), 201


@app_views.route('/muscle_groups/<muscle_group_id>', methods=['PUT'])
def update_muscle_group(muscle_group_id):
    """Update an existing muscle group"""
    
    muscle_group = storage.get(MuscleGroup, muscle_group_id)
    if muscle_group is None:
        abort(404, description="Muscle group not found")
    
    if not request.get_json():
        abort(400, description="Not a JSON or form data")
    
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at', '__class__']
    for key, value in data.items():
        if key not in ignore:
            setattr(muscle_group, key, value)
    
    storage.save()
    return jsonify(muscle_group.to_dict()), 200


@app_views.route('/muscle_groups/<muscle_group_id>', methods=['DELETE'])
def delete_muscle_group(muscle_group_id):
    """Delete a muscle group"""
    muscle_group = storage.get(MuscleGroup, muscle_group_id)
    if muscle_group is None:
        abort(404, description="Muscle group not found")

    storage.delete(muscle_group)
    storage.save()
    return jsonify({}), 200

