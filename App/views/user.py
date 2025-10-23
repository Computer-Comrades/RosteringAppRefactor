from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt

user_views = Blueprint('user_views', __name__, template_folder='../templates')

from App.controllers.auth import login
from App.controllers.user import create_user as controller_create_user, create_admin as controller_create_admin,create_staff as controller_create_staff

@user_views.route('/create-user',methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Call the controller function to create a new user
    user = controller_create_user(username, password)
    if user:
        return jsonify(message=f'User {username} created successfully'), 201
    return jsonify(message='User creation failed'), 400

@user_views.route('/create-admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Call the controller function to create a new admin
    admin = controller_create_admin(username, password)
    if admin:
        return jsonify(message=f'Admin {username} created successfully'), 201
    return jsonify(message='Admin creation failed'), 400

@user_views.route('/create-staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Call the controller function to create a new staff user
    staff = controller_create_staff(username, password)
    if staff:
        return jsonify(message=f'Staff {username} created successfully'), 201
    return jsonify(message='Staff creation failed'), 400