from flask import Flask, jsonify, request, abort
from models import storage
from models.group_member import GroupMember

from api.v1.src.views import app_views
@app_views.route('/group_members', methods=['GET'])
def get_all_group_members():
    """Retrieve all group members"""
    group_members = storage.all(GroupMember).values()
    members_list = [member.to_dict() for member in group_members]
    return jsonify(members_list), 200


@app_views.route('/group_members/<member_id>', methods=['GET'])
def get_group_member(member_id):
    """Retrieve a specific group member by ID"""
    member = storage.get(GroupMember, member_id)
    if member is None:
        abort(404, description="Group member not found")
    return jsonify(member.to_dict()), 200


@app_views.route('/group_members', methods=['POST'])
def create_group_member():
    """Create a new group member"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['first_name', 'last_name', 'email', 'added_by', 'Alumni_group_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create new GroupMember object
    new_member = GroupMember(
        first_name=data['first_name'],
        last_name=data['last_name'],
        middle_names=data.get('middle_names'),
        gender=data.get('gender'),
        cellphone=data.get('cellphone'),
        date_of_birth=data.get('date_of_birth'),
        is_validated=data.get('is_validated', False),
        added_by=data['added_by'],
        email=data['email'],
        Alumni_group_id=data['Alumni_group_id']
    )

    storage.new(new_member)
    storage.save()

    return jsonify(new_member.to_dict()), 201


@app_views.route('/group_members/<member_id>', methods=['PUT'])
def update_group_member(member_id):
    """Update an existing group member"""
    member = storage.get(GroupMember, member_id)
    if member is None:
        abort(404, description="Group member not found")

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    member.first_name = data.get('first_name', member.first_name)
    member.last_name = data.get('last_name', member.last_name)
    member.middle_names = data.get('middle_names', member.middle_names)
    member.gender = data.get('gender', member.gender)
    member.cellphone = data.get('cellphone', member.cellphone)
    member.date_of_birth = data.get('date_of_birth', member.date_of_birth)
    member.is_validated = data.get('is_validated', member.is_validated)
    member.added_by = data.get('added_by', member.added_by)
    member.email = data.get('email', member.email)
    member.Alumni_group_id = data.get('Alumni_group_id', member.Alumni_group_id)

    storage.save()
    return jsonify(member.to_dict()), 200


@app_views.route('/group_members/<member_id>', methods=['DELETE'])
def delete_group_member(member_id):
    """Delete a group member"""
    member = storage.get(GroupMember, member_id)
    if member is None:
        abort(404, description="Group member not found")

    storage.delete(member)
    storage.save()
    return jsonify({}), 200

