from flask import jsonify, request, abort
from models import storage
from api.v1.src.views import app_views
from models.client import Client

@app_views.route('/clients', methods=['GET'])
def get_all_clients():
    """Retrieve all clients"""
    clients = storage.all(Client).values()
    client_list = [client.to_dict() for client in clients]
    return jsonify(client_list), 200

@app_views.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    """Retrieve a specific client by ID"""
    client = storage.get(Client, client_id)
    if client is None:
        abort(404, description="Client not found")
    return jsonify(client.to_dict()), 200

@app_views.route('/clients', methods=['POST'])
def create_client():
    """Create a new client"""
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    required_fields = ['user_id', 'goal']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    new_client = Client(**data)
    new_client.save()
    return jsonify(new_client.to_dict()), 201

@app_views.route('/clients/<client_id>', methods=['PUT'])
def update_client(client_id):
    """Update an existing client"""
    client = storage.get(Client, client_id)
    if client is None:
        abort(404, description="Client not found")
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.json
    updateable_fields = ['goal']
    for key, value in data.items():
        if key in updateable_fields:
            setattr(client, key, value)
    client.save()
    return jsonify(client.to_dict()), 200

@app_views.route('/clients/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Delete a client"""
    client = storage.get(Client, client_id)
    if client is None:
        abort(404, description="Client not found")
    storage.delete(client)
    storage.save()
    return jsonify({}), 200

