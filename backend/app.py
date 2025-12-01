"""
CampXplore Backend Application
Version 0.1
Main Flask application with all configurations
"""

import os
from flask import Flask, jsonify
from config import get_config
from extensions import db, init_extensions
from sqlalchemy import text
from routes import all_blueprints
from models.waypoint import Waypoint
from flask_cors import CORS

def create_app(config_name='development'):
    """Application factory pattern"""

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(get_config(config_name))

    # --- 🔑 CRITICAL CORS CONFIGURATION ---
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://campxplore.onrender.com') 
    
    # Initialize CORS with credentials support for the /api routes
    CORS(app, resources={r"/api/*": {"origins": FRONTEND_URL, "supports_credentials": True}})
    # -----------------------------------------
    
    # Initialize extensions
    init_extensions(app)

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'name': 'CampXplore API',
            'version': '0.1',
            'status': 'active',
            'endpoints': {
                'auth': '/api/auth',
                'buildings': '/api/buildings',
                'navigation': '/api/navigation',
                'complaints': '/api/complaints',
                'feedback': '/api/feedback',
                'analytics': '/api/analytics'
            }
        }), 200

    # Health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            db_status = f'unhealthy: {str(e)}'

        return jsonify({
            'status': 'running',
            'database': db_status
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Resource not found',
            'status': 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Internal server error',
            'status': 500
        }), 500

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Access forbidden',
            'status': 403
        }), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized access',
            'status': 401
        }), 401

    return app


# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))


# Database initialization
@app.cli.command()
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully!")


@app.cli.command()
def drop_db():
    """Drop all database tables"""
    with app.app_context():
        db.drop_all()
        print("✓ Database tables dropped!")


# Development server
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
