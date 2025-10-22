from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt
from App.controllers.admin import create_shift as controller_create_shift

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')



from App.controllers.auth import jwt_authenticate
# Define your admin routes here

@admin_views.route('/admin/create-shift', methods=['POST'])
def create_shift():
    data = request.get_json()
    staff_id = data.get('staff_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    shift = controller_create_shift(staff_id, date, start_time, end_time)
    if shift:
        return jsonify(message='Shift created successfully'), 201
    return jsonify(message='Shift creation failed'), 400
