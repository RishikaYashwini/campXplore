"""
Feedback Routes
Facility feedback and ratings
"""

from flask import Blueprint, request, jsonify, session
from models.feedback import Feedback
from models.building import Building
from extensions import db
from utils.decorators import login_required
from utils.validators import validate_rating, validate_category, sanitize_input
from sqlalchemy import func

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')

# Valid feedback categories
FEEDBACK_CATEGORIES = [
    'Classroom', 'Library', 'Laboratory', 'Cafeteria',
    'Restroom', 'WiFi', 'Parking', 'Sports Facility', 'Other'
]


@feedback_bp.route('', methods=['GET'])
def get_all_feedback():
    """
    Get all feedback with optional filters
    Query params: building_id, category, min_rating, page, per_page
    """
    try:
        query = Feedback.query

        # Apply filters
        building_id = request.args.get('building_id', type=int)
        if building_id:
            query = query.filter_by(building_id=building_id)

        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)

        min_rating = request.args.get('min_rating', type=int)
        if min_rating:
            query = query.filter(Feedback.rating >= min_rating)

        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')

        if sort_order == 'desc':
            query = query.order_by(getattr(Feedback, sort_by).desc())
        else:
            query = query.order_by(getattr(Feedback, sort_by).asc())

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        feedbacks = [f.to_dict(include_user=False) for f in paginated.items]

        return jsonify({
            'feedback': feedbacks,
            'total': paginated.total,
            'page': page,
            'per_page': per_page,
            'pages': paginated.pages
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch feedback: {str(e)}'}), 500


@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """Get specific feedback by ID"""
    try:
        feedback = Feedback.query.get(feedback_id)

        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404

        return jsonify({'feedback': feedback.to_dict(include_user=True)}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch feedback: {str(e)}'}), 500


@feedback_bp.route('', methods=['POST'])
@login_required
def create_feedback():
    """Submit new feedback"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract and validate fields
        facility = sanitize_input(data.get('facility', ''), max_length=100)
        building_id = data.get('building_id')
        rating = data.get('rating')
        comments = sanitize_input(data.get('comments', ''))
        category = data.get('category', '')

        # Validations
        if not facility:
            return jsonify({'error': 'Facility name is required'}), 400

        valid_rating, rating_msg = validate_rating(rating)
        if not valid_rating:
            return jsonify({'error': rating_msg}), 400

        if category:
            valid_category, category_msg = validate_category(category, FEEDBACK_CATEGORIES)
            if not valid_category:
                return jsonify({'error': category_msg}), 400

        # Validate building exists if provided
        if building_id:
            building = Building.query.get(building_id)
            if not building:
                return jsonify({'error': 'Invalid building ID'}), 400

        # Create feedback
        feedback = Feedback(
            user_id=session['user_id'],
            facility=facility,
            building_id=building_id,
            rating=int(rating),
            comments=comments,
            category=category
        )

        db.session.add(feedback)
        db.session.commit()

        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback': feedback.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create feedback: {str(e)}'}), 500


@feedback_bp.route('/building/<int:building_id>', methods=['GET'])
def get_building_feedback(building_id):
    """Get all feedback for a specific building"""
    try:
        # Check if building exists
        building = Building.query.get(building_id)
        if not building:
            return jsonify({'error': 'Building not found'}), 404

        # Get feedback
        feedbacks = Feedback.query.filter_by(building_id=building_id).order_by(
            Feedback.created_at.desc()
        ).all()

        # Calculate average rating
        avg_rating = db.session.query(func.avg(Feedback.rating)).filter_by(
            building_id=building_id
        ).scalar()

        return jsonify({
            'building': building.to_dict(),
            'feedback': [f.to_dict() for f in feedbacks],
            'total_feedback': len(feedbacks),
            'average_rating': round(float(avg_rating), 2) if avg_rating else 0
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch building feedback: {str(e)}'}), 500


@feedback_bp.route('/my-feedback', methods=['GET'])
@login_required
def get_my_feedback():
    """Get current user's feedback"""
    try:
        user_id = session.get('user_id')

        feedbacks = Feedback.query.filter_by(user_id=user_id).order_by(
            Feedback.created_at.desc()
        ).all()

        return jsonify({
            'feedback': [f.to_dict() for f in feedbacks],
            'total': len(feedbacks)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch feedback: {str(e)}'}), 500


@feedback_bp.route('/summary', methods=['GET'])
def get_feedback_summary():
    """Get overall feedback summary statistics"""
    try:
        # Total feedback count
        total = Feedback.query.count()

        # Average rating overall
        avg_rating = db.session.query(func.avg(Feedback.rating)).scalar()

        # Rating distribution
        rating_dist = db.session.query(
            Feedback.rating,
            func.count(Feedback.feedback_id)
        ).group_by(Feedback.rating).all()

        rating_distribution = {str(rating): count for rating, count in rating_dist}

        # Category distribution
        category_dist = db.session.query(
            Feedback.category,
            func.count(Feedback.feedback_id)
        ).group_by(Feedback.category).all()

        category_distribution = {cat: count for cat, count in category_dist if cat}

        return jsonify({
            'total_feedback': total,
            'average_rating': round(float(avg_rating), 2) if avg_rating else 0,
            'rating_distribution': rating_distribution,
            'category_distribution': category_distribution
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch summary: {str(e)}'}), 500
