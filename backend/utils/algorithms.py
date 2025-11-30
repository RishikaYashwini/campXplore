"""
Algorithm Implementations
Navigation and pathfinding algorithms
"""

import heapq
from models.path import Path
from models.building import Building


def dijkstra_shortest_path(start_building_id, end_building_id):
    """
    Find shortest path between two buildings using Dijkstra's algorithm

    Args:
        start_building_id (int): Starting building ID
        end_building_id (int): Destination building ID

    Returns:
        tuple: (path_list, total_distance) or (None, None) if no path found
    """

    # Get all paths from database
    all_paths = Path.query.all()

    if not all_paths:
        return None, None

    # Build adjacency graph
    graph = {}
    all_building_ids = set()

    for path in all_paths:
        source = path.source_building_id
        dest = path.destination_building_id
        distance = float(path.distance)

        all_building_ids.add(source)
        all_building_ids.add(dest)

        # Initialize graph entries
        if source not in graph:
            graph[source] = []
        if dest not in graph:
            graph[dest] = []

        # Add bidirectional edges
        graph[source].append((dest, distance))
        graph[dest].append((source, distance))

    # Check if start and end buildings exist
    if start_building_id not in all_building_ids or end_building_id not in all_building_ids:
        return None, None

    # Dijkstra's algorithm implementation
    distances = {building_id: float('infinity') for building_id in all_building_ids}
    previous = {building_id: None for building_id in all_building_ids}
    distances[start_building_id] = 0

    # Priority queue: (distance, building_id)
    pq = [(0, start_building_id)]
    visited = set()

    while pq:
        current_distance, current_building = heapq.heappop(pq)

        # Skip if already visited
        if current_building in visited:
            continue

        visited.add(current_building)

        # Found destination
        if current_building == end_building_id:
            break

        # Skip if current distance is greater than recorded
        if current_distance > distances[current_building]:
            continue

        # Check neighbors
        if current_building in graph:
            for neighbor, weight in graph[current_building]:
                distance = current_distance + weight

                # Update if shorter path found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_building
                    heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path
    if distances[end_building_id] == float('infinity'):
        return None, None

    path = []
    current = end_building_id

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end_building_id]


def get_path_details(building_ids):
    """
    Get detailed building information for a path

    Args:
        building_ids (list): List of building IDs in path order

    Returns:
        list: List of building dictionaries with details
    """
    if not building_ids:
        return []

    buildings = Building.query.filter(Building.building_id.in_(building_ids)).all()
    building_dict = {b.building_id: b for b in buildings}

    # Return in order
    result = []
    for bid in building_ids:
        if bid in building_dict:
            result.append(building_dict[bid].to_dict())

    return result
