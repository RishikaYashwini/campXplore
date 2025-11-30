"""
Database Initialization Script - Dr. Ambedkar Institute of Technology
VERIFIED GPS coordinates manually confirmed
Campus Center: 12.963718°N, 77.506037°E
"""

from app import app
from extensions import db
from models.user import User
from models.building import Building
from models.path import Path
from models.complaint import Complaint
from models.feedback import Feedback


def init_database():
    """Initialize database with tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")


def seed_buildings():
    """Add Dr. AIT campus buildings with VERIFIED coordinates"""
    with app.app_context():
        print("\nSeeding Dr. AIT buildings with manually verified GPS coordinates...")

        # Verified campus center: 12.963718°N, 77.506037°E
        # Campus spread: ~450m x 300m on 20.30 acres
        # Each building positioned relative to campus center

        buildings_data = [
            {
                'name': 'Main Administrative Block',
                'code': 'ADMIN',
                'latitude': 12.963514,
                'longitude': 77.505695,
                'description': 'Main administrative building housing principal office, accounts, and admission department. Located at campus center.',
                'floor_count': 3,
                'facilities': ['Principal Office', 'Admission Office', 'Accounts Department', 'Staff Rooms', 'Reception']
            },
            {
                'name': 'Central Library',
                'code': 'LIB',
                'latitude': 12.964675,
                'longitude': 77.505570,
                'description': 'Central library with 72,983 volumes, digital library with DELNET access, and reading halls',
                'floor_count': 3,
                'facilities': ['Reading Hall', 'Digital Library', 'DELNET Access', 'Study Rooms', 'Book Collection']
            },
            {
                'name': 'Civil Engineering Block',
                'code': 'CIVIL',
                'latitude': 12.964282,
                'longitude': 77.506511,
                'description': 'Civil Engineering department with material testing, surveying, and concrete labs',
                'floor_count': 3,
                'facilities': ['Classrooms', 'Material Testing Lab', 'Surveying Lab', 'Concrete Lab', 'Faculty Rooms']
            },
            {
                'name': 'Computer Science Block',
                'code': 'CSE',
                'latitude': 12.963260,
                'longitude': 77.506344,
                'description': 'Computer Science and Engineering department with advanced computer labs and project facilities',
                'floor_count': 4,
                'facilities': ['Computer Labs', 'Project Lab', 'Classrooms', 'Server Room', 'Faculty Cabins']
            },
            {
                'name': 'Electronics & Communication Block',
                'code': 'ECE',
                'latitude': 12.963298,
                'longitude': 77.506039,
                'description': 'ECE department with electronics, communication, VLSI and embedded systems labs',
                'floor_count': 3,
                'facilities': ['Electronics Lab', 'Communication Lab', 'VLSI Lab', 'Embedded Systems Lab', 'Classrooms']
            },
            {
                'name': 'Student Cafeteria',
                'code': 'CAF',
                'latitude': 12.964537,
                'longitude': 77.505333,
                'description': 'Central cafeteria serving vegetarian food and snacks to students and faculty',
                'floor_count': 2,
                'facilities': ['Food Court', 'Seating Area', 'Canteen', 'Snack Counter', 'WiFi']
            },
            {
                'name': 'Sports Complex & Indoor Stadium',
                'code': 'SPORTS',
                'latitude': 12.964951,
                'longitude': 77.506033,
                'description': 'Indoor sports complex with gymnasium, basketball court and outdoor playgrounds',
                'floor_count': 2,
                'facilities': ['Indoor Stadium', 'Gymnasium', 'Sports Equipment', 'Changing Rooms', 'Basketball Court']
            },
            {
                'name': 'Mechanical Engineering Block',
                'code': 'MECH',
                'latitude': 12.964022,
                'longitude': 77.506649,
                'description': 'Mechanical Engineering department with workshop, CAD lab and thermodynamics facilities',
                'floor_count': 3,
                'facilities': ['Workshop', 'CAD Lab', 'Thermodynamics Lab', 'Machine Shop', 'Classrooms']
            },
            {
                'name': 'Boys Hostel',
                'code': 'HOSTEL-B',
                'latitude': 12.965166,
                'longitude': 77.505364,
                'description': 'Boys hostel with accommodation for 900 students. Includes mess and recreation facilities.',
                'floor_count': 4,
                'facilities': ['Rooms', 'Common Room', 'Mess', 'Study Hall', 'Recreation Area']
            },
            {
                'name': 'Girls Hostel',
                'code': 'HOSTEL-G',
                'latitude': 12.964269,
                'longitude': 77.506232,
                'description': 'Girls hostel with accommodation for 600 students with 24/7 security',
                'floor_count': 4,
                'facilities': ['Rooms', 'Common Room', 'Mess', 'Study Hall', 'Security']
            },
            {
                'name': 'Auditorium & Seminar Hall',
                'code': 'AUD',
                'latitude': 12.963459,
                'longitude': 77.505921,
                'description': 'Main auditorium for events, seminars, cultural activities and placement drives',
                'floor_count': 2,
                'facilities': ['Auditorium', 'Seminar Halls', 'Audio-Visual Equipment', 'Stage', 'Green Room']
            },
            {
                'name': 'Research & Development Center',
                'code': 'R&D',
                'latitude': 12.964434,
                'longitude': 77.506523,
                'description': 'Research center with TEQIP funding for advanced research and development projects',
                'floor_count': 2,
                'facilities': ['Research Labs', 'Project Rooms', 'Conference Room', 'Equipment Room', 'Faculty Research Area']
            }
        ]

        for building_data in buildings_data:
            building = Building(**building_data)
            db.session.add(building)

        db.session.commit()
        print(f"✓ Added {len(buildings_data)} Dr. AIT campus buildings with precise GPS coordinates")
        print("  Campus Center: 12.963718°N, 77.506037°E")
        print("  Campus Area: 20.30 acres")

def seed_paths():
    """Add paths between Dr. AIT buildings with calculated distances"""
    with app.app_context():
        print("\nSeeding campus paths...")

        # Paths based on actual GPS distances between buildings
        paths_data = [
            # From Admin Block (Main entrance)
            (1, 2, 135, 2),   # Admin to Library
            (1, 3, 110, 2),   # Admin to Civil
            (1, 4, 75, 1),    # Admin to CSE
            (1, 5, 45, 1),    # Admin to ECE
            (1, 6, 120, 2),   # Admin to Cafeteria

            # From Library
            (2, 4, 135, 2),   # Library to CSE
            (2, 6, 45, 1),    # Library to Cafeteria
            (2, 7, 90, 1),    # Library to Sports
            (2, 9, 55, 1),    # Library to Boys Hostel

            # From Civil Block
            (3, 4, 65, 1),    # Civil to CSE
            (3, 5, 95, 1),    # Civil to ECE
            (3, 8, 50, 1),    # Civil to Mech
            (3, 10, 50, 1),   # Civil to Girls Hostel

            # From CSE Block
            (4, 5, 40, 1),    # CSE to ECE
            (4, 8, 85, 1),    # CSE to Mech
            (4, 10, 45, 1),   # CSE to Girls Hostel
            (4, 11, 30, 1),   # CSE to Auditorium

            # From ECE Block
            (5, 11, 60, 1),   # ECE to Auditorium
            (5, 12, 90, 1),   # ECE to R&D

            # From Cafeteria
            (6, 7, 70, 1),    # Cafeteria to Sports
            (6, 9, 95, 1),    # Cafeteria to Boys Hostel

            # From Sports Complex
            (7, 9, 55, 1),    # Sports to Boys Hostel
            (7, 12, 95, 1),   # Sports to R&D

            # From Mech Block
            (8, 10, 60, 1),   # Mech to Girls Hostel
            (8, 12, 70, 1),   # Mech to R&D

            # From Boys Hostel
            (9, 6, 95, 1),    # Boys Hostel to Cafeteria
            (9, 2, 55, 1),    # Boys Hostel to Library

            # From Girls Hostel
            (10, 3, 50, 1),   # Girls Hostel to Civil
            (10, 4, 45, 1),   # Girls Hostel to CSE

            # From Auditorium
            (11, 4, 30, 1),   # Auditorium to CSE
            (11, 12, 120, 2), # Auditorium to R&D

            # From R&D
            (12, 3, 50, 1),   # R&D to Civil
            (12, 8, 70, 1),   # R&D to Mech
        ]

        for source_id, dest_id, distance, time in paths_data:
            path = Path(
                source_building_id=source_id,
                destination_building_id=dest_id,
                distance=distance,
                estimated_time=time
            )
            db.session.add(path)

        db.session.commit()
        print(f"✓ Added {len(paths_data)} campus paths")


def seed_users():
    """Add sample users"""
    with app.app_context():
        print("\nSeeding users...")

        users_data = [
            {
                'name': 'Admin User',
                'email': 'admin@drait.edu.in',
                'password': 'admin123',
                'role': 'admin',
                'department': 'Administration'
            },
            {
                'name': 'Rishika Yashwini',
                'email': 'rishika@drait.edu.in',
                'password': 'student123',
                'role': 'student',
                'department': 'Computer Science',
                'phone': '+91-9876543210'
            },
            {
                'name': 'Rajesh Kumar',
                'email': 'rajesh@drait.edu.in',
                'password': 'student123',
                'role': 'student',
                'department': 'Electronics',
                'phone': '+91-9876543211'
            },
            {
                'name': 'Dr. C Nanjundaswamy',
                'email': 'principal@drait.edu.in',
                'password': 'faculty123',
                'role': 'faculty',
                'department': 'Principal Office',
                'phone': '+91-9876543212'
            },
            {
                'name': 'Prof. Vijaya S',
                'email': 'vijaya@drait.edu.in',
                'password': 'faculty123',
                'role': 'faculty',
                'department': 'Civil Engineering',
                'phone': '+91-9876543213'
            }
        ]

        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit()
        print(f"✓ Added {len(users_data)} users")

        print("\n" + "="*60)
        print("DEFAULT LOGIN CREDENTIALS:")
        print("="*60)
        print("Admin: admin@drait.edu.in / admin123")
        print("Student: rishika@drait.edu.in / student123")
        print("Faculty: principal@drait.edu.in / faculty123")
        print("="*60)

def seed_sample_complaints():
    """Add sample complaints"""
    with app.app_context():
        print("\nSeeding sample complaints...")

        complaints_data = [
            {
                'user_id': 2,
                'title': 'WiFi Issues in CSE Lab',
                'description': 'WiFi connection is unstable in CSE Block computer lab.',
                'category': 'Technology',
                'priority': 'high',
                'status': 'open',
                'building_id': 4
            },
            {
                'user_id': 2,
                'title': 'Cleanliness in Cafeteria',
                'description': 'Tables need cleaning during lunch hours.',
                'category': 'Cleanliness',
                'priority': 'medium',
                'status': 'in_progress',
                'building_id': 6
            },
            {
                'user_id': 3,
                'title': 'Lab Equipment Maintenance',
                'description': 'Oscilloscopes in ECE lab need repair.',
                'category': 'Infrastructure',
                'priority': 'high',
                'status': 'open',
                'building_id': 5
            },
            {
                'user_id': 3,
                'title': 'Library AC Not Working',
                'description': 'AC on 2nd floor not cooling properly.',
                'category': 'Infrastructure',
                'priority': 'medium',
                'status': 'resolved',
                'building_id': 2
            }
        ]

        for complaint_data in complaints_data:
            complaint = Complaint(**complaint_data)
            db.session.add(complaint)

        db.session.commit()
        print(f"✓ Added {len(complaints_data)} sample complaints")


def seed_sample_feedback():
    """Add sample feedback"""
    with app.app_context():
        print("\nSeeding sample feedback...")

        feedback_data = [
            {
                'user_id': 2,
                'facility': 'Digital Library',
                'building_id': 2,
                'rating': 5,
                'comments': 'Excellent digital library with DELNET access.',
                'category': 'Library'
            },
            {
                'user_id': 2,
                'facility': 'Computer Lab',
                'building_id': 4,
                'rating': 4,
                'comments': 'Good systems, internet needs improvement.',
                'category': 'Laboratory'
            },
            {
                'user_id': 3,
                'facility': 'Cafeteria Food',
                'building_id': 6,
                'rating': 3,
                'comments': 'Food okay, needs more variety.',
                'category': 'Cafeteria'
            },
            {
                'user_id': 3,
                'facility': 'Sports Complex',
                'building_id': 7,
                'rating': 5,
                'comments': 'Excellent facilities!',
                'category': 'Sports Facility'
            }
        ]

        for feedback_entry in feedback_data:
            feedback = Feedback(**feedback_entry)
            db.session.add(feedback)

        db.session.commit()
        print(f"✓ Added {len(feedback_data)} sample feedback")


def main():
    """Main initialization"""
    print("="*80)
    print("DR. AMBEDKAR INSTITUTE OF TECHNOLOGY - DATABASE SETUP")
    print("CampXplore Version 0.1 - VERIFIED GPS COORDINATES")
    print("="*80)

    init_database()
    seed_buildings()
    seed_paths()
    seed_users()
    seed_sample_complaints()
    seed_sample_feedback()

    print("\n" + "="*80)
    print("✓ DATABASE INITIALIZATION COMPLETED!")
    print("="*80)
    print("\nCampus: Dr. Ambedkar Institute of Technology")
    print("Center: 12.963718°N, 77.506037°E (Verified)")
    print("Location: Outer Ring Road, Bangalore - 560056")
    print("\nAPI: http://localhost:5000")
    print("="*80)


if __name__ == '__main__':
    main()
