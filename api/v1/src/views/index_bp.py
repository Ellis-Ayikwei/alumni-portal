#!/usr/bin/python3
"""the blue print for the index"""
from flask import Flask, jsonify, render_template
from api.v1.src.views import app_views
from models import storage


@app_views.route("/status")
def status():
    """to check the status of the api"""
    return jsonify({'status' : 'ok you are connected to sprout collab1 api'})

@app_views.route("/home")
def home():
    """"the home route """
    return render_template("index.html")

@app_views.route("/stats")
def storage_counts():
    '''
        return counts of all classes in storage
    '''
    cls_counts = {
        "Users": storage.count("User"),
        "Beneficiaries": storage.count("Beneficiary"),
        "Alumin Groups": storage.count("AlumniGroup"),
        "GroupMembers": storage.count("GroupMember"),
        "Amendments": storage.count("Amendment"),
        "Contracts": storage.count("Contract"),
        "Paymemts" : storage.count("Payment")

    }
    return jsonify(cls_counts)
