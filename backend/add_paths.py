
from app import app
from extensions import db
from models.waypoint import Waypoint
from models.path import Path

with app.app_context():
    # Get waypoints
    waypoints = {wp.code: wp.waypoint_id for wp in Waypoint.query.all()}

    # Define paths
    paths_data = [
        ('waypoint', 'WP-GATE', 'waypoint', 'WP-ADMIN', 50, 1),
        ('building', 1, 'waypoint', 'WP-ADMIN', 30, 1),
        ('waypoint', 'WP-ADMIN', 'waypoint', 'WP-PLAZA', 40, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-ACADEMIC', 45, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-LIB-PATH', 60, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-CAF', 55, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-AUD', 35, 1),
        ('building', 2, 'waypoint', 'WP-LIB-PATH', 25, 1),
        ('waypoint', 'WP-LIB-PATH', 'waypoint', 'WP-CAF', 40, 1),
        ('waypoint', 'WP-LIB-PATH', 'waypoint', 'WP-NORTH', 50, 1),
        ('waypoint', 'WP-ACADEMIC', 'building', 4, 35, 1),
        ('waypoint', 'WP-ACADEMIC', 'building', 5, 30, 1),
        ('waypoint', 'WP-ACADEMIC', 'waypoint', 'WP-ENGG', 40, 1),
        ('building', 3, 'waypoint', 'WP-ENGG', 35, 1),
        ('waypoint', 'WP-ENGG', 'waypoint', 'WP-RD', 45, 1),
        ('building', 6, 'waypoint', 'WP-CAF', 20, 1),
        ('waypoint', 'WP-CAF', 'waypoint', 'WP-HOSTEL', 60, 1),
        ('building', 7, 'waypoint', 'WP-SPORTS', 25, 1),
        ('waypoint', 'WP-SPORTS', 'waypoint', 'WP-HOSTEL', 45, 1),
        ('waypoint', 'WP-SPORTS', 'waypoint', 'WP-NORTH', 35, 1),
        ('building', 8, 'waypoint', 'WP-ENGG', 30, 1),
        ('building', 9, 'waypoint', 'WP-HOSTEL', 30, 1),
        ('building', 10, 'waypoint', 'WP-HOSTEL', 40, 1),
        ('building', 11, 'waypoint', 'WP-AUD', 25, 1),
        ('waypoint', 'WP-AUD', 'waypoint', 'WP-ACADEMIC', 50, 1),
        ('building', 12, 'waypoint', 'WP-RD', 30, 1),
        ('waypoint', 'WP-RD', 'waypoint', 'WP-ENGG', 35, 1),
    ]

    count = 0
    for source_type, source_id, dest_type, dest_id, distance, time in paths_data:
        # Forward path
        if source_type == 'building':
            s_b, s_w = source_id, None
        else:
            s_b, s_w = None, waypoints.get(source_id)

        if dest_type == 'building':
            d_b, d_w = dest_id, None
        else:
            d_b, d_w = None, waypoints.get(dest_id)

        if (s_b or s_w) and (d_b or d_w):
            # Add forward path
            db.session.add(Path(
                source_building_id=s_b,
                source_waypoint_id=s_w,
                destination_building_id=d_b,
                destination_waypoint_id=d_w,
                distance=distance,
                estimated_time=time
            ))

            # Add reverse path
            db.session.add(Path(
                source_building_id=d_b,
                source_waypoint_id=d_w,
                destination_building_id=s_b,
                destination_waypoint_id=s_w,
                distance=distance,
                estimated_time=time
            ))
            count += 2

    db.session.commit()
    print(f"✓ Added {count} paths!")
