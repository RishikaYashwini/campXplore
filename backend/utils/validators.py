"""
Validation Functions
Input validation and sanitization
"""

import re


def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, "Valid email"


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    # Version 0.1 - Basic validation
    # Future: Add complexity requirements
    return True, "Valid password"


def validate_rating(rating):
    """Validate rating value (1-5)"""
    if rating is None:
        return False, "Rating is required"

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"
        return True, "Valid rating"
    except (ValueError, TypeError):
        return False, "Rating must be a number"


def validate_priority(priority):
    """Validate complaint priority"""
    valid_priorities = ['low', 'medium', 'high', 'urgent']
    if priority and priority.lower() not in valid_priorities:
        return False, f"Priority must be one of: {', '.join(valid_priorities)}"
    return True, "Valid priority"


def validate_category(category, valid_categories):
    """Validate category against allowed list"""
    if not category:
        return False, "Category is required"

    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"

    return True, "Valid category"


def sanitize_input(text, max_length=None):
    """Basic input sanitization"""
    if not text:
        return ""

    # Remove leading/trailing whitespace
    text = text.strip()

    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text
