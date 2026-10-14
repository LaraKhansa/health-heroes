"""
Database Population Script
Generate activities with AI and save to database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse

from main import app
from db.models import db, Activity
from db.seed import build_activity, load_seed_activities


def save_activities_to_database(activities_data):
    """
    Save generated activities to database
    
    Args:
        activities_data: List of activity dictionaries
    
    Returns:
        Number of successfully saved activities
    """
    print(f"\nSaving {len(activities_data)} activities to database...")
    print("-" * 70)
    
    saved_count = 0
    
    for idx, activity_data in enumerate(activities_data, 1):
        try:
            db.session.add(build_activity(activity_data))
            saved_count += 1
            
            # Commit in batches of 10
            if saved_count % 10 == 0:
                db.session.commit()
                print(f"Saved {saved_count} activities...")
                
        except Exception as e:
            # A malformed activity fails before it is added, so earlier ones are unaffected
            print(f"Error saving activity {idx}: {e}")
            continue
    
    # Final commit
    db.session.commit()
    
    print("-" * 70)
    print(f"Successfully saved: {saved_count} activities")
    
    return saved_count


def populate_database(activities_per_combination=5):
    """
    Main function: Generate and save activities
    """
    from utils.activity_generator import generate_all_activities
    
    with app.app_context():
        print("=" * 70)
        print("HEALTH HEROES - ACTIVITY GENERATION")
        print("=" * 70)
        
        # Generate first so a failed run never leaves the database empty
        print("\nStarting AI generation...")
        print("=" * 70)
        activities_data = generate_all_activities(activities_per_combination)
        
        if not activities_data:
            print("\nNo activities generated! Existing activities were kept.")
            return
        
        # Clear old activities
        print("\nClearing old activities...")
        old_count = Activity.query.count()
        if old_count > 0:
            Activity.query.delete()
            db.session.commit()
            print(f"Cleared {old_count} old activities")
        else:
            print("Database is empty")
        
        # Save to database
        print("\n" + "=" * 70)
        saved_count = save_activities_to_database(activities_data)
        
        # Final summary
        print("\n" + "=" * 70)
        print("  🎉 COMPLETE!")
        print("=" * 70)
        print(f"Total activities in database: {Activity.query.count()}")
        print("=" * 70)


def show_statistics():
    """Show database statistics"""
    with app.app_context():
        total = Activity.query.count()
        
        if total == 0:
            print("\n📊 Database is empty. Run generation first!")
            return
        
        print("\n" + "=" * 70)
        print("  📊 DATABASE STATISTICS")
        print("=" * 70)
        print(f"📊 Total activities: {total}")
        
        # Count by category
        from utils.constants import ACTIVITY_CATEGORIES
        print("\n📁 By Category:")
        for category in ACTIVITY_CATEGORIES.keys():
            count = Activity.query.filter_by(category=category).count()
            category_name = ACTIVITY_CATEGORIES[category]['en']
            print(f"  - {category_name}: {count}")
        
        # Count by age range
        from utils.constants import AGE_RANGES
        print("\n👶 By Age Range:")
        for age_range in AGE_RANGES:
            count = Activity.query.filter_by(age_range=age_range).count()
            print(f"  - {age_range}: {count}")
        
        print("=" * 70)


def reset_to_seed():
    """Replace all activities with the bundled starter set"""
    with app.app_context():
        Activity.query.delete()
        db.session.commit()
        count = load_seed_activities()
        print(f"🌱 Loaded {count} starter activities")


if __name__ == "__main__":
    from utils.constants import HOME_AREAS, ACTIVITY_CATEGORIES, AGE_RANGES
    
    parser = argparse.ArgumentParser(description="Manage the activities database")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--generate', type=int, metavar='N',
                       help='Generate N activities per combination with Gemini (replaces existing activities)')
    group.add_argument('--seed', action='store_true',
                       help='Replace existing activities with the bundled starter set (no API key needed)')
    group.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--yes', action='store_true', help='Skip the confirmation prompt')
    args = parser.parse_args()
    
    if args.stats:
        show_statistics()
    elif args.seed:
        reset_to_seed()
    else:
        num = max(1, min(args.generate, 10))
        total_combinations = len(HOME_AREAS) * len(ACTIVITY_CATEGORIES) * len(AGE_RANGES)
        print(f"\n🎯 Will generate up to {total_combinations * num} activities "
              f"with {total_combinations} API calls")
        
        if args.yes or input("\nProceed? (yes/no): ").strip().lower() in ['yes', 'y']:
            populate_database(activities_per_combination=num)
        else:
            print("❌ Cancelled")
