"""
Feedback Model
Handles user feedback and facility ratings
"""

from datetime import datetime
from extensions import db


class Feedback(db.Model):
    """Feedback model for facility ratings and comments"""

    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    facility = db.Column(db.String(100), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.building_id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comments = db.Column(db.Text)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, include_user=False):
        """Convert feedback object to dictionary"""
        data = {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'facility': self.facility,
            'building_id': self.building_id,
            'rating': self.rating,
            'comments': self.comments,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_user and self.user:
            data['user_name'] = self.user.name

        if self.building:
            data['building_name'] = self.building.name

        return data

    def __repr__(self):
        return f'<Feedback {self.feedback_id}: {self.facility} - {self.rating}★>'
