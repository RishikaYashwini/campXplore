"""
Buildings Routes
Campus building information
"""

from flask import Blueprint, jsonify, request
from models.building import Building
from extensions import db

buildings_bp = Blueprint('buildings', __name__, url_prefix='/api/buildings')


@buildings_bp.route('', methods=['GET'])
def get_all_buildings():
    """Get all campus buildings"""
    try:
        buildings = Building.query.all()

        return jsonify({
            'buildings': [building.to_dict() for building in buildings],
            'total': len(buildings)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch buildings: {str(e)}'}), 500


@buildings_bp.route('/<int:building_id>', methods=['GET'])
def get_building(building_id):
    """Get specific building by ID"""
    try:
        building = Building.query.get(building_id)

        if not building:
            return jsonify({'error': 'Building not found'}), 404

        return jsonify({'building': building.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch building: {str(e)}'}), 500


@buildings_bp.route('/search', methods=['GET'])
def search_buildings():
    """Search buildings by name or code"""
    try:
        query = request.args.get('q', '').strip()

        if not query:
            return jsonify({'error': 'Search query is required'}), 400

        # Search in name or code
        buildings = Building.query.filter(
            db.or_(
                Building.name.ilike(f'%{query}%'),
                Building.code.ilike(f'%{query}%')
            )
        ).all()

        return jsonify({
            'buildings': [building.to_dict() for building in buildings],
            'total': len(buildings),
            'query': query
        }), 200

    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500
