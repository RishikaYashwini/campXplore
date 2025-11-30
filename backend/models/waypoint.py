"""
Waypoint Model - Navigation Waypoints
Location: backend/models/waypoint.py
"""

from extensions import db
from datetime import datetime

class Waypoint(db.Model):
    """
    Waypoint model representing path intersections and key points on campus
    Used for realistic navigation routing
    """
    __tablename__ = 'waypoints'

    waypoint_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    waypoint_type = db.Column(db.String(50), nullable=False)  # intersection, entrance, junction
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Waypoint {self.name}>'

    def to_dict(self):
        return {
            'waypoint_id': self.waypoint_id,
            'name': self.name,
            'code': self.code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'waypoint_type': self.waypoint_type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
