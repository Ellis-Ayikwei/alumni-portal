from flask import Flask, jsonify, request, abort
from models import storage
from models.amendment import Amendment

from api.v1.src.views import app_views
@app_views.route('/amendments', methods=['GET'])
def get_all_amendments():
    """Retrieve all amendments"""
    amendments = storage.all(Amendment).values()
    amendments_list = [amendment.to_dict() for amendment in amendments]
    return jsonify(amendments_list), 200


@app_views.route('/amendments/<amendment_id>', methods=['GET'])
def get_amendment(amendment_id):
    """Retrieve a specific amendment by ID"""
    amendment = storage.get(Amendment, amendment_id)
    if amendment is None:
        abort(404, description="Amendment not found")
    return jsonify(amendment.to_dict()), 200


@app_views.route('/amendments', methods=['POST'])
def create_amendment():
    """Create a new amendment"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['contract_id', 'amended_by', 'change_log', 'new_values', 'old_values']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create new Amendment object
    new_amendment = Amendment(
        contract_id=data['contract_id'],
        amended_by=data['amended_by'],
        change_log=data['change_log'],
        new_values=data['new_values'],
        old_values=data['old_values'],
        change_date=data.get('change_date', datetime.utcnow())  # Optional field
    )
    
    storage.new(new_amendment)
    storage.save()

    return jsonify(new_amendment.to_dict()), 201


@app_views.route('/amendments/<amendment_id>', methods=['PUT'])
def update_amendment(amendment_id):
    """Update an existing amendment"""
    amendment = storage.get(Amendment, amendment_id)
    if amendment is None:
        abort(404, description="Amendment not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    amendment.contract_id = data.get('contract_id', amendment.contract_id)
    amendment.amended_by = data.get('amended_by', amendment.amended_by)
    amendment.change_log = data.get('change_log', amendment.change_log)
    amendment.new_values = data.get('new_values', amendment.new_values)
    amendment.old_values = data.get('old_values', amendment.old_values)
    amendment.change_date = data.get('change_date', amendment.change_date)

    storage.save()
    return jsonify(amendment.to_dict()), 200


@app_views.route('/amendments/<amendment_id>', methods=['DELETE'])
def delete_amendment(amendment_id):
    """Delete an amendment"""
    amendment = storage.get(Amendment, amendment_id)
    if amendment is None:
        abort(404, description="Amendment not found")

    storage.delete(amendment)
    storage.save()
    return jsonify({}), 200

