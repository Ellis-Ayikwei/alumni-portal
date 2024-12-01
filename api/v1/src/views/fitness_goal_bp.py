from flask import jsonify, request, abort
from models import storage
from models.fitness_goal import FitnessGoal
from api.v1.src.views import app_views

@app_views.route('/fitness_goals', methods=['GET'])
def get_all_fitness_goals():
    """Retrieve all fitness goals"""
    fitness_goals = storage.all(FitnessGoal).values()
    fitness_goals_list = [goal.to_dict() for goal in fitness_goals]
    return jsonify(fitness_goals_list), 200

@app_views.route('/fitness_goals/<goal_id>', methods=['GET'])
def get_fitness_goal(goal_id):
    """Retrieve a specific fitness goal by ID"""
    fitness_goal = storage.get(FitnessGoal, goal_id)
    if fitness_goal is None:
        abort(404, description="Fitness goal not found")
    return jsonify(fitness_goal.to_dict()), 200

@app_views.route('/fitness_goals', methods=['POST'])
def create_fitness_goal():
    """Create a new fitness goal"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['definition', 'description', 'diet_recommendations', 'goal', 'index', 'workout_recommendations']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    new_fitness_goal = FitnessGoal(**data)
    storage.new(new_fitness_goal)
    storage.save()

    return jsonify(new_fitness_goal.to_dict()), 201

@app_views.route('/fitness_goals/<goal_id>', methods=['PUT'])
def update_fitness_goal(goal_id):
    """Update an existing fitness goal"""
    fitness_goal = storage.get(FitnessGoal, goal_id)
    if fitness_goal is None:
        abort(404, description="Fitness goal not found")

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    updateable_fields = ['definition', 'description', 'diet_recommendations', 'goal', 'index', 'workout_recommendations']
    for key, value in data.items():
        if key in updateable_fields:
            setattr(fitness_goal, key, value)

    storage.save()
    return jsonify(fitness_goal.to_dict()), 200

@app_views.route('/fitness_goals/<goal_id>', methods=['DELETE'])
def delete_fitness_goal(goal_id):
    """Delete a fitness goal"""
    fitness_goal = storage.get(FitnessGoal, goal_id)
    if fitness_goal is None:
        abort(404, description="Fitness goal not found")

    storage.delete(fitness_goal)
    storage.save()
    return jsonify({}), 200

