"""
Complaints Routes
Issue tracking and complaint management
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models.complaint import Complaint
from models.user import User
from extensions import db
from utils.decorators import login_required, admin_required
from utils.validators import validate_priority, validate_category, sanitize_input

complaints_bp = Blueprint('complaints', __name__, url_prefix='/api/complaints')

# Valid complaint categories
COMPLAINT_CATEGORIES = [
    'Infrastructure', 'Maintenance', 'Safety', 'Cleanliness',
    'Technology', 'Transportation', 'Food Services', 'Other'
]


@complaints_bp.route('', methods=['GET'])
@login_required
def get_complaints():
    """
    Get complaints (user's own or all for admin)
    Query params: status, category, priority, page, per_page
    """
    try:
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        # Base query
        if user_role == 'admin':
            query = Complaint.query
        else:
            query = Complaint.query.filter_by(user_id=user_id)

        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)

        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)

        priority = request.args.get('priority')
        if priority:
            query = query.filter_by(priority=priority)

        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')

        if sort_order == 'desc':
            query = query.order_by(getattr(Complaint, sort_by).desc())
        else:
            query = query.order_by(getattr(Complaint, sort_by).asc())

        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        complaints = [c.to_dict(include_user=(user_role == 'admin')) for c in paginated.items]

        return jsonify({
            'complaints': complaints,
            'total': paginated.total,
            'page': page,
            'per_page': per_page,
            'pages': paginated.pages
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch complaints: {str(e)}'}), 500


@complaints_bp.route('/<int:complaint_id>', methods=['GET'])
@login_required
def get_complaint(complaint_id):
    """Get specific complaint by ID"""
    try:
        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404

        # Check authorization (user can only see their own, admin can see all)
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role != 'admin' and complaint.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403

        return jsonify({
            'complaint': complaint.to_dict(include_user=(user_role == 'admin'))
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch complaint: {str(e)}'}), 500


@complaints_bp.route('', methods=['POST'])
@login_required
def create_complaint():
    """Submit a new complaint"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract and validate fields
        title = sanitize_input(data.get('title', ''), max_length=200)
        description = sanitize_input(data.get('description', ''))
        category = data.get('category', '')
        priority = data.get('priority', 'medium').lower()
        building_id = data.get('building_id')
        location_details = sanitize_input(data.get('location_details', ''), max_length=200)

        # Validations
        if not title:
            return jsonify({'error': 'Title is required'}), 400

        if not description:
            return jsonify({'error': 'Description is required'}), 400

        valid_category, category_msg = validate_category(category, COMPLAINT_CATEGORIES)
        if not valid_category:
            return jsonify({'error': category_msg}), 400

        valid_priority, priority_msg = validate_priority(priority)
        if not valid_priority:
            return jsonify({'error': priority_msg}), 400

        # Create complaint
        complaint = Complaint(
            user_id=session['user_id'],
            title=title,
            description=description,
            category=category,
            priority=priority,
            building_id=building_id,
            location_details=location_details
        )

        db.session.add(complaint)
        db.session.commit()

        return jsonify({
            'message': 'Complaint submitted successfully',
            'complaint': complaint.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create complaint: {str(e)}'}), 500


@complaints_bp.route('/<int:complaint_id>', methods=['PUT'])
@admin_required
def update_complaint(complaint_id):
    """Update complaint (admin only)"""
    try:
        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404

        data = request.get_json()

        # Update allowed fields
        if 'status' in data:
            valid_statuses = ['open', 'in_progress', 'resolved', 'closed']
            if data['status'] in valid_statuses:
                complaint.status = data['status']

                # Set resolved timestamp
                if data['status'] == 'resolved' and not complaint.resolved_at:
                    complaint.resolved_at = datetime.utcnow()

        if 'priority' in data:
            valid_priorities = ['low', 'medium', 'high', 'urgent']
            if data['priority'] in valid_priorities:
                complaint.priority = data['priority']

        if 'admin_response' in data:
            complaint.admin_response = sanitize_input(data['admin_response'])

        complaint.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Complaint updated successfully',
            'complaint': complaint.to_dict(include_user=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update complaint: {str(e)}'}), 500


@complaints_bp.route('/<int:complaint_id>', methods=['DELETE'])
@login_required
def delete_complaint(complaint_id):
    """Delete complaint (own complaints or admin)"""
    try:
        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404

        # Check authorization
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_role != 'admin' and complaint.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403

        db.session.delete(complaint)
        db.session.commit()

        return jsonify({'message': 'Complaint deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete complaint: {str(e)}'}), 500


@complaints_bp.route('/stats', methods=['GET'])
@login_required
def get_complaint_stats():
    """Get complaint statistics for current user"""
    try:
        user_id = session.get('user_id')

        total = Complaint.query.filter_by(user_id=user_id).count()
        open_count = Complaint.query.filter_by(user_id=user_id, status='open').count()
        in_progress = Complaint.query.filter_by(user_id=user_id, status='in_progress').count()
        resolved = Complaint.query.filter_by(user_id=user_id, status='resolved').count()

        return jsonify({
            'total': total,
            'open': open_count,
            'in_progress': in_progress,
            'resolved': resolved,
            'closed': total - open_count - in_progress - resolved
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500
