from flask import jsonify, request, abort
from models import storage
from api.v1.src.views import app_views
from models.coach import Coach

@app_views.route('/coaches', methods=['GET'])
def get_all_coaches():
    """Retrieve all coaches"""
    coaches = storage.all(Coach).values()
    coach_list = [coach.to_dict() for coach in coaches]
    return jsonify(coach_list), 200

@app_views.route('/coaches/<coach_id>', methods=['GET'])
def get_coach(coach_id):
    """Retrieve a specific coach by ID"""
    coach = storage.get(Coach, coach_id)
    if coach is None:
        abort(404, description="Coach not found")
    return jsonify(coach.to_dict()), 200

@app_views.route('/coaches', methods=['POST'])
def create_coach():
    """Create a new coach"""
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    required_fields = ['user_id', 'specialization', 'experience_years']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    new_coach = Coach(**data)
    new_coach.save()
    return jsonify(new_coach.to_dict()), 201

@app_views.route('/coaches/<coach_id>', methods=['PUT'])
def update_coach(coach_id):
    """Update an existing coach"""
    coach = storage.get(Coach, coach_id)
    if coach is None:
        abort(404, description="Coach not found")
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    updateable_fields = ['specialization', 'experience_years']
    for key, value in data.items():
        if key in updateable_fields:
            setattr(coach, key, value)
    coach.save()
    return jsonify(coach.to_dict()), 200

@app_views.route('/coaches/<coach_id>', methods=['DELETE'])
def delete_coach(coach_id):
    """Delete a coach"""
    coach = storage.get(Coach, coach_id)
    if coach is None:
        abort(404, description="Coach not found")
    storage.delete(coach)
    storage.save()
    return jsonify({}), 200

