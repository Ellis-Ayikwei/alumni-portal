from flask import Flask, jsonify, request, abort
from models import storage
from models.alumni_group import AlumniGroup, Status

from api.v1.src.views import app_views
@app_views.route('/alumni_groups', methods=['GET'])
def get_all_alumni_groups():
    """Retrieve all alumni groups"""
    alumni_groups = storage.all(AlumniGroup).values()
    alumni_groups_list = []
    for group in alumni_groups:
        group_dict = group.to_dict()
        group_dict['members'] = [member.to_dict() for member in group.members]
        group_dict['contract'] = [contract.to_dict() for contract in group.contract]
        group_dict['insurance_package'] = group.insurance_package.to_dict()
        group_dict['president'] = group.president.to_dict()
        alumni_groups_list.append(group_dict)
    return jsonify(alumni_groups_list), 200


@app_views.route('/alumni_groups/<group_id>', methods=['GET'])
def get_alumni_group(group_id):
    """Retrieve a specific alumni group by ID"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")
    group_dict = alumni_group.to_dict()
    group_dict['members'] = [member.to_dict() for member in alumni_group.members]
    group_dict['contract'] = [contract.to_dict() for contract in alumni_group.contract]
    group_dict['insurance_package'] = alumni_group.insurance_package.to_dict()
    group_dict['president'] = alumni_group.president.to_dict()
    return jsonify(group_dict), 200



@app_views.route('/alumni_groups', methods=['POST'])
def create_alumni_group():
    """Create a new alumni group"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['name', 'start_date', 'end_date', 'president_user_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    
    # Create new AlumniGroup object
    new_group = AlumniGroup(**data)
    
    new_group.save()

    return jsonify(new_group.to_dict()), 201


@app_views.route('/alumni_groups/<group_id>', methods=['PUT'])
def update_alumni_group(group_id):
    """Update an existing alumni group"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")
    print(request.get_json())
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()

    updateable_fields = ['name', 'start_date', 'end_date', 'president_user_id', 'package_id']
    for key, value in data.items():
        if key in updateable_fields:
            setattr(alumni_group, key, value)
    

    # Update status only if it is in the correct enum format
    if 'status' in data and data['status'] in Status.__members__:
        alumni_group.status = Status[data['status']]
    
    storage.save()
    
    return jsonify(alumni_group.to_dict()), 200


@app_views.route('/alumni_groups/<group_id>', methods=['DELETE'])
def delete_alumni_group(group_id):
    """Delete an alumni group"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")

    storage.delete(alumni_group)
    storage.save()
    return jsonify({}), 200
