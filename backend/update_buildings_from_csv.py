"""
CampXplore Building Update Script - Full FK Constraint Handling
"""

import csv
import json
from datetime import datetime
from app import app
from extensions import db
from models.building import Building
from models.complaint import Complaint
from models.feedback import Feedback
from models.path import Path

def backup_existing_data():
    print("\n" + "="*60)
    print("STEP 1: Creating backup of existing data (buildings, paths, complaints, feedback)...")
    print("="*60)

    with app.app_context():
        existing_buildings = Building.query.all()
        existing_paths = Path.query.all()
        existing_complaints = Complaint.query.all()
        existing_feedback = Feedback.query.all()

        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'buildings': [b.to_dict() for b in existing_buildings],
            'paths': [p.to_dict() for p in existing_paths],
            'complaints': [c.to_dict() for c in existing_complaints],
            'feedback': [f.to_dict() for f in existing_feedback],
            'id_mapping': {}
        }

        backup_filename = f'backup_full_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=2)

        print(f"✓ Backed up buildings: {len(existing_buildings)}")
        print(f"✓ Backed up paths: {len(existing_paths)}")
        print(f"✓ Backed up complaints: {len(existing_complaints)}")
        print(f"✓ Backed up feedback: {len(existing_feedback)}")
        print(f"✓ Backup saved to: {backup_filename}")

        return backup_data

def load_csv_data(csv_file='campus_data.csv'):
    print("\n" + "="*60)
    print("STEP 2: Loading building data from CSV...")
    print("="*60)

    buildings_data = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            buildings_data.append({
                'name': row['Name'],
                'description': row['Description'],
                'latitude': float(row['Latitude (N)']),
                'longitude': float(row['Longitude (E)']),
                'type': row['Type']
            })

    print(f"✓ Loaded {len(buildings_data)} locations from CSV")
    return buildings_data

def clear_dependent_tables():
    print("\n" + "="*60)
    print("STEP 3: Clearing dependent tables to handle FK constraints...")
    print("="*60)

    with app.app_context():
        total_paths = Path.query.count()
        total_complaints = Complaint.query.count()
        total_feedback = Feedback.query.count()

        if total_paths > 0:
            Path.query.delete()
            db.session.commit()
            print(f"✓ Deleted {total_paths} paths")
        else:
            print("No paths to delete.")
            
        if total_complaints > 0:
            Complaint.query.delete()
            db.session.commit()
            print(f"✓ Deleted {total_complaints} complaints")
        else:
            print("No complaints to delete.")
            
        if total_feedback > 0:
            Feedback.query.delete()
            db.session.commit()
            print(f"✓ Deleted {total_feedback} feedback entries")
        else:
            print("No feedback to delete.")

def update_buildings(buildings_data):
    print("\n" + "="*60)
    print("STEP 4: Updating buildings table...")
    print("="*60)

    with app.app_context():
        old_buildings = Building.query.all()
        old_building_map = {b.building_id: b.name for b in old_buildings}

        print(f"Old buildings count: {len(old_buildings)}")

        # Clear buildings
        Building.query.delete()
        db.session.commit()
        print("✓ Cleared old building data")

        new_buildings = []
        for data in buildings_data:
            building = Building(
                name=data['name'],
                description=data['description'],
                latitude=data['latitude'],
                longitude=data['longitude'],
                code=None,
                floor_count=1,
                facilities=None,
                image_url=None
            )
            new_buildings.append(building)

        db.session.add_all(new_buildings)
        db.session.commit()
        print(f"✓ Inserted {len(new_buildings)} new buildings")

        new_buildings_sorted = Building.query.order_by(Building.building_id).all()
        id_mapping = {}

        for i, old_id in enumerate(sorted(old_building_map.keys())):
            if i < len(new_buildings_sorted):
                id_mapping[old_id] = new_buildings_sorted[i].building_id

        print("\nID Mapping (Old -> New):")
        for old_id, new_id in id_mapping.items():
            old_name = old_building_map.get(old_id, "Unknown")
            new_name = Building.query.get(new_id).name if new_id else "None"
            print(f"  {old_id} ({old_name[:30]}) -> {new_id} ({new_name[:30]})")

        return id_mapping

def restore_dependent_tables(backup_data, id_mapping):
    print("\n" + "="*60)
    print("STEP 5: Restoring dependent tables with updated building IDs...")
    print("="*60)

    with app.app_context():
        # Restore paths
        restored_paths = 0
        for p_data in backup_data['paths']:
            old_src = p_data['source_building_id']
            old_dest = p_data['destination_building_id']

            new_src = id_mapping.get(old_src, None)
            new_dest = id_mapping.get(old_dest, None)

            if new_src is None or new_dest is None:
                continue

            path = Path(
                source_building_id=new_src,
                dest_building_id=new_dest,
                source_waypoint_id=p_data.get('source_waypoint_id'),
                destination_waypoint_id=p_data.get('destination_waypoint_id'),
                distance=p_data.get('distance'),
                estimated_time=p_data.get('estimated_time'),
                path_type=p_data.get('path_type'),
                accessibility=p_data.get('accessibility'),
                created_at=p_data.get('created_at')
            )
            db.session.add(path)
            restored_paths += 1

        # Restore complaints
        restored_complaints = 0
        for c_data in backup_data['complaints']:
            old_building = c_data['building_id']
            new_building = id_mapping.get(old_building, None)
            if new_building is None:
                continue

            complaint = Complaint(
                user_id=c_data['user_id'],
                title=c_data['title'],
                description=c_data['description'],
                category=c_data['category'],
                priority=c_data['priority'],
                status=c_data['status'],
                building_id=new_building,
                location_details=c_data['location_details'],
                image_url=c_data.get('image_url'),
                admin_response=c_data.get('admin_response'),
                created_at=c_data['created_at'],
                updated_at=c_data['updated_at'],
                resolved_at=c_data.get('resolved_at')
            )
            db.session.add(complaint)
            restored_complaints += 1

        # Restore feedbacks
        restored_feedbacks = 0
        for f_data in backup_data['feedback']:
            old_building = f_data['building_id']
            new_building = id_mapping.get(old_building, None)
            if new_building is None:
                continue

            feedback = Feedback(
                user_id=f_data['user_id'],
                facility=f_data['facility'],
                building_id=new_building,
                rating=f_data['rating'],
                comments=f_data['comments'],
                category=f_data['category'],
                created_at=f_data['created_at']
            )
            db.session.add(feedback)
            restored_feedbacks += 1

        db.session.commit()
        print(f"✓ Restored {restored_paths} paths")
        print(f"✓ Restored {restored_complaints} complaints")
        print(f"✓ Restored {restored_feedbacks} feedbacks")

def verify_update():
    print("\n" + "="*60)
    print("STEP 6: Verifying update...")
    print("="*60)

    with app.app_context():
        buildings = Building.query.all()
        print(f"✓ Total buildings in database: {len(buildings)}")

        print("\nSample buildings:")
        for b in buildings[:5]:
            print(f"  - {b.name} ({b.latitude}, {b.longitude})")

        complaints_count = Complaint.query.count()
        feedbacks_count = Feedback.query.count()
        paths_count = Path.query.count()

        print(f"\n✓ Complaints preserved: {complaints_count}")
        print(f"✓ Feedbacks preserved: {feedbacks_count}")
        print(f"✓ Paths preserved: {paths_count}")

def main():
    print("\n" + "="*70)
    print("  CampXplore Building Update - Full FK Constraints Handling")
    print("="*70)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    try:
        backup_data = backup_existing_data()

        clear_dependent_tables()

        buildings_data = load_csv_data('campus_data.csv')

        id_mapping = update_buildings(buildings_data)

        restore_dependent_tables(backup_data, id_mapping)

        verify_update()

        print("\n" + "="*70)
        print("  ✓✓✓ UPDATE COMPLETED SUCCESSFULLY! ✓✓✓")
        print("="*70)
        print(f"  Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nUpdate failed. Please check the error and try again.")
        print("Your data has been backed up and can be restored if needed.")
        raise

if __name__ == '__main__':
    main()
