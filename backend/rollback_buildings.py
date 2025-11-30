"""
CampXplore Building Rollback Script
Restores buildings from backup file if update fails or needs to be reverted
"""

import json
import sys
from datetime import datetime
from app import app
from extensions import db
from models.building import Building

def list_backups():
    """List all available backup files"""
    import os
    import glob

    backups = glob.glob('backup_buildings_*.json')
    backups.sort(reverse=True)

    if not backups:
        print("No backup files found!")
        return None

    print("\nAvailable backups:")
    for i, backup in enumerate(backups, 1):
        size = os.path.getsize(backup)
        print(f"  {i}. {backup} ({size} bytes)")

    return backups

def restore_from_backup(backup_file):
    """Restore buildings from backup file"""
    print(f"\nRestoring from: {backup_file}")

    with open(backup_file, 'r') as f:
        backup_data = json.load(f)

    print(f"Backup timestamp: {backup_data['timestamp']}")
    print(f"Buildings in backup: {len(backup_data['buildings'])}")

    with app.app_context():
        # Clear current buildings
        Building.query.delete()
        db.session.commit()
        print("✓ Cleared current building data")

        # Restore from backup
        for building_data in backup_data['buildings']:
            building = Building(
                name=building_data['name'],
                code=building_data.get('code'),
                latitude=building_data['latitude'],
                longitude=building_data['longitude'],
                description=building_data.get('description'),
                floor_count=building_data.get('floor_count', 1),
                facilities=building_data.get('facilities'),
                image_url=building_data.get('image_url')
            )
            db.session.add(building)

        db.session.commit()
        print(f"✓ Restored {len(backup_data['buildings'])} buildings")

        # Verify
        count = Building.query.count()
        print(f"\n✓ Verification: {count} buildings in database")

def main():
    """Main execution"""
    print("="*60)
    print("  CampXplore Building Rollback Tool")
    print("="*60)

    backups = list_backups()

    if not backups:
        return

    print("\nEnter backup number to restore (or 'q' to quit): ", end='')
    choice = input()

    if choice.lower() == 'q':
        print("Cancelled.")
        return

    try:
        index = int(choice) - 1
        if 0 <= index < len(backups):
            restore_from_backup(backups[index])
            print("\n✓✓✓ ROLLBACK COMPLETED SUCCESSFULLY! ✓✓✓")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input!")

if __name__ == '__main__':
    main()
