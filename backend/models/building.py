"""
Building Model
Represents campus buildings and their details
"""

from datetime import datetime
from extensions import db


class Building(db.Model):
    """Building model for campus locations"""

    __tablename__ = 'buildings'

    building_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    description = db.Column(db.Text)
    floor_count = db.Column(db.Integer, default=1)
    facilities = db.Column(db.JSON)  # List of facilities
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    complaints = db.relationship('Complaint', backref='building', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='building', lazy='dynamic')

    def to_dict(self):
        """Convert building object to dictionary"""
        return {
            'building_id': self.building_id,
            'name': self.name,
            'code': self.code,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'description': self.description,
            'floor_count': self.floor_count,
            'facilities': self.facilities or [],
            'image_url': self.image_url
        }

    def __repr__(self):
        return f'<Building {self.name}>'
