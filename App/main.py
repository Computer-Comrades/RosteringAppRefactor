from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    
    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roster.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Initialize extensions
    db.init_app(app)
    
    return app