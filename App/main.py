from flask import Flask
from .database import db
from .controllers.auth import setup_jwt

def create_app():
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roster.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key-here'
    
    # Initialize extensions
    db.init_app(app)
    setup_jwt(app)
    
    # Register blueprints
    from .views.index import index_views
    from .views.auth import auth_views
    from .views.Admin import admin_views
    from .views.Staff import staff_views
    from .views.user import user_views
    
    app.register_blueprint(index_views)
    app.register_blueprint(auth_views)
    app.register_blueprint(admin_views)
    app.register_blueprint(user_views)
    app.register_blueprint(staff_views)

    
    return app