from flask import Flask, jsonify, request, abort
from models import storage
from models.alumni_group import AlumniGroup, Status

from api.v1.src.views import app_views
@app_views.route('/alumni_groups', methods=['GET'])
def get_all_alumni_groups():
    """Retrieve all alumni groups"""
    alumni_groups = storage.all(AlumniGroup).values()
    alumni_groups_list = [group.to_dict() for group in alumni_groups]
    return jsonify(alumni_groups_list), 200


@app_views.route('/alumni_groups/<group_id>', methods=['GET'])
def get_alumni_group(group_id):
    """Retrieve a specific alumni group by ID"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")
    return jsonify(alumni_group.to_dict()), 200


@app_views.route('/alumni_groups', methods=['POST'])
def create_alumni_group():
    """Create a new alumni group"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['name', 'start_date', 'end_date', 'insurance_package']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    
    # Create new AlumniGroup object
    new_group = AlumniGroup(
        name=data['name'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        insurance_package=data['insurance_package'],
        president_id=data.get('president_id'),
        is_locked=data.get('is_locked', False),
        status=Status[data.get('status', 'ACTIVE')]
    )
    
    storage.new(new_group)
    storage.save()

    return jsonify(new_group.to_dict()), 201


@app_views.route('/alumni_groups/<group_id>', methods=['PUT'])
def update_alumni_group(group_id):
    """Update an existing alumni group"""
    alumni_group = storage.get(AlumniGroup, group_id)
    if alumni_group is None:
        abort(404, description="Alumni group not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    data = request.json
    alumni_group.name = data.get('name', alumni_group.name)
    alumni_group.start_date = data.get('start_date', alumni_group.start_date)
    alumni_group.end_date = data.get('end_date', alumni_group.end_date)
    alumni_group.insurance_package = data.get('insurance_package', alumni_group.insurance_package)
    alumni_group.president_id = data.get('president_id', alumni_group.president_id)
    alumni_group.is_locked = data.get('is_locked', alumni_group.is_locked)

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
