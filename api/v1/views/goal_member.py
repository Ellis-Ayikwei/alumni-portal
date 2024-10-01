#!/usr/bin/python3
""" objects that handles all default RestFul API actions for goal_members """
from models.collaboration import Collaboration
from models.goal_member import Goal_member
from models.goal import Goal
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/goals/mygoals/<user_id>', methods=['GET'], strict_slashes=False)
def get_goals_by_user(user_id):
    """
    Retrieves the list of goals that a user is a member of.
    """
    goal_members = storage.all(Goal_member).values()
    goals = storage.all(Goal).values()

    # Filter goal members first to find those related to the user
    user_goal_members = [goal_member for goal_member in goal_members if goal_member.user_id == user_id]

    # Construct the response with goal details and goal member details
    user_goals_info = []
    for goal_member in user_goal_members:
        goal_info = next((goal.to_dict() for goal in goals if goal.id == goal_member.goal_id), None)
        if goal_info:
            goal_member_info = goal_member.to_dict()
            # Combine goal info and goal member info in the response
            user_goals_info.append({
                'goal': goal_info,
                'goal_member': goal_member_info
            })

    return jsonify(user_goals_info)

@app_views.route('goal_members', methods=['GET'],
                 strict_slashes=False)
def get_all_members():
    """
    Retrieves the list of all goal_members objects
    """
    goal_members = storage.all(Goal_member).values()
    if not goal_members:
        abort(404)
    list_goals_m = []
    for goal_m in goal_members:
        list_goals_m.append(goal_m.to_dict())

    return jsonify(list_goals_m)


@app_views.route('/goals/<goal_id>/goal_members', methods=['GET'],
                 strict_slashes=False)
def get_goal_members(goal_id):
    """
    Retrieves the list of all goal_members objects
    of a specific Goal_member, or a specific collaboration
    """
    list_goal_members = []
    goal = storage.get(Goal, goal_id)
    if not goal:
        abort(404)
    for member in goal.members:
        list_goal_members.append(member.to_dict())

    return jsonify(list_goal_members)


# @app_views.route('/goal_members/<collaboration_id>/', methods=['GET'], strict_slashes=False)
# def get_collaboration(collaboration_id):
#     """
#     Retrieves a specific collaboration based on id
#     """
#     collaboration = storage.get(Collaboration, collaboration_id)
#     if not collaboration:
#         abort(404)
#     return jsonify(collaboration.to_dict())


# @app_views.route('/goal_members/<collaboration_id>', methods=['DELETE'], strict_slashes=False)
# def delete_collaboration(collaboration_id):
#     """
#     Deletes a collaboration based on id provided
#     """
#     collaboration = storage.get(Collaboration, collaboration_id)

#     if not collaboration:
#         abort(404)
#     storage.delete(collaboration)
#     storage.save()

#     return make_response(jsonify({}), 200)


# @app_views.route('/goals/<goal_id>/goal_members', methods=['POST'],
#                  strict_slashes=False)
# def post_collaboration(goal_id):
#     """
#     Creates a Collaboration
#     """
    
#     goal = storage.get(Goal_member, goal_id)
#     if not goal:
#         abort(404)
#     if not request.get_json():
#         abort(400, description="Not a JSON")
#     if 'name' not in request.get_json():
#         abort(400, description="Missing name")
   

#     data = request.get_json()
#     instance = Collaboration(**data)
#     instance.goal_id = goal.id
#     instance.save()
#     return make_response(jsonify(instance.to_dict()), 201)


# @app_views.route('/goal_members/<collaboration_id>', methods=['PUT'], strict_slashes=False)
# def put_collaboration(collaboration_id):
#     """
#     Updates a Collaboration
#     """
#     collaboration = storage.get(Collaboration, collaboration_id)
#     if not collaboration:
#         abort(404)

#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     ignore = ['id', 'goal_id', 'created_at', 'updated_at']

#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore:
#             setattr(collaboration, key, value)
#     storage.save()
#     return make_response(jsonify(collaboration.to_dict()), 200)
