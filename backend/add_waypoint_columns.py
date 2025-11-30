"""
Database Migration - Add Waypoint Columns to Paths Table
Location: backend/add_waypoint_columns.py
"""

from app import app
from extensions import db

def add_waypoint_columns():
    """Add source_waypoint_id and destination_waypoint_id to paths table"""
    with app.app_context():
        print("\n" + "="*70)
        print("ADDING WAYPOINT COLUMNS TO PATHS TABLE")
        print("="*70)

        # Get database connection
        with db.engine.connect() as connection:
            # Start transaction
            trans = connection.begin()

            try:
                # Check if columns already exist
                check_query = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='paths' 
                AND column_name IN ('source_waypoint_id', 'destination_waypoint_id')
                """
                result = connection.execute(db.text(check_query))
                existing_cols = [row[0] for row in result]

                if 'source_waypoint_id' in existing_cols and 'destination_waypoint_id' in existing_cols:
                    print("✓ Columns already exist!")
                    trans.commit()
                    return

                print("\nAdding columns to paths table...")

                # Add source_waypoint_id column
                if 'source_waypoint_id' not in existing_cols:
                    connection.execute(db.text("""
                        ALTER TABLE paths 
                        ADD COLUMN source_waypoint_id INTEGER
                    """))
                    print("✓ Added source_waypoint_id column")

                # Add destination_waypoint_id column
                if 'destination_waypoint_id' not in existing_cols:
                    connection.execute(db.text("""
                        ALTER TABLE paths 
                        ADD COLUMN destination_waypoint_id INTEGER
                    """))
                    print("✓ Added destination_waypoint_id column")

                # Add foreign key constraints
                print("\nAdding foreign key constraints...")

                try:
                    connection.execute(db.text("""
                        ALTER TABLE paths 
                        ADD CONSTRAINT fk_paths_source_waypoint 
                        FOREIGN KEY (source_waypoint_id) 
                        REFERENCES waypoints(waypoint_id)
                    """))
                    print("✓ Added foreign key for source_waypoint_id")
                except Exception as e:
                    print(f"  Note: Foreign key constraint may already exist ({str(e)[:50]}...)")

                try:
                    connection.execute(db.text("""
                        ALTER TABLE paths 
                        ADD CONSTRAINT fk_paths_destination_waypoint 
                        FOREIGN KEY (destination_waypoint_id) 
                        REFERENCES waypoints(waypoint_id)
                    """))
                    print("✓ Added foreign key for destination_waypoint_id")
                except Exception as e:
                    print(f"  Note: Foreign key constraint may already exist ({str(e)[:50]}...)")

                # Commit transaction
                trans.commit()

                print("\n" + "="*70)
                print("✓ MIGRATION COMPLETE!")
                print("="*70)
                print("\nPaths table now supports waypoint routing!")

            except Exception as e:
                trans.rollback()
                print(f"\n❌ ERROR: {str(e)}")
                raise


if __name__ == '__main__':
    add_waypoint_columns()
