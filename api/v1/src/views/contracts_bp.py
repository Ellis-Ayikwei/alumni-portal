from flask import Flask, jsonify, request, abort
from models import storage
from models.contract import Contract

from api.v1.src.views import app_views
@app_views.route('/contracts', methods=['GET'])
def get_all_contracts():
    """Retrieve all contracts"""
    contracts = storage.all(Contract).values()
    contracts_list = [contract.to_dict() for contract in contracts]
    return jsonify(contracts_list), 200


@app_views.route('/contracts/<contract_id>', methods=['GET'])
def get_contract(contract_id):
    """Retrieve a specific contract by ID"""
    contract = storage.get(Contract, contract_id)
    if contract is None:
        abort(404, description="Contract not found")
    return jsonify(contract.to_dict()), 200


@app_views.route('/contracts', methods=['POST'])
def create_contract():
    """Create a new contract"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['group_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create new Contract object
    new_contract = Contract(
        group_id=data['group_id']
    )
    
    storage.new(new_contract)
    storage.save()

    return jsonify(new_contract.to_dict()), 201


@app_views.route('/contracts/<contract_id>', methods=['PUT'])
def update_contract(contract_id):
    """Update an existing contract"""
    contract = storage.get(Contract, contract_id)
    if contract is None:
        abort(404, description="Contract not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    contract.group_id = data.get('group_id', contract.group_id)

    storage.save()
    return jsonify(contract.to_dict()), 200


@app_views.route('/contracts/<contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    """Delete a contract"""
    contract = storage.get(Contract, contract_id)
    if contract is None:
        abort(404, description="Contract not found")

    storage.delete(contract)
    storage.save()
    return jsonify({}), 200
