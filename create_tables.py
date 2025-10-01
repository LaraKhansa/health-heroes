"""
Create/Update Database Tables
Run this script to create all database tables
"""

from main import app
from db.models import db, User, FamilyProfile, Child, ActivityCompletion, Activity

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("=" * 70)
        print("CREATING DATABASE TABLES")
        print("=" * 70)
        
        # Create all tables
        db.create_all()
        
        print("\n✅ Tables created successfully!")
        
        # Show existing data
        print("\n" + "=" * 70)
        print("DATABASE STATUS")
        print("=" * 70)
        
        print(f"\nUsers: {User.query.count()}")
        print(f"Family Profiles: {FamilyProfile.query.count()}")
        print(f"Children: {Child.query.count()}")
        print(f"Activities: {Activity.query.count()}")
        print(f"Activity Completions: {ActivityCompletion.query.count()}")
        
        print("\n" + "=" * 70)
        print("  ✅ COMPLETE!")
        print("=" * 70)

if __name__ == "__main__":
    create_tables()