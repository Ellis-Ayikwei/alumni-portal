from colorama import Fore
from flask import Flask, jsonify, request, abort
from models import storage
from models.alumni_group import AlumniGroup, Status

from api.v1.src.views import app_views
from models.user import GroupMember
@app_views.route('/alumni_groups', methods=['GET'])
def get_all_alumni_groups():
    """Retrieve all alumni groups"""
    alumni_groups = storage.all(AlumniGroup).values()
    alumni_groups_list = []
    for group in alumni_groups:
        group_dict = group.to_dict()
        group_dict['members'] = [member.to_dict() for member in group.members] if group.members else None
        # group_dict['contracts'] = [contract.to_dict() for contract in group.contracts] if group.contracts else None
        group_dict['insurance_package'] = group.insurance_package.to_dict() if group.insurance_package else None
        group_dict['president'] = group.president.to_dict() if group.president else None
        alumni_groups_list.append(group_dict)
    return jsonify(alumni_groups_list), 200


@app_views.route('/alumni_groups/<group_id>', methods=['GET'])
def get_alumni_group(group_id):
    """Retrieve a specific alumni group by ID"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")
    group_dict = alumni_group.to_dict()
    group_dict['members'] = [member.to_dict() for member in alumni_group.members] if alumni_group.members else None
    # group_dict['contract'] = [contract.to_dict() for contract in alumni_group.contracts] if alumni_group.contracts else None
    group_dict['insurance_package'] = alumni_group.insurance_package.to_dict() if alumni_group.insurance_package else None
    group_dict['president'] = alumni_group.president.to_dict() if alumni_group.president else None
    return jsonify(group_dict), 200



@app_views.route('/alumni_groups', methods=['POST'])
def create_alumni_group():
    """Create a new alumni group"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['name', 'start_date', 'end_date']
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
    group = storage.get(AlumniGroup, group_id)
    all_group_members = storage.all(GroupMember).values()

    if group is None:
        abort(404, description="Alumni group not found")

    if not request.get_json():
        abort(400, description="Not a JSON")

    group_data = request.get_json()
    print(group_data)
    group_members  = list(filter(lambda  x: x.group_id == group_id, all_group_members))

    updateable_fields = ['status','name', 'start_date', 'end_date', 'president_user_id', 'package_id', 'description']
    for key, value in group_data.items():
        if key in updateable_fields:
            setattr(group, key, value)
        group.save()
        
    if 'is_president' in group_data and group_data['is_president']:
        grp_membership = storage.get(GroupMember, group_data['id'])
        for member in group_members:
            member.is_president = False
        group.president_user_id = group_data['president_user_id']
        grp_membership.is_president = True
        

    if 'status' in group_data and group_data['status'] in Status.__members__:
        group.status = Status[group_data['status']]

    storage.save()

    return jsonify(group.to_dict()), 200



@app_views.route('/alumni_groups/<group_id>', methods=['DELETE'])
def delete_alumni_group(group_id):
    """Delete an alumni group"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")

    storage.delete(alumni_group)
    storage.save()
    return jsonify({}), 200
