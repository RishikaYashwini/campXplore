"""
Routes Package
API endpoint blueprints for CampXplore
Version 0.1
"""

from .auth import auth_bp
from .buildings import buildings_bp
from .navigation import navigation_bp
from .complaints import complaints_bp
from .feedback import feedback_bp
from .analytics import analytics_bp

# List of all blueprints to be registered in main app
all_blueprints = [
    auth_bp,
    buildings_bp,
    navigation_bp,
    complaints_bp,
    feedback_bp,
    analytics_bp
]

__all__ = [
    'all_blueprints',
    'auth_bp',
    'buildings_bp',
    'navigation_bp',
    'complaints_bp',
    'feedback_bp',
    'analytics_bp'
]
