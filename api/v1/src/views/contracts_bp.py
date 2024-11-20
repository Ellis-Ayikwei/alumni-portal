from flask import Flask, json, jsonify, request, abort
from models import storage, user
from models.contract import Contract
from models.contract import Status as ContractStatus

from api.v1.src.views import app_views
from models.contract_member import ContractMember
@app_views.route('/contracts/my_contracts/<string:user_id>', methods=['GET'])
def get_contracts_for_user(user_id: str) -> tuple[list[dict], int]:
    """Retrieve all contracts for a user

    Args:
        user_id (str): The ID of the user

    Returns:
        tuple[list[dict], int]: A list of contracts and a status code
    """
    all_contract_members = storage.all(ContractMember).values()
    user_contracts_memberships: list[ContractMember] = [contract_member for contract_member in all_contract_members if contract_member.user_id == user_id]

    user_contracts: list[dict] = [c.contract for c in user_contracts_memberships]
    contracts_list: list[dict] = []
    for contract in user_contracts:
        print(contract.name)
        contracts_list.append({
            "name": contract.name,
            "id": contract.id,
            "group": contract.group.name,
            "signed_date": contract.signed_date,
            "underwriter": contract.underwriter.full_name if contract.underwriter else None,
        })

    return jsonify(contracts_list), 200



@app_views.route('/contracts', methods=['GET'])
def get_all_contracts():
    """Retrieve all contracts"""
    contracts = storage.all(Contract).values()
    contracts_list = []
    for contract in contracts:
        contract_dict = contract.to_dict()
        contract_dict["insurance_package"] = contract.insurance_package.to_dict()
        contract_dict["underwriter"] = contract.underwriter.to_dict() if contract.underwriter else None
        contracts_list.append(contract_dict)
    
    # print("--c-c-c--c-c-"*10)
    # print(json.dumps(contracts_list[0], indent=4))
    return jsonify(contracts_list), 200


@app_views.route('/contracts/<contract_id>', methods=['GET'])
def get_contract_by_id(contract_id):
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
    print(data)
    required_fields = ['group_id', 'expiry_date', 'signed_date', 'status', 'underwriter_id', 'insurance_package_id']
    for field in required_fields:
        if field not in data:
            # if field == "underwriter_id":
            #     underwriter_data[field]
            abort(400, description=f"Missing {field}")

    # Create new Contract object
    new_contract = Contract(
       **data
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

    if not request.get_json():
        abort(400, description="Not a JSON")
    
    contract_data = request.get_json()

    updateable_fields = ['group_id', 'expiry_date', 'signed_date', 'status', 'underwriter_id', 'insurance_package_id']
    for key, value in contract_data.items():
        if key in updateable_fields:
            setattr(contract, key, value)
        contract.save()

    if 'status' in contract_data and contract_data['status'] in ContractStatus.__members__:
        contract.status = contract_data['status']
        if contract.status == "LOCKED":
            contract.lock_contract()

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
