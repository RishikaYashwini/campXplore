"""
CampXplore - Interactive Building Reassignment Tool
Manually fix wrong building references in complaints and feedback
"""

from app import app
from extensions import db
from models.building import Building
from models.complaint import Complaint
from models.feedback import Feedback

def display_all_buildings():
    """Display all available buildings for reference"""
    with app.app_context():
        buildings = Building.query.order_by(Building.building_id).all()

        print("\n" + "="*70)
        print("AVAILABLE BUILDINGS (for reference)")
        print("="*70)
        print(f"{'ID':<5} {'Building Name':<50}")
        print("-"*70)

        for b in buildings:
            print(f"{b.building_id:<5} {b.name[:48]:<50}")

        print("="*70)

        return buildings

def fix_complaints():
    """Interactive fixing of complaints"""
    print("\n" + "="*70)
    print("FIXING COMPLAINTS")
    print("="*70)

    with app.app_context():
        complaints = Complaint.query.all()

        if not complaints:
            print("No complaints found in database.")
            return

        print(f"\nTotal complaints to review: {len(complaints)}")
        print("-"*70)

        buildings = {b.building_id: b.name for b in Building.query.all()}
        changes_made = 0

        for i, complaint in enumerate(complaints, 1):
            current_building_name = buildings.get(complaint.building_id, "UNKNOWN BUILDING")

            print(f"\n[Complaint {i}/{len(complaints)}]")
            print(f"  Complaint ID: {complaint.complaint_id}")
            print(f"  Title: {complaint.title}")
            print(f"  Description: {complaint.description[:100]}...")
            print(f"  Category: {complaint.category}")
            print(f"  Current Building ID: {complaint.building_id}")
            print(f"  Current Building Name: {current_building_name}")
            print(f"  Status: {complaint.status}")

            # Ask if user wants to change
            print("\n  Options:")
            print("    [Enter] - Keep current building")
            print("    [number] - Change to building ID number")
            print("    [s] - Skip (same as Enter)")
            print("    [q] - Save and quit")
            print("    [h] - Show building list again")

            choice = input("\n  Your choice: ").strip().lower()

            if choice == 'q':
                print("\n  Saving changes and quitting...")
                db.session.commit()
                break
            elif choice == 'h':
                display_all_buildings()
                choice = input("\n  Enter new building ID (or press Enter to skip): ").strip()
            elif choice == '' or choice == 's':
                print("  → Keeping current building")
                continue

            # Try to parse as building ID
            try:
                new_building_id = int(choice)
                if new_building_id in buildings:
                    complaint.building_id = new_building_id
                    print(f"  ✓ Changed to: {buildings[new_building_id]}")
                    changes_made += 1
                else:
                    print(f"  ✗ Invalid building ID: {new_building_id}")
            except ValueError:
                print(f"  ✗ Invalid input: {choice}")

        # Final save
        db.session.commit()
        print(f"\n✓ Complaints updated: {changes_made} changes made")

def fix_feedbacks():
    """Interactive fixing of feedbacks"""
    print("\n" + "="*70)
    print("FIXING FEEDBACKS")
    print("="*70)

    with app.app_context():
        feedbacks = Feedback.query.all()

        if not feedbacks:
            print("No feedbacks found in database.")
            return

        print(f"\nTotal feedbacks to review: {len(feedbacks)}")
        print("-"*70)

        buildings = {b.building_id: b.name for b in Building.query.all()}
        changes_made = 0

        for i, feedback in enumerate(feedbacks, 1):
            current_building_name = buildings.get(feedback.building_id, "UNKNOWN BUILDING")

            print(f"\n[Feedback {i}/{len(feedbacks)}]")
            print(f"  Feedback ID: {feedback.feedback_id}")
            print(f"  Facility: {feedback.facility}")
            print(f"  Rating: {feedback.rating}/5")
            print(f"  Comments: {feedback.comments[:100] if feedback.comments else 'None'}...")
            print(f"  Category: {feedback.category}")
            print(f"  Current Building ID: {feedback.building_id}")
            print(f"  Current Building Name: {current_building_name}")

            # Ask if user wants to change
            print("\n  Options:")
            print("    [Enter] - Keep current building")
            print("    [number] - Change to building ID number")
            print("    [s] - Skip (same as Enter)")
            print("    [q] - Save and quit")
            print("    [h] - Show building list again")

            choice = input("\n  Your choice: ").strip().lower()

            if choice == 'q':
                print("\n  Saving changes and quitting...")
                db.session.commit()
                break
            elif choice == 'h':
                display_all_buildings()
                choice = input("\n  Enter new building ID (or press Enter to skip): ").strip()
            elif choice == '' or choice == 's':
                print("  → Keeping current building")
                continue

            # Try to parse as building ID
            try:
                new_building_id = int(choice)
                if new_building_id in buildings:
                    feedback.building_id = new_building_id
                    print(f"  ✓ Changed to: {buildings[new_building_id]}")
                    changes_made += 1
                else:
                    print(f"  ✗ Invalid building ID: {new_building_id}")
            except ValueError:
                print(f"  ✗ Invalid input: {choice}")

        # Final save
        db.session.commit()
        print(f"\n✓ Feedbacks updated: {changes_made} changes made")

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("  CampXplore - Building Reassignment Tool")
    print("  Fix wrong building references in complaints and feedback")
    print("="*70)

    # Display buildings first
    display_all_buildings()

    print("\n\nWhat would you like to fix?")
    print("  1. Fix Complaints")
    print("  2. Fix Feedbacks")
    print("  3. Fix Both (Complaints first, then Feedbacks)")
    print("  q. Quit")

    choice = input("\nYour choice: ").strip().lower()

    if choice == '1':
        fix_complaints()
    elif choice == '2':
        fix_feedbacks()
    elif choice == '3':
        fix_complaints()
        input("\nPress Enter to continue to Feedbacks...")
        fix_feedbacks()
    elif choice == 'q':
        print("\nExiting...")
        return
    else:
        print("\nInvalid choice. Exiting...")
        return

    print("\n" + "="*70)
    print("  ✓✓✓ FIXING COMPLETED! ✓✓✓")
    print("="*70)
    print("\nAll changes have been saved to the database.")
    print("Restart your backend server to see the updates.")

if __name__ == '__main__':
    main()
