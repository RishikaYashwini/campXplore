"""
Path Model
Represents walking paths between buildings
"""

from models.waypoint import Waypoint
from datetime import datetime
from extensions import db


class Path(db.Model):
    """Path model for navigation between buildings"""

    __tablename__ = 'paths'

    path_id = db.Column(db.Integer, primary_key=True)
    source_building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=True)
    destination_building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'), nullable=True)
    source_waypoint_id = db.Column(db.Integer, db.ForeignKey('waypoints.waypoint_id'), nullable=True)
    destination_waypoint_id = db.Column(db.Integer, db.ForeignKey('waypoints.waypoint_id'), nullable=True)
    distance = db.Column(db.Numeric(8, 2), nullable=False)  # Distance in meters
    estimated_time = db.Column(db.Integer)  # Time in minutes
    path_type = db.Column(db.String(20), default='walkway')  # walkway, road, stairs, elevator
    accessibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    source = db.relationship('Building', foreign_keys=[source_building_id])
    destination = db.relationship('Building', foreign_keys=[destination_building_id])
    source_waypoint = db.relationship('Waypoint', foreign_keys=[source_waypoint_id])
    destination_waypoint = db.relationship('Waypoint', foreign_keys=[destination_waypoint_id])
    
    def to_dict(self):
        """Convert path object to dictionary"""
        return {
            'path_id': self.path_id,
            'source_building_id': self.source_building_id,
            'source_waypoint_id': self.source_waypoint_id,
            'destination_building_id': self.destination_building_id,
            'destination_waypoint_id': self.destination_waypoint_id,
            'distance': float(self.distance),
            'estimated_time': self.estimated_time,
            'path_type': self.path_type,
            'accessibility': self.accessibility
        }

    def __repr__(self):
        return f'<Path {self.source_building_id} -> {self.destination_building_id}>'
