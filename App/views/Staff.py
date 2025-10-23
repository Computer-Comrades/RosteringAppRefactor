from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt
from App.controllers.user import create_staff
from App.controllers.attendance import staff_in
staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


from App.controllers.auth import jwt_authenticate
# Define your staff routes here

# @staff_views.route('/create-staff', methods=['POST'])
# def create_staff():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     # Call the controller function to create a new staff user
#     staff = create_staff(username, password)
#     if staff:
#         return jsonify(message=f'Staff {username} created successfully'), 201
#     return jsonify(message='Staff creation failed'), 400

@staff_views.route('/staff/clock-in', methods=['POST'])
@jwt_required()
def clock_in():
    data = request.get_json()
    shift_id = data.get('shift_id')
    # current_user is the full user object loaded by user_lookup_callback
    # Call the controller function to handle clock-in
    result = staff_in(current_user.username, shift_id)
    if result:
        return jsonify(message='Clock-in successful'), 200
    return jsonify(message='Clock-in failed'), 400