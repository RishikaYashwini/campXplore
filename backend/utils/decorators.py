"""
Decorator Functions
Authentication and authorization decorators
"""

from functools import wraps
from flask import session, jsonify


def login_required(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this resource'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this resource'
            }), 401

        if session.get('user_role') != 'admin':
            return jsonify({
                'error': 'Admin access required',
                'message': 'You do not have permission to access this resource'
            }), 403

        return f(*args, **kwargs)
    return decorated_function


def optional_login(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Just pass through, check session in route if needed
        return f(*args, **kwargs)
    return decorated_function
