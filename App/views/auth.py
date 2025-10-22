from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt

from.index import index_views

from App.controllers.auth import jwt_authenticate

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        access_token = jwt_authenticate(username, password)
        if access_token:
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message='Invalid credentials'), 401
        