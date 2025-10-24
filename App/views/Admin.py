from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt
from functools import wraps
#from App.controllers.admin import create_shift as controller_create_shift
from App.controllers.admin import schedule_shifts, view_shift_report
from App.controllers.shifts import get_shift
from App.models.admin import Admin

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

#from App.controllers.auth import admin_required
# Define your admin routes here


@admin_views.route('/api/shifts', methods=['POST'])
@jwt_required()
def admin_create_shifts():
    # Verify that the current user is an admin
    if not current_user or not isinstance(current_user, Admin):
        return jsonify(message='Unauthorized. Admin access required.'), 403
    
    data = request.get_json()
    staff_id = data.get('staff_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    shift = schedule_shifts(staff_id, date, start_time, end_time)
    if shift:
        return jsonify(message='Shift created successfully'), 201
    return jsonify(message='Shift creation failed'), 400

@admin_views.route('/api/reports', methods=['GET'])
@jwt_required()
def view_report():
    # Verify that the current user is an admin
    if not current_user or not isinstance(current_user, Admin):
        return jsonify(message='Unauthorized. Admin access required.'), 403

    report = view_shift_report()
    if report:
        return jsonify(message=report), 200
    return jsonify(message='No report available'), 404

@admin_views.route('/api/shiftlist', methods=['GET'])
@jwt_required()
def view_shift_list():
    # Verify that the current user is an admin
    if not current_user or not isinstance(current_user, Admin):
        return jsonify(message='Unauthorized. Admin access required.'), 403
    
    schedule= get_shift()
    if schedule:
        return jsonify(message=schedule), 200
    return jsonify(message='No shifts available'), 404

