import json
from click import group
from colorama import Fore
from flask import Flask, jsonify, request, abort
from models import storage
from models.alumni_group import AlumniGroup, Status

from api.v1.src.views import app_views
from models.invite import Invite
from models.user import GroupMember, User


@app_views.route('/alumni_groups/<group_id>/invite_code', methods=['POST'], strict_slashes=False)
def get_group_invite(group_id):
    """Retrieve an invite code for a user to join a specific group"""
    print("hit the api")
    
    print(request.json)
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    
    print('it is a json')
    
    data = request.get_json()
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404, description="User not found")
   

    invite = Invite(
        group_id=group_id,
        creator_id=user_id,
    )
    generated_invite = invite.generate_code()
    
    return jsonify(generated_invite.to_dict()), 200


@app_views.route('/alumni_groups/my_groups/<user_id>', methods=['GET'])
def get_user_alumni_groups(user_id):
    """Retrieve all alumni groups a user is a part of"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, description="User not found")

    memberships = [{"group_id": membership.group_id} for membership in user.group_memberships]
    memberships_list = []
    for membership in memberships:
        group = storage.get(AlumniGroup, membership["group_id"])
        group_dict = group.to_dict()
        group_dict['members'] = [member.to_dict() for member in group.members]
        if group.president:
            group_dict['president'] = {key: value for key, value in group.president.to_dict().items() if key not in ['groups_as_president', 'group_memberships']}
        memberships_list.append(group_dict)
    return jsonify(memberships_list), 200


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
