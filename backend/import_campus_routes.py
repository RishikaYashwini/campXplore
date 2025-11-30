"""
CampXplore - Route-Based Path Import Script
Automatically calculates distances and creates paths from route definitions
"""

import csv
import math
from datetime import datetime
from app import app
from extensions import db
from models.building import Building
from models.waypoint import Waypoint
from models.path import Path

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in meters"""
    # Convert to float to handle Decimal types
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)

    R = 6371000  # Earth radius in meters
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def calculate_walking_time(distance_meters):
    """Calculate estimated walking time in minutes"""
    walking_speed = 1.4  # meters per second
    time_seconds = distance_meters / walking_speed
    return max(1, int(time_seconds / 60))

def get_node_coordinates(node_type, node_id, buildings_dict, waypoints_dict):
    """Get GPS coordinates for a building or waypoint"""
    if node_type == 'B':
        if node_id in buildings_dict:
            return buildings_dict[node_id]['lat'], buildings_dict[node_id]['lon']
    elif node_type == 'W':
        if node_id in waypoints_dict:
            return waypoints_dict[node_id]['lat'], waypoints_dict[node_id]['lon']
    return None, None

def parse_route_sequence(sequence):
    """
    Parse route sequence like: B:3 > W:110 > W:105 > B:5
    Returns list of (type, id) tuples: [('B', 3), ('W', 110), ('W', 105), ('B', 5)]
    """
    nodes = []
    parts = sequence.split('>')

    for part in parts:
        part = part.strip()
        if ':' not in part:
            continue

        node_type, node_id = part.split(':')
        node_type = node_type.strip().upper()
        node_id = int(node_id.strip())
        nodes.append((node_type, node_id))

    return nodes

def create_paths_from_route(route_name, sequence, path_type, accessibility, buildings_dict, waypoints_dict):
    """Create individual path entries from a route sequence"""
    nodes = parse_route_sequence(sequence)

    if len(nodes) < 2:
        print(f"  ✗ Route '{route_name}' has less than 2 nodes. Skipping.")
        return []

    paths = []
    total_distance = 0

    # Create paths for each hop in the route
    for i in range(len(nodes) - 1):
        src_type, src_id = nodes[i]
        dest_type, dest_id = nodes[i + 1]

        # Get coordinates
        src_lat, src_lon = get_node_coordinates(src_type, src_id, buildings_dict, waypoints_dict)
        dest_lat, dest_lon = get_node_coordinates(dest_type, dest_id, buildings_dict, waypoints_dict)

        if src_lat is None or dest_lat is None:
            print(f"  ✗ Could not find coordinates for {src_type}:{src_id} or {dest_type}:{dest_id}")
            continue

        # Calculate distance
        distance = haversine_distance(src_lat, src_lon, dest_lat, dest_lon)
        total_distance += distance

        # Create path object
        path_data = {
            'distance': round(distance, 2),
            'estimated_time': calculate_walking_time(distance),
            'path_type': path_type,
            'accessibility': accessibility
        }

        # Set source and destination based on type
        if src_type == 'B':
            path_data['source_building_id'] = src_id
        else:
            path_data['source_waypoint_id'] = src_id

        if dest_type == 'B':
            path_data['destination_building_id'] = dest_id
        else:
            path_data['destination_waypoint_id'] = dest_id

        paths.append(path_data)

    print(f"  ✓ Route '{route_name}': {len(paths)} hops, {round(total_distance, 2)}m total")

    return paths

def load_routes_from_csv(csv_file='campus_routes.csv'):
    """Load routes from CSV and create path entries"""
    print("\n" + "="*70)
    print("LOADING ROUTES FROM CSV")
    print("="*70)

    with app.app_context():
        # Load buildings and waypoints
        buildings = Building.query.all()
        waypoints = Waypoint.query.all()

        buildings_dict = {
            b.building_id: {'lat': b.latitude, 'lon': b.longitude, 'name': b.name}
            for b in buildings
        }

        waypoints_dict = {
            w.waypoint_id: {'lat': w.latitude, 'lon': w.longitude, 'name': w.name}
            for w in waypoints
        }

        print(f"✓ Loaded {len(buildings_dict)} buildings")
        print(f"✓ Loaded {len(waypoints_dict)} waypoints")

        # Read routes from CSV
        all_paths = []
        route_count = 0

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                route_name = row['route_name']
                sequence = row['path_sequence']
                path_type = row.get('path_type', 'walkway')
                accessibility = row.get('accessibility', 'true').lower() == 'true'

                print(f"\nProcessing: {route_name}")
                print(f"  Sequence: {sequence}")

                paths = create_paths_from_route(
                    route_name, sequence, path_type, accessibility,
                    buildings_dict, waypoints_dict
                )

                all_paths.extend(paths)
                route_count += 1

        return all_paths, route_count

def import_paths(csv_file='campus_routes.csv', clear_existing=True):
    """Import paths from CSV file"""
    print("\n" + "="*70)
    print("CAMPXPLORE - ROUTE-BASED PATH IMPORT")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    with app.app_context():
        # Clear existing paths if requested
        if clear_existing:
            print("\nClearing existing paths...")
            existing_count = Path.query.count()
            Path.query.delete()
            db.session.commit()
            print(f"✓ Deleted {existing_count} existing paths")

        # Load routes and create paths
        all_paths, route_count = load_routes_from_csv(csv_file)

        # Insert paths into database
        print("\n" + "="*70)
        print("INSERTING PATHS INTO DATABASE")
        print("="*70)

        for path_data in all_paths:
            path = Path(**path_data)
            db.session.add(path)

        db.session.commit()

        print(f"\n✓ Successfully imported {len(all_paths)} path segments from {route_count} routes")

        # Verify
        total_paths = Path.query.count()
        print(f"✓ Total paths in database: {total_paths}")

        print("\n" + "="*70)
        print("✓✓✓ IMPORT COMPLETED SUCCESSFULLY! ✓✓✓")
        print("="*70)
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print("\nRestart your backend and test navigation!")

if __name__ == '__main__':
    import_paths('campus_routes.csv', clear_existing=True)
