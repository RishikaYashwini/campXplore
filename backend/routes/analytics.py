"""
Analytics Routes - Fixed for Session-Based Authentication
Location: backend/routes/analytics.py
"""

from flask import Blueprint, jsonify, session
from extensions import db
from models.user import User
from models.complaint import Complaint
from models.feedback import Feedback
from models.building import Building
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

def login_required(f):
    """Custom decorator for session-based authentication"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@analytics_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get comprehensive dashboard statistics for admin panel"""
    try:
        # Check if user is admin
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        # User statistics
        total_users = User.query.count()
        students = User.query.filter_by(role='student').count()
        faculty = User.query.filter_by(role='faculty').count()
        admins = User.query.filter_by(role='admin').count()

        # Complaint statistics
        total_complaints = Complaint.query.count()
        open_complaints = Complaint.query.filter_by(status='open').count()
        in_progress_complaints = Complaint.query.filter_by(status='in_progress').count()
        resolved_complaints = Complaint.query.filter_by(status='resolved').count()
        closed_complaints = Complaint.query.filter_by(status='closed').count()

        # Complaint categories breakdown
        category_query = db.session.query(
            Complaint.category,
            func.count(Complaint.complaint_id).label('count')
        ).group_by(Complaint.category).all()

        complaint_categories = {category: count for category, count in category_query}

        # Feedback statistics
        total_feedback = Feedback.query.count()
        avg_rating_result = db.session.query(func.avg(Feedback.rating)).scalar()
        average_rating = float(avg_rating_result) if avg_rating_result else 0.0

        # Buildings count
        total_buildings = Building.query.count()

        dashboard_data = {
            'total_users': total_users,
            'students': students,
            'faculty': faculty,
            'admins': admins,
            'total_complaints': total_complaints,
            'open_complaints': open_complaints,
            'in_progress_complaints': in_progress_complaints,
            'resolved_complaints': resolved_complaints,
            'closed_complaints': closed_complaints,
            'complaint_categories': complaint_categories,
            'total_feedback': total_feedback,
            'average_rating': round(average_rating, 2),
            'total_buildings': total_buildings
        }

        return jsonify(dashboard_data), 200

    except Exception as e:
        print(f"Error in dashboard stats: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ✨ NEW: Complaints Analytics Endpoint
@analytics_bp.route('/complaints', methods=['GET'])
@login_required
def get_complaint_analytics():
    """Get detailed complaint analytics for charts"""
    try:
        # Check if user is admin
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        # Complaint statistics by status
        total_complaints = Complaint.query.count()
        open_complaints = Complaint.query.filter_by(status='open').count()
        in_progress_complaints = Complaint.query.filter_by(status='in_progress').count()
        resolved_complaints = Complaint.query.filter_by(status='resolved').count()
        closed_complaints = Complaint.query.filter_by(status='closed').count()

        # Complaint statistics by priority
        high_priority_complaints = Complaint.query.filter_by(priority='high').count()
        medium_priority_complaints = Complaint.query.filter_by(priority='medium').count()
        low_priority_complaints = Complaint.query.filter_by(priority='low').count()

        # Complaint categories breakdown
        category_query = db.session.query(
            Complaint.category,
            func.count(Complaint.complaint_id).label('count')
        ).group_by(Complaint.category).all()

        complaint_categories = {category: count for category, count in category_query}

        complaint_data = {
            'total_complaints': total_complaints,
            'open_complaints': open_complaints,
            'in_progress_complaints': in_progress_complaints,
            'resolved_complaints': resolved_complaints,
            'closed_complaints': closed_complaints,
            'high_priority_complaints': high_priority_complaints,
            'medium_priority_complaints': medium_priority_complaints,
            'low_priority_complaints': low_priority_complaints,
            'complaint_categories': complaint_categories
        }

        return jsonify(complaint_data), 200

    except Exception as e:
        print(f"Error in complaint analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ✨ NEW: Feedback Analytics Endpoint
@analytics_bp.route('/feedback', methods=['GET'])
@login_required
def get_feedback_analytics():
    """Get detailed feedback analytics for charts"""
    try:
        # Check if user is admin
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        # Feedback statistics
        total_feedback = Feedback.query.count()

        # Ratings breakdown (1-5 stars)
        ratings_1 = Feedback.query.filter_by(rating=1).count()
        ratings_2 = Feedback.query.filter_by(rating=2).count()
        ratings_3 = Feedback.query.filter_by(rating=3).count()
        ratings_4 = Feedback.query.filter_by(rating=4).count()
        ratings_5 = Feedback.query.filter_by(rating=5).count()

        # Calculate average rating
        avg_rating_result = db.session.query(func.avg(Feedback.rating)).scalar()
        average_rating = float(avg_rating_result) if avg_rating_result else 0.0

        # Category breakdown (if your Feedback model has category field)
        try:
            category_query = db.session.query(
                Feedback.category,
                func.count(Feedback.feedback_id).label('count')
            ).group_by(Feedback.category).all()

            feedback_categories = {category: count for category, count in category_query}
        except:
            # If category field doesn't exist, skip this
            feedback_categories = {}

        feedback_data = {
            'total_feedback': total_feedback,
            'average_rating': round(average_rating, 2),
            'ratings_1': ratings_1,
            'ratings_2': ratings_2,
            'ratings_3': ratings_3,
            'ratings_4': ratings_4,
            'ratings_5': ratings_5,
            'feedback_categories': feedback_categories
        }

        return jsonify(feedback_data), 200

    except Exception as e:
        print(f"Error in feedback analytics: {str(e)}")
        return jsonify({'error': str(e)}), 500