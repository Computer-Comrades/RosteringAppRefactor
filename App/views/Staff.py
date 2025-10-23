from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt
from App.controllers.shifts import get_shift
from App.controllers.attendance import staff_in, staff_out
from App.models.staff import Staff

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

# Define your staff routes here

@staff_views.route('/api/attnd', methods=['POST'])
@jwt_required()
def clock_in():
    # Verify that the current user is a staff member
    if not current_user or not isinstance(current_user, Staff):
        return jsonify(message='Unauthorized. Staff access required.'), 403
    
    data = request.get_json()
    shift_id = data.get('shift_id')
    
    if not shift_id:
        return jsonify(message='Shift ID is required'), 400
    
    # Call the controller function to handle clock-in
    result = staff_in(current_user.username, shift_id)
    if result:
        return jsonify(message='Clock-in successful'), 200
    return jsonify(message='Clock-in failed'), 400

@staff_views.route('/api/attnd-out', methods=['POST'])
@jwt_required()
def clock_out():    
    # Verify that the current user is a staff member
    if not current_user or not isinstance(current_user, Staff):
        return jsonify(message='Unauthorized. Staff access required.'), 403
    
    data = request.get_json()
    shift_id = data.get('shift_id')
    
    if not shift_id:
        return jsonify(message='Shift ID is required'), 400
    
    # Call the controller function to handle clock-out
    result = staff_out(current_user.username, shift_id)
    if result:
        return jsonify(message='Clock-out successful'), 200
    return jsonify(message='Clock-out failed'), 400

@staff_views.route('/api/staffschedule', methods=['GET'])
@jwt_required()
def view_staff_schedule():
    schedule= get_shift()
    if schedule:
        return jsonify(message=schedule), 200
    return jsonify(message='No shifts available'), 404