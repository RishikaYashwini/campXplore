"""
PHASE 2: Enhanced Navigation API with Waypoints
Location: backend/routes/navigation.py
"""

from flask import Blueprint, request, jsonify, session
from extensions import db
from models.building import Building
from models.waypoint import Waypoint
from models.path import Path
import heapq

navigation_bp = Blueprint('navigation', __name__, url_prefix='/api/navigation')


def session_required(f):
    """Custom decorator for session-based authentication"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


class WaypointRouter:
    """Enhanced router that handles buildings and waypoints"""

    def __init__(self):
        self.graph = {}
        self.nodes = {}  # Store node info (type, name, coordinates)

    def build_graph(self):
        """Build graph with buildings and waypoints"""
        # Get all buildings
        buildings = Building.query.all()
        for building in buildings:
            node_id = f"B{building.building_id}"
            self.nodes[node_id] = {
                'type': 'building',
                'id': building.building_id,
                'name': building.name,
                'code': building.code,
                'lat': float(building.latitude),
                'lng': float(building.longitude)
            }
            self.graph[node_id] = []

        # Get all waypoints
        waypoints = Waypoint.query.all()
        for waypoint in waypoints:
            node_id = f"W{waypoint.waypoint_id}"
            self.nodes[node_id] = {
                'type': 'waypoint',
                'id': waypoint.waypoint_id,
                'name': waypoint.name,
                'code': waypoint.code,
                'lat': float(waypoint.latitude),
                'lng': float(waypoint.longitude)
            }
            self.graph[node_id] = []

        # Get all paths
        paths = Path.query.all()
        for path in paths:
            # Determine source node
            if path.source_building_id:
                source = f"B{path.source_building_id}"
            elif path.source_waypoint_id:
                source = f"W{path.source_waypoint_id}"
            else:
                continue

            # Determine destination node
            if path.destination_building_id:
                dest = f"B{path.destination_building_id}"
            elif path.destination_waypoint_id:
                dest = f"W{path.destination_waypoint_id}"
            else:
                continue

            # Add edge to graph
            distance = float(path.distance)
            self.graph[source].append((dest, distance))

    def dijkstra(self, start_node, end_node):
        """Find shortest path using Dijkstra's algorithm"""
        if start_node not in self.graph or end_node not in self.graph:
            return None, float('inf')

        # Priority queue: (distance, node, path)
        pq = [(0, start_node, [start_node])]
        visited = set()

        while pq:
            current_dist, current_node, path = heapq.heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)

            if current_node == end_node:
                return path, current_dist

            for neighbor, edge_dist in self.graph[current_node]:
                if neighbor not in visited:
                    new_dist = current_dist + edge_dist
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_dist, neighbor, new_path))

        return None, float('inf')

    def get_route_details(self, path_nodes):
        """Convert node IDs to detailed route information"""
        if not path_nodes:
            return []

        route_details = []
        for i, node_id in enumerate(path_nodes):
            node_info = self.nodes[node_id].copy()

            # Calculate segment distance if not last node
            if i < len(path_nodes) - 1:
                next_node = path_nodes[i + 1]
                segment_distance = self._get_segment_distance(node_id, next_node)
                node_info['distance_to_next'] = segment_distance
            else:
                node_info['distance_to_next'] = 0

            node_info['sequence'] = i + 1
            route_details.append(node_info)

        return route_details

    def _get_segment_distance(self, node1, node2):
        """Get distance between two connected nodes"""
        # Parse node IDs
        if node1.startswith('B'):
            source_building_id = int(node1[1:])
            source_waypoint_id = None
        else:
            source_building_id = None
            source_waypoint_id = int(node1[1:])

        if node2.startswith('B'):
            dest_building_id = int(node2[1:])
            dest_waypoint_id = None
        else:
            dest_building_id = None
            dest_waypoint_id = int(node2[1:])

        # Find path in database
        path = Path.query.filter_by(
            source_building_id=source_building_id,
            source_waypoint_id=source_waypoint_id,
            destination_building_id=dest_building_id,
            destination_waypoint_id=dest_waypoint_id
        ).first()

        return float(path.distance) if path else 0


@navigation_bp.route('/route', methods=['POST'])
@session_required
def calculate_route():
    """Calculate route between two buildings using waypoints"""
    try:
        data = request.get_json()
        start_building_id = data.get('start_building_id')
        end_building_id = data.get('end_building_id')

        if not start_building_id or not end_building_id:
            return jsonify({'error': 'Start and end buildings required'}), 400

        # Verify buildings exist
        start_building = Building.query.get(start_building_id)
        end_building = Building.query.get(end_building_id)

        if not start_building or not end_building:
            return jsonify({'error': 'Invalid building IDs'}), 404

        # Build routing graph
        router = WaypointRouter()
        router.build_graph()

        # Calculate shortest path
        start_node = f"B{start_building_id}"
        end_node = f"B{end_building_id}"

        path_nodes, total_distance = router.dijkstra(start_node, end_node)

        if path_nodes is None:
            return jsonify({'error': 'No route found between buildings'}), 404

        # Get detailed route information
        route_details = router.get_route_details(path_nodes)

        # Calculate estimated time (assuming 1.4 m/s walking speed)
        walking_speed = 1.4  # meters per second
        estimated_time_seconds = total_distance / walking_speed
        estimated_time_minutes = int(estimated_time_seconds / 60)

        # Generate turn-by-turn directions
        directions = generate_directions(route_details)

        response = {
            'start': {
                'building_id': start_building.building_id,
                'name': start_building.name,
                'code': start_building.code,
                'lat': float(start_building.latitude),
                'lng': float(start_building.longitude)
            },
            'end': {
                'building_id': end_building.building_id,
                'name': end_building.name,
                'code': end_building.code,
                'lat': float(end_building.latitude),
                'lng': float(end_building.longitude)
            },
            'route': route_details,
            'total_distance': round(total_distance, 2),
            'estimated_time_minutes': max(1, estimated_time_minutes),
            'waypoints_count': len([r for r in route_details if r['type'] == 'waypoint']),
            'directions': directions
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error calculating route: {str(e)}")
        return jsonify({'error': str(e)}), 500


def generate_directions(route_details):
    """Generate human-readable turn-by-turn directions"""
    directions = []

    for i, segment in enumerate(route_details):
        if i == 0:
            # Start point
            directions.append({
                'step': 1,
                'instruction': f"Start at {segment['name']}",
                'distance': 0
            })
        elif i < len(route_details) - 1:
            # Intermediate waypoints
            distance = segment.get('distance_to_next', 0)
            next_point = route_details[i + 1]

            directions.append({
                'step': i + 1,
                'instruction': f"Walk {distance}m towards {next_point['name']}",
                'distance': distance
            })
        else:
            # End point
            directions.append({
                'step': len(route_details),
                'instruction': f"Arrive at {segment['name']}",
                'distance': 0
            })

    return directions


@navigation_bp.route('/waypoints', methods=['GET'])
@session_required
def get_waypoints():
    """Get all waypoints for map display"""
    try:
        waypoints = Waypoint.query.all()
        return jsonify({
            'waypoints': [wp.to_dict() for wp in waypoints]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
