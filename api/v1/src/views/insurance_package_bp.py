from colorama import Fore
from flask import Flask, jsonify, request, abort
from sqlalchemy import values
from models import storage
from models.benefit import Benefit
from models.insurance_package import InsurancePackage, PaymentFrequency

from api.v1.src.views import app_views

# @app.route('/payment-frequencies', methods=['GET'])
# def get_payment_frequencies():
#     """Retrieve all payment frequencies supported"""
#     # Create a dictionary with payment frequencies
#     frequencies = {freq.name: freq.value for freq in PaymentFrequency}
#     return jsonify(frequencies)

@app_views.route('/insurance_packages', methods=['GET'], strict_slashes=False)
def get_all_insurance_packages():
    """Retrieve all insurance packages"""
    insurance_packages = storage.all(InsurancePackage).values()
    insurance_packages_list = []
    for package in insurance_packages:
        package_dict = package.to_dict()
        benefits_list = []
        for benefit in package.benefits:
            benefits_list.append(benefit.to_dict())
        package_dict["benefits"] = benefits_list
        package_dict["groups"] = [group.to_dict() for group in package.groups]
        insurance_packages_list.append(package_dict)
    return jsonify(insurance_packages_list), 200


@app_views.route('/insurance_packages/<package_id>', methods=['GET'])
def get_insurance_package_by_id(package_id):
    """Retrieve a specific insurance package by ID"""
    package = storage.get(InsurancePackage, package_id)
    if package is None:
        abort(404, description="Insurance package not found")

    return jsonify(package.to_dict()), 200


@app_views.route('/insurance_packages', methods=['POST'])
def create_insurance_package():
    """Create a new insurance package"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    print(f"{Fore.LIGHTYELLOW_EX}the data from the package upload is {data}")
    # required_fields = ['name', 'description', 'sum_assured', 'monthly_premium_ghs', 'annual_premium_ghs']
    # for field in required_fields:
    #     if field not in data:
    #         abort(400, description=f"Missing {field}")

    new_package = InsurancePackage(**data)
    new_package.save()
    for key,value in data['bnfs'].items():
        new_benefit = Benefit(
                    name = key,
                    package_id = new_package.id,
                    premium_payable = value
                    )
        new_benefit.save()

    return jsonify(new_package.to_dict()), 201


@app_views.route('/insurance_packages/<package_id>', methods=['PUT'])
def update_insurance_package(package_id):
    """Update an existing insurance package"""
    insurance_package = storage.get(InsurancePackage, package_id)
    if insurance_package is None:
        abort(404, description="Insurance package not found")

    if not request.get_json():
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at', '__class__', 'benefits', 'groups', 'package_id']
    print(f"{Fore.RED} - {data}")
    for key, value in data.items():
        if key not in ignore:
            setattr(insurance_package, key, value)
    if 'benefits' in data:
        for bene in data['benefits']:
            benefit = storage.get(Benefit, bene["id"])
            if benefit is None:
                continue
            for key, value in bene.items():
                if key not in ignore:
                    setattr(benefit, key, value)
            benefit.save()
    storage.save()
    return jsonify(insurance_package.to_dict()), 200


@app_views.route('/insurance_packages/<package_id>', methods=['DELETE'])
def delete_insurance_package(package_id):
    """Delete an insurance package"""
    package = storage.get(InsurancePackage, package_id)
    if package is None:
        abort(404, description="Insurance package not found")

    storage.delete(package)
    storage.save()
    return jsonify({}), 200

