from turtle import update
from colorama import Fore
from flask import Flask, jsonify, request, abort
from models import storage
from models.alumni_group import AlumniGroup
from models.group_member import GroupMember

from api.v1.src.views import app_views




# @app_views.route('/all_group_presidents', methods=['GET'])
# def get_all_group_presidents():
#     """Retrieve all group presidents"""
#     group_presidents = storage.all(President)
#     presidents_list = []
#     for president in group_presidents:
#         president_dict = president.to_dict()
#         president_dict['user'] = president.user.to_dict()
#         president["group"] = president.group.to_dict()
#         presidents_list.append(president_dict)
        
#     return jsonify(presidents_list), 200

@app_views.route('/group_members', methods=['GET'])
def get_all_group_members():
    """Retrieve all group members"""
    group_members = storage.all(GroupMember).values()
    members_list = []
    for member in group_members:
        member_dict = member.to_dict()
        member_dict['user_info'] = member.user_info.to_dict()
        members_list.append(member_dict)
    return jsonify(members_list), 200


@app_views.route('/group_members/<member_id>', methods=['GET'])
def get_group_member(member_id):
    """Retrieve a specific group member by ID"""
    member = storage.get(GroupMember, member_id)
    if member is None:
        abort(404, description="Group member not found")
    member_dict = member.to_dict()
    member_dict['user_info'] = member.user_info.to_dict()
    member_dict["beneficiaries"] = [beneficiary.to_dict() for beneficiary in member.beneficiaries]
    return jsonify(member_dict), 200


@app_views.route('/alumni_groups/<group_id>/members', methods=['POST'], strict_slashes=False)
def create_group_member(group_id):
    """Create a new group member"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['user_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Check if the user is already a member of the group
    all_members = storage.all(GroupMember)
    existing_member = None
    for member in all_members.values():
        if member.user_id == data['user_id'] and member.group_id == group_id:
            existing_member = member
    
    if existing_member is not None:
        abort(400, description=f"{existing_member.user_info.username} is already a member of the group")

    # Create new GroupMember object
    new_member = GroupMember(
        **data,
        group_id=group_id
    )

    new_member.save()

    return jsonify(new_member.to_dict()), 201

@app_views.route('/group_members/<member_id>', methods=['PUT'])
def update_group_member(member_id):
    """Update an existing group member"""
    member = storage.get(GroupMember, member_id)
    if member is None:
        abort(404, description="Group member not found")

    if not request.get_json():
        abort(400, description="Not a JSON")
        
    
    updateable_fields = ['status', 'user_info', 'beneficiaries']
    data = request.get_json()
    print(data)
    for key, value in data.items():
        if key not in updateable_fields:
            abort(400, description="Not a JSON")
        setattr(member, key, value)
    
    if data["status"] == "APPROVED":
        member.set_isApproved()
    storage.save()
    return jsonify(member.to_dict()), 200


@app_views.route('/group_members/<member_id>', methods=['DELETE'])
def delete_group_member(member_id):
    """Delete a group member"""
    member = storage.get(GroupMember, member_id)
    group = storage.get(AlumniGroup, member.group_id)
    print(member.group_id)
    if member is None:
        abort(404, description="Group member not found")
    
    if member.is_president:
        member.handle_president_removal()
    
    storage.delete(member)
    storage.save()
    print(f"{Fore.BLUE} the user is president{group}")
    return jsonify({}), 200

