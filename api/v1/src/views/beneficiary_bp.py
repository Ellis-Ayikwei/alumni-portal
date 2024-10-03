from flask import Flask, jsonify, request, abort
from models import storage
from models.beneficiary import Beneficiary

from api.v1.src.views import app_views
@app_views.route('/beneficiaries', methods=['GET'])
def get_all_beneficiaries():
    """Retrieve all beneficiaries"""
    beneficiaries = storage.all(Beneficiary).values()
    beneficiaries_list = [beneficiary.to_dict() for beneficiary in beneficiaries]
    return jsonify(beneficiaries_list), 200


@app_views.route('/beneficiaries/<beneficiary_id>', methods=['GET'])
def get_beneficiary(beneficiary_id):
    """Retrieve a specific beneficiary by ID"""
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    if beneficiary is None:
        abort(404, description="Beneficiary not found")
    return jsonify(beneficiary.to_dict()), 200


@app_views.route('/beneficiaries', methods=['POST'])
def create_beneficiary():
    """Create a new beneficiary"""
    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    required_fields = ['first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    
    new_beneficiary = Beneficiary(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=data.get('date_of_birth'),
        relationship_type=data.get('relationship_type'),
        member_id=data.get('member_id')
    )
    storage.new(new_beneficiary)
    storage.save()

    return jsonify(new_beneficiary.to_dict()), 201


@app_views.route('/beneficiaries/<beneficiary_id>', methods=['PUT'])
def update_beneficiary(beneficiary_id):
    """Update an existing beneficiary"""
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    if beneficiary is None:
        abort(404, description="Beneficiary not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    beneficiary.first_name = data.get('first_name', beneficiary.first_name)
    beneficiary.last_name = data.get('last_name', beneficiary.last_name)
    beneficiary.date_of_birth = data.get('date_of_birth', beneficiary.date_of_birth)
    beneficiary.relationship_type = data.get('relationship_type', beneficiary.relationship_type)

    storage.save()
    return jsonify(beneficiary.to_dict()), 200


@app_views.route('/beneficiaries/<beneficiary_id>', methods=['DELETE'])
def delete_beneficiary(beneficiary_id):
    """Delete a beneficiary"""
    beneficiary = storage.get(Beneficiary, beneficiary_id)
    if beneficiary is None:
        abort(404, description="Beneficiary not found")

    storage.delete(beneficiary)
    storage.save()
    return jsonify({}), 200
