from flask import jsonify, request, abort
from models import storage
from models.meal_plan import MealPlan
from models.coach import Coach
from models.client import Client

from api.v1.src.views import app_views

@app_views.route('/meal_plans', methods=['GET'])
def get_all_meal_plans():
    """Retrieve all meal plans"""
    meal_plans = storage.all(MealPlan).values()
    meal_plans_list = []
    for plan in meal_plans:
        plan_dict = plan.to_dict()
        plan_dict['coach_info'] = plan.coach.to_dict() if plan.coach else None
        plan_dict['client_info'] = plan.client.to_dict() if plan.client else None
        meal_plans_list.append(plan_dict)
    return jsonify(meal_plans_list), 200

@app_views.route('/meal_plans/<plan_id>', methods=['GET'])
def get_meal_plan(plan_id):
    """Retrieve a specific meal plan by ID"""
    plan = storage.get(MealPlan, plan_id)
    if plan is None:
        abort(404, description="Meal plan not found")
    plan_dict = plan.to_dict()
    plan_dict['coach_info'] = plan.coach.to_dict() if plan.coach else None
    plan_dict['client_info'] = plan.client.to_dict() if plan.client else None
    return jsonify(plan_dict), 200

@app_views.route('/meal_plans', methods=['POST'])
def create_meal_plan():
    """Create a new meal plan"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['title', 'coach_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Check if the coach exists
    coach = storage.get(Coach, data['coach_id'])
    if coach is None:
        abort(404, description="Coach not found")

    # Create new MealPlan object
    new_plan = MealPlan(
        **data
    )

    storage.new(new_plan)
    storage.save()

    return jsonify(new_plan.to_dict()), 201

@app_views.route('/meal_plans/<plan_id>', methods=['PUT'])
def update_meal_plan(plan_id):
    """Update an existing meal plan"""
    plan = storage.get(MealPlan, plan_id)
    if plan is None:
        abort(404, description="Meal plan not found")

    if not request.get_json():
        abort(400, description="Not a JSON")
        
    updateable_fields = ['title', 'description', 'client_id']
    data = request.get_json()
    for key, value in data.items():
        if key in updateable_fields:
            setattr(plan, key, value)
    
    storage.save()
    return jsonify(plan.to_dict()), 200

@app_views.route('/meal_plans/<plan_id>', methods=['DELETE'])
def delete_meal_plan(plan_id):
    """Delete a meal plan"""
    plan = storage.get(MealPlan, plan_id)
    if plan is None:
        abort(404, description="Meal plan not found")
    
    storage.delete(plan)
    storage.save()
    return jsonify({}), 200

