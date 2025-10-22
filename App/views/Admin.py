from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, get_jwt_identity, get_jwt

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')


from App.controllers.auth import jwt_authenticate
# Define your admin routes here

@admin_views.route('/admin/create', methods=['GET'])
def admin_create():
    return render_template('admin/create.html')
