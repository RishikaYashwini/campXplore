"""
Fix Path Table Constraints - Make Building IDs Nullable
Location: backend/fix_path_constraints.py
"""

from app import app
from extensions import db

def fix_path_constraints():
    """Make building_id columns nullable to support waypoint paths"""
    with app.app_context():
        print("\n" + "="*70)
        print("FIXING PATH TABLE CONSTRAINTS")
        print("="*70)

        with db.engine.connect() as connection:
            trans = connection.begin()

            try:
                print("\nMaking building columns nullable...")

                # Drop NOT NULL constraint from source_building_id
                connection.execute(db.text("""
                    ALTER TABLE paths 
                    ALTER COLUMN source_building_id DROP NOT NULL
                """))
                print("✓ source_building_id is now nullable")

                # Drop NOT NULL constraint from destination_building_id
                connection.execute(db.text("""
                    ALTER TABLE paths 
                    ALTER COLUMN destination_building_id DROP NOT NULL
                """))
                print("✓ destination_building_id is now nullable")

                trans.commit()

                print("\n" + "="*70)
                print("✓ CONSTRAINTS FIXED!")
                print("="*70)
                print("\nPaths table now supports:")
                print("  • Building-to-Building paths")
                print("  • Building-to-Waypoint paths")
                print("  • Waypoint-to-Waypoint paths")

            except Exception as e:
                trans.rollback()
                print(f"\n❌ ERROR: {str(e)}")
                raise


if __name__ == '__main__':
    fix_path_constraints()
