"""
Flask Extensions
Centralized extension initialization
"""

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
cors = CORS()


def init_extensions(app):
    """Initialize Flask extensions with app instance"""
    db.init_app(app)
    cors.init_app(app, supports_credentials=True, origins=['http://localhost:3000'])

    return app
