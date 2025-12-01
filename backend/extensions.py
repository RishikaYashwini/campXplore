"""
Flask Extensions
Centralized extension initialization
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
cors = CORS()


def init_extensions(app):
    """Initialize Flask extensions with app instance"""
    db.init_app(app)
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    cors.init_app(app, supports_credentials=True, origins=CORS_ALLOWED_ORIGINS)

    return app
