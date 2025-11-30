"""
Database Reset Script
Drops all tables and recreates them fresh
"""

from app import app
from extensions import db

def reset_database():
    """Drop all tables and recreate"""
    with app.app_context():
        print("="*80)
        print("RESETTING DATABASE")
        print("="*80)
        print()

        print("Dropping all existing tables...")
        db.drop_all()
        print("✓ All tables dropped")

        print("\nCreating fresh tables...")
        db.create_all()
        print("✓ Fresh tables created")

        print("\n" + "="*80)
        print("✓ DATABASE RESET COMPLETE")
        print("="*80)
        print("\nNow run: python init_db.py")
        print("="*80)

if __name__ == '__main__':
    reset_database()
