"""
Helper Functions
General utility functions
"""

from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    if not filename:
        return False

    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    return '.' in filename and            filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, folder='uploads'):
    """Save uploaded file and return filename"""
    if not file or not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"

    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    return filename


def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return None

    if isinstance(dt, str):
        return dt

    return dt.strftime('%Y-%m-%d %H:%M:%S')


def calculate_walking_time(distance_meters):
    """
    Calculate estimated walking time
    Average walking speed: 75 meters per minute
    """
    if not distance_meters:
        return 0

    walking_speed = 75  # meters per minute
    return int(distance_meters / walking_speed)


def paginate_query(query, page=1, per_page=20):
    """Paginate a SQLAlchemy query"""
    if page < 1:
        page = 1

    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }
