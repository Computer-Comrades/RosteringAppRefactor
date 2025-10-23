from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt
from functools import wraps
#from App.controllers.admin import create_shift as controller_create_shift
from App.controllers.admin import schedule_shifts, view_shift_report
admin_views = Blueprint('admin_views', __name__, template_folder='../templates')



from App.controllers.auth import jwt_authenticate
# Define your admin routes here

# Custom decorator to check if user is admin
# def admin_required():
#     def wrapper(fn):
#         @wraps(fn)
#         @jwt_required()
#         def decorator(*args, **kwargs):
#             # current_user is loaded via the user_lookup_callback in auth.py
#             if current_user.position != 'admin':
#                 return jsonify(message='Admin access required'), 403
#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper

@admin_views.route('/admin/create-shift', methods=['POST'])
def create_shift():
    data = request.get_json()
    staff_id = data.get('staff_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    shift = schedule_shifts(staff_id, date, start_time, end_time)
    if shift:
        return jsonify(message='Shift created successfully'), 201
    return jsonify(message='Shift creation failed'), 400

@admin_views.route('/admin/view-shift', methods=['GET'])
#@admin_required()
def view_report():
    report = view_shift_report()
    #return [a.get_json() for a in Attendance.query.all()]
    if report:
        return jsonify(report=report), 200
    return jsonify(message='No report available'), 404

