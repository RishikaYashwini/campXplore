"""
Configuration Settings for CampXplore
Version 0.1 - Basic Configuration
"""

import os
from datetime import timedelta


class Config:
    """Base configuration"""

    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or         'postgresql://campxplore_user:campxplore_pass@localhost:5432/campxplore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for debugging SQL queries

    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Pagination
    ITEMS_PER_PAGE = 20

    # Application settings
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # In production, always set SECRET_KEY via environment variable
    # === SESSION/COOKIE FIX FOR DEPLOYMENT ===
    # 1. Forces cookie to be sent only over HTTPS (Render uses HTTPS)
    SESSION_COOKIE_SECURE = True 

    # 2. Helps mitigate CSRF; 'Lax' allows cookie sending during cross-site top-level navigation,
    #    which is crucial for APIs hosted on a separate subdomain from the frontend.
    SESSION_COOKIE_SAMESITE = 'Lax' 
    
    # 3. Prevents client-side JS from accessing the cookie (security standard)
    SESSION_COOKIE_HTTPONLY = True 
    
    # 4. Optional: Give the session cookie a unique name
    SESSION_COOKIE_NAME = 'campXploreSession' 

    # Database URL is read from environment variables, not hardcoded here
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://campxplore_user:campxplore_pass@localhost:5432/campxplore_test'


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name='default'):
    """Get configuration by name"""
    return config_by_name.get(config_name, DevelopmentConfig)
