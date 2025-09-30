"""
Database Population Script
Generate activities with AI and save to database
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from db.models import db, Activity
from utils.activity_generator import generate_all_activities


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
            # Create Activity object
            activity = Activity(
                title_en=activity_data['title_en'],
                title_ar=activity_data['title_ar'],
                description_en=activity_data['description_en'],
                description_ar=activity_data['description_ar'],
                age_range=activity_data['age_range'],
                duration=activity_data['duration'],
                category=activity_data['category']
            )
            
            # Set JSON fields
            activity.set_materials(activity_data['materials'])
            activity.set_steps_en(activity_data['steps_en'])
            activity.set_steps_ar(activity_data['steps_ar'])
            activity.set_home_requirements([activity_data['home_area']])
            
            db.session.add(activity)
            saved_count += 1
            
            # Commit in batches of 10
            if saved_count % 10 == 0:
                db.session.commit()
                print(f"Saved {saved_count} activities...")
                
        except Exception as e:
            print(f"Error saving activity {idx}: {e}")
            db.session.rollback()
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
    with app.app_context():
        print("=" * 70)
        print("HEALTH HEROES - ACTIVITY GENERATION")
        print("=" * 70)
        
        # Clear old activities
        print("\nClearing old activities...")
        old_count = Activity.query.count()
        if old_count > 0:
            Activity.query.delete()
            db.session.commit()
            print(f"Cleared {old_count} old activities")
        else:
            print("Database is empty")
        
        # Generate activities with AI
        print("\nStarting AI generation...")
        print("=" * 70)
        activities_data = generate_all_activities(activities_per_combination)
        
        if not activities_data:
            print("\nNo activities generated! Aborting...")
            return
        
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


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🌟 HEALTH HEROES - ACTIVITY DATABASE MANAGER")
    print("=" * 70)
    print("\nOptions:")
    print("1. Generate and save activities")
    print("2. Show statistics")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        try:
            num = input("\nActivities per combination (1-5, recommended 3): ").strip()
            num = int(num) if num else 3
            if num < 1 or num > 10:
                print("⚠️  Using default: 3")
                num = 3
        except:
            num = 3
        
        # Show estimate
        from utils.constants import HOME_AREAS, ACTIVITY_CATEGORIES, AGE_RANGES
        total_combinations = len(HOME_AREAS) * len(ACTIVITY_CATEGORIES) * len(AGE_RANGES)
        total_activities = total_combinations * num
        estimated_time = total_combinations * 3 // 60
        
        print(f"\n🎯 Will generate: {total_activities} activities")
        print(f"⏱️  Estimated time: ~{estimated_time} minutes")
        
        confirm = input("\nProceed? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            populate_database(activities_per_combination=num)
        else:
            print("❌ Cancelled")
    
    elif choice == "2":
        show_statistics()
    
    else:
        print("👋 Goodbye!")