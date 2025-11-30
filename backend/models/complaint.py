"""
Complaint Model
Handles user complaints and feedback issues
"""

from datetime import datetime
from extensions import db


class Complaint(db.Model):
    """Complaint model for issue tracking"""

    __tablename__ = 'complaints'

    complaint_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'))
    location_details = db.Column(db.String(200))
    image_url = db.Column(db.String(255))
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    def to_dict(self, include_user=False):
        """Convert complaint object to dictionary"""
        data = {
            'complaint_id': self.complaint_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'building_id': self.building_id,
            'location_details': self.location_details,
            'image_url': self.image_url,
            'admin_response': self.admin_response,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

        if include_user and self.user:
            data['user_name'] = self.user.name
            data['user_email'] = self.user.email

        if self.building:
            data['building_name'] = self.building.name

        return data

    def __repr__(self):
        return f'<Complaint {self.complaint_id}: {self.title}>'
