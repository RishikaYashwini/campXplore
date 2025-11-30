"""
FIXED Seed Waypoints for Dr. AIT Campus
Location: backend/seed_waypoints.py
"""

from app import app
from extensions import db
from models.waypoint import Waypoint
from models.path import Path

def seed_waypoints():
    """Add waypoints for Dr. AIT campus walking paths"""
    with app.app_context():
        print("\n" + "="*70)
        print("SEEDING DR. AIT CAMPUS WAYPOINTS")
        print("="*70)

        # Check if waypoints already exist
        existing_count = Waypoint.query.count()
        if existing_count > 0:
            print(f"Waypoints already exist ({existing_count} found)")
            print("Adding paths only...")
            add_waypoint_paths()
            return

        waypoints_data = [
            {
                'name': 'Main Gate Entrance',
                'code': 'WP-GATE',
                'latitude': 12.963200,
                'longitude': 77.505500,
                'waypoint_type': 'entrance',
                'description': 'Main entrance gate to Dr. AIT campus'
            },
            {
                'name': 'Admin Junction',
                'code': 'WP-ADMIN',
                'latitude': 12.963600,
                'longitude': 77.505800,
                'waypoint_type': 'junction',
                'description': 'Junction near Administrative Block'
            },
            {
                'name': 'Central Plaza',
                'code': 'WP-PLAZA',
                'latitude': 12.963718,
                'longitude': 77.506037,
                'waypoint_type': 'intersection',
                'description': 'Central plaza - main campus intersection'
            },
            {
                'name': 'Library Path',
                'code': 'WP-LIB-PATH',
                'latitude': 12.964400,
                'longitude': 77.505650,
                'waypoint_type': 'pathway',
                'description': 'Path leading to Central Library'
            },
            {
                'name': 'Academic Block Junction',
                'code': 'WP-ACADEMIC',
                'latitude': 12.963500,
                'longitude': 77.506200,
                'waypoint_type': 'junction',
                'description': 'Junction connecting CSE, ECE, and Civil blocks'
            },
            {
                'name': 'Cafeteria Junction',
                'code': 'WP-CAF',
                'latitude': 12.964300,
                'longitude': 77.505400,
                'waypoint_type': 'junction',
                'description': 'Junction near Student Cafeteria'
            },
            {
                'name': 'Sports Complex Entrance',
                'code': 'WP-SPORTS',
                'latitude': 12.964800,
                'longitude': 77.505900,
                'waypoint_type': 'entrance',
                'description': 'Entrance to Sports Complex'
            },
            {
                'name': 'Hostel Road',
                'code': 'WP-HOSTEL',
                'latitude': 12.965000,
                'longitude': 77.505600,
                'waypoint_type': 'pathway',
                'description': 'Main road to hostel area'
            },
            {
                'name': 'Engineering Block Path',
                'code': 'WP-ENGG',
                'latitude': 12.963900,
                'longitude': 77.506400,
                'waypoint_type': 'pathway',
                'description': 'Path connecting engineering blocks'
            },
            {
                'name': 'North Gate',
                'code': 'WP-NORTH',
                'latitude': 12.964900,
                'longitude': 77.506200,
                'waypoint_type': 'entrance',
                'description': 'North gate entrance'
            },
            {
                'name': 'Auditorium Path',
                'code': 'WP-AUD',
                'latitude': 12.963700,
                'longitude': 77.505750,
                'waypoint_type': 'pathway',
                'description': 'Path to Auditorium'
            },
            {
                'name': 'Research Center Junction',
                'code': 'WP-RD',
                'latitude': 12.964200,
                'longitude': 77.506450,
                'waypoint_type': 'junction',
                'description': 'Junction near R&D Center'
            }
        ]

        waypoint_objects = []
        for wp_data in waypoints_data:
            waypoint = Waypoint(**wp_data)
            db.session.add(waypoint)
            waypoint_objects.append(waypoint)

        db.session.commit()
        print(f"✓ Added {len(waypoints_data)} waypoints")

        # Now add paths connecting waypoints and buildings
        print("\nAdding paths connecting waypoints...")
        add_waypoint_paths()

        print("\n" + "="*70)
        print("✓ WAYPOINT SEEDING COMPLETE!")
        print("="*70)


def add_waypoint_paths():
    """Add paths connecting buildings and waypoints"""

    # Define paths (source_type, source_id, dest_type, dest_id, distance_m, time_min)
    paths_data = [
        # Main Gate connections
        ('waypoint', 'WP-GATE', 'waypoint', 'WP-ADMIN', 50, 1),

        # Admin Building (ID:1) connections
        ('building', 1, 'waypoint', 'WP-ADMIN', 30, 1),
        ('waypoint', 'WP-ADMIN', 'waypoint', 'WP-PLAZA', 40, 1),

        # Central Plaza hub - connects to everything
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-ACADEMIC', 45, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-LIB-PATH', 60, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-CAF', 55, 1),
        ('waypoint', 'WP-PLAZA', 'waypoint', 'WP-AUD', 35, 1),

        # Library (ID:2) connections
        ('building', 2, 'waypoint', 'WP-LIB-PATH', 25, 1),
        ('waypoint', 'WP-LIB-PATH', 'waypoint', 'WP-CAF', 40, 1),
        ('waypoint', 'WP-LIB-PATH', 'waypoint', 'WP-NORTH', 50, 1),

        # Academic blocks connections
        ('waypoint', 'WP-ACADEMIC', 'building', 4, 35, 1),  # CSE (ID:4)
        ('waypoint', 'WP-ACADEMIC', 'building', 5, 30, 1),  # ECE (ID:5)
        ('waypoint', 'WP-ACADEMIC', 'waypoint', 'WP-ENGG', 40, 1),

        # Civil Engineering (ID:3)
        ('building', 3, 'waypoint', 'WP-ENGG', 35, 1),
        ('waypoint', 'WP-ENGG', 'waypoint', 'WP-RD', 45, 1),

        # Cafeteria (ID:6)
        ('building', 6, 'waypoint', 'WP-CAF', 20, 1),
        ('waypoint', 'WP-CAF', 'waypoint', 'WP-HOSTEL', 60, 1),

        # Sports Complex (ID:7)
        ('building', 7, 'waypoint', 'WP-SPORTS', 25, 1),
        ('waypoint', 'WP-SPORTS', 'waypoint', 'WP-HOSTEL', 45, 1),
        ('waypoint', 'WP-SPORTS', 'waypoint', 'WP-NORTH', 35, 1),

        # Mechanical (ID:8)
        ('building', 8, 'waypoint', 'WP-ENGG', 30, 1),
        ('waypoint', 'WP-ENGG', 'waypoint', 'WP-RD', 40, 1),

        # Hostels (ID:9, 10)
        ('building', 9, 'waypoint', 'WP-HOSTEL', 30, 1),  # Boys Hostel
        ('building', 10, 'waypoint', 'WP-HOSTEL', 40, 1),  # Girls Hostel

        # Auditorium (ID:11)
        ('building', 11, 'waypoint', 'WP-AUD', 25, 1),
        ('waypoint', 'WP-AUD', 'waypoint', 'WP-ACADEMIC', 50, 1),

        # R&D Center (ID:12)
        ('building', 12, 'waypoint', 'WP-RD', 30, 1),
        ('waypoint', 'WP-RD', 'waypoint', 'WP-ENGG', 35, 1),
    ]

    # Get all waypoints by code
    waypoints = {wp.code: wp.waypoint_id for wp in Waypoint.query.all()}

    path_count = 0
    for source_type, source_id, dest_type, dest_id, distance, time in paths_data:
        # Resolve source
        if source_type == 'building':
            source_building_id = source_id
            source_waypoint_id = None
        else:
            source_building_id = None
            source_waypoint_id = waypoints.get(source_id)

        # Resolve destination
        if dest_type == 'building':
            dest_building_id = dest_id
            dest_waypoint_id = None
        else:
            dest_building_id = None
            dest_waypoint_id = waypoints.get(dest_id)

        if (source_building_id or source_waypoint_id) and (dest_building_id or dest_waypoint_id):
            # Create path WITHOUT is_bidirectional
            path = Path(
                source_building_id=source_building_id,
                source_waypoint_id=source_waypoint_id,
                destination_building_id=dest_building_id,
                destination_waypoint_id=dest_waypoint_id,
                distance=distance,
                estimated_time=time
            )
            db.session.add(path)
            path_count += 1

            # Add reverse path for bidirectional routing
            reverse_path = Path(
                source_building_id=dest_building_id,
                source_waypoint_id=dest_waypoint_id,
                destination_building_id=source_building_id,
                destination_waypoint_id=source_waypoint_id,
                distance=distance,
                estimated_time=time
            )
            db.session.add(reverse_path)
            path_count += 1

    db.session.commit()
    print(f"✓ Added {path_count} paths (bidirectional pairs)")


if __name__ == '__main__':
    seed_waypoints()
