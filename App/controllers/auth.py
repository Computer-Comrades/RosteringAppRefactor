from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import User, Staff, Admin


def authenticate(username, password):
    staff = Staff.query.filter_by(username=username).first()
    if staff and staff.check_password(password):
        return staff
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        return admin
    return None

def jwt_authenticate(username, password):
    user = User.query.filter_by(username=username).one_or_none()
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt