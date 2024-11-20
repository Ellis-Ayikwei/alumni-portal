from click import FLOAT
from flask import Flask, jsonify, request, abort
from models import storage  # Assuming this is your data layer abstraction
from models.payment import PaymentStatus, Payment

from api.v1.src.views import app_views
@app_views.route('/payments/users_payments/<user_id>', methods=['GET'])
def get_users_payments(user_id):
    """Retrieve all payments made by a user"""
    payments = storage.all(Payment).values()
    users_payments = [payment.to_dict() for payment in payments if payment.payer_id == user_id]
    return jsonify(users_payments), 200


@app_views.route('/payments', methods=['GET'])
def get_all_payments():
    """Retrieve all payments"""
    payments = storage.all(Payment).values()
    payments_list = [payment.to_dict() for payment in payments]
    return jsonify(payments_list), 200


@app_views.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Retrieve a specific payment by ID"""
    payment = storage.get(Payment, payment_id)
    if payment is None:
        abort(404, description="Payment not found")
    return jsonify(payment.to_dict()), 200


@app_views.route('/payments', methods=['POST'])
def create_payment():
    """Create a new payment"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    required_fields = ['amount', 'payment_date', 'payer_id']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    # Create new Payment object
    print(float(data["amount"]))
    
    new_payment = Payment(
        amount=float(data["amount"]),
        payment_date=data['payment_date'],
        status=data.get('status', PaymentStatus.PENDING),
        payer_id=data['payer_id'],
        group_id=data["group_id"],
        payment_method_id=data["payment_method_id"]
    )
    
    new_payment.save()

    # return jsonify(new_payment.to_dict()), 201
    return jsonify({}), 201


@app_views.route('/payments/<payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Update an existing payment"""
    payment = storage.get(Payment, payment_id)
    if payment is None:
        abort(404, description="Payment not found")

    if not request.json:
        abort(400, description="Not a JSON")
    
    
    ignore = ['id', 'created_at', 'updated_at', '__class__', 'payment_method', 'group', 'payer']
    data = request.json
    for key,value in data.items():
        if key not in ignore:
            setattr(payment, key, value)
    storage.save()
    
    return jsonify(payment.to_dict()), 200


@app_views.route('/payments/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Delete a payment"""
    payment = storage.get(Payment, payment_id)
    if payment is None:
        abort(404, description="Payment not found")

    storage.delete(payment)
    storage.save()
    return jsonify({}), 200
