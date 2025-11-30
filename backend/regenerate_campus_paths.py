"""
CampXplore Realistic Path Regeneration Script - FIXED VERSION
Generates realistic walking paths using buildings and waypoints
Handles Decimal/Float type conversion for database compatibility
"""

import csv
import math
from datetime import datetime
from decimal import Decimal
from app import app
from extensions import db
from models.building import Building
from models.waypoint import Waypoint
from models.path import Path

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in meters
    Handles both float and Decimal types from database
    """
    # Convert all inputs to float to handle Decimal types from database
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    R = 6371000  # Earth radius in meters

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def calculate_walking_time(distance_meters):
    """Calculate estimated walking time in minutes (assuming 1.4 m/s average walking speed)"""
    walking_speed = 1.4  # meters per second
    time_seconds = distance_meters / walking_speed
    return max(1, int(time_seconds / 60))  # Minimum 1 minute

def load_waypoints_from_csv(csv_file='dr_ait_campus_waypoints.csv'):
    """Load waypoints from CSV and insert into database"""
    print("\n" + "="*60)
    print("STEP 1: Loading waypoints from CSV...")
    print("="*60)

    with app.app_context():
        # Clear existing waypoints
        Waypoint.query.delete()
        db.session.commit()
        print("✓ Cleared existing waypoints")

        waypoints_data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                waypoint = Waypoint(
                    waypoint_id=int(row['waypoint_id']),
                    name=row['name'],
                    code=f"WP{row['waypoint_id']}",
                    latitude=float(row['latitude(N)']),
                    longitude=float(row['longitude(E)']),
                    waypoint_type=row['type']
                )
                waypoints_data.append(waypoint)

        db.session.bulk_save_objects(waypoints_data)
        db.session.commit()
        print(f"✓ Loaded {len(waypoints_data)} waypoints from CSV")

        return waypoints_data

def generate_realistic_paths():
    """Generate realistic paths based on proximity and campus layout"""
    print("\n" + "="*60)
    print("STEP 2: Generating realistic campus paths...")
    print("="*60)

    with app.app_context():
        # Get all buildings and waypoints
        buildings = Building.query.all()
        waypoints = Waypoint.query.all()

        print(f"Buildings: {len(buildings)}")
        print(f"Waypoints: {len(waypoints)}")

        paths = []

        # Strategy 1: Connect each building to nearest waypoints (entrance/intersection types)
        print("\nConnecting buildings to nearby waypoints...")
        for building in buildings:
            nearest_waypoints = []

            for waypoint in waypoints:
                distance = haversine_distance(
                    building.latitude, building.longitude,
                    waypoint.latitude, waypoint.longitude
                )

                # Connect building to waypoints within 150 meters
                if distance <= 150:
                    nearest_waypoints.append((waypoint, distance))

            # Sort by distance and take closest 3
            nearest_waypoints.sort(key=lambda x: x[1])
            for waypoint, distance in nearest_waypoints[:3]:
                path = Path(
                    source_building_id=building.building_id,
                    destination_waypoint_id=waypoint.waypoint_id,
                    distance=round(distance, 2),
                    estimated_time=calculate_walking_time(distance),
                    path_type='walkway',
                    accessibility=True
                )
                paths.append(path)

                # Create reverse path
                reverse_path = Path(
                    source_waypoint_id=waypoint.waypoint_id,
                    destination_building_id=building.building_id,
                    distance=round(distance, 2),
                    estimated_time=calculate_walking_time(distance),
                    path_type='walkway',
                    accessibility=True
                )
                paths.append(reverse_path)

        print(f"✓ Created {len(paths)} building-waypoint connections")

        # Strategy 2: Connect waypoints to nearby waypoints (realistic walking paths)
        print("\nConnecting waypoints to form walking paths...")
        waypoint_paths_count = 0

        for i, wp1 in enumerate(waypoints):
            for wp2 in waypoints[i+1:]:
                distance = haversine_distance(
                    wp1.latitude, wp1.longitude,
                    wp2.latitude, wp2.longitude
                )

                # Connect waypoints within 100 meters (realistic walking distance)
                if distance <= 100:
                    path = Path(
                        source_waypoint_id=wp1.waypoint_id,
                        destination_waypoint_id=wp2.waypoint_id,
                        distance=round(distance, 2),
                        estimated_time=calculate_walking_time(distance),
                        path_type='walkway',
                        accessibility=True
                    )
                    paths.append(path)

                    # Create reverse path
                    reverse_path = Path(
                        destination_waypoint_id=wp1.waypoint_id,
                        source_waypoint_id=wp2.waypoint_id,
                        distance=round(distance, 2),
                        estimated_time=calculate_walking_time(distance),
                        path_type='walkway',
                        accessibility=True
                    )
                    paths.append(reverse_path)
                    waypoint_paths_count += 2

        print(f"✓ Created {waypoint_paths_count} waypoint-waypoint connections")

        # Strategy 3: Direct building-to-building for very close buildings
        print("\nConnecting nearby buildings directly...")
        building_paths_count = 0

        for i, b1 in enumerate(buildings):
            for b2 in buildings[i+1:]:
                distance = haversine_distance(
                    b1.latitude, b1.longitude,
                    b2.latitude, b2.longitude
                )

                # Connect buildings within 80 meters directly
                if distance <= 80:
                    path = Path(
                        source_building_id=b1.building_id,
                        destination_building_id=b2.building_id,
                        distance=round(distance, 2),
                        estimated_time=calculate_walking_time(distance),
                        path_type='walkway',
                        accessibility=True
                    )
                    paths.append(path)

                    # Create reverse path
                    reverse_path = Path(
                        source_building_id=b2.building_id,
                        destination_building_id=b1.building_id,
                        distance=round(distance, 2),
                        estimated_time=calculate_walking_time(distance),
                        path_type='walkway',
                        accessibility=True
                    )
                    paths.append(reverse_path)
                    building_paths_count += 2

        print(f"✓ Created {building_paths_count} direct building-building connections")

        # Insert all paths into database
        print("\nInserting paths into database...")
        db.session.bulk_save_objects(paths)
        db.session.commit()

        print(f"\n✓ Total paths created: {len(paths)}")

        return len(paths)

def verify_paths():
    """Verify that paths were created successfully"""
    print("\n" + "="*60)
    print("STEP 3: Verifying path generation...")
    print("="*60)

    with app.app_context():
        total_paths = Path.query.count()
        building_to_waypoint = Path.query.filter(
            Path.source_building_id.isnot(None),
            Path.destination_waypoint_id.isnot(None)
        ).count()

        waypoint_to_waypoint = Path.query.filter(
            Path.source_waypoint_id.isnot(None),
            Path.destination_waypoint_id.isnot(None)
        ).count()

        building_to_building = Path.query.filter(
            Path.source_building_id.isnot(None),
            Path.destination_building_id.isnot(None)
        ).count()

        print(f"✓ Total paths: {total_paths}")
        print(f"  - Building → Waypoint: {building_to_waypoint}")
        print(f"  - Waypoint → Waypoint: {waypoint_to_waypoint}")
        print(f"  - Building → Building: {building_to_building}")

        # Sample paths
        print("\nSample paths:")
        sample_paths = Path.query.limit(5).all()
        for p in sample_paths:
            print(f"  Path {p.path_id}: {p.distance}m, {p.estimated_time} min")

def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("  CampXplore Realistic Path Regeneration - FIXED VERSION")
    print("="*70)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        # Step 1: Load waypoints
        load_waypoints_from_csv('dr_ait_campus_waypoints.csv')

        # Step 2: Generate paths
        total_paths = generate_realistic_paths()

        # Step 3: Verify
        verify_paths()

        print("\n" + "="*70)
        print("  ✓✓✓ PATH GENERATION COMPLETED SUCCESSFULLY! ✓✓✓")
        print("="*70)
        print(f"  Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print("\nYour navigation routing is now ready to use!")
        print("Test it on the frontend by selecting two buildings for directions.")

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nPath generation failed. Please check the error.")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
