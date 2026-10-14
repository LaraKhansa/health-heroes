"""
Activity Generator for Health Heroes
Uses Gemini AI to generate bilingual (Arabic/English) activities
Cultural context: UAE/Islamic values
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

from app.ai_client import generate_json
from utils.constants import HOME_AREAS, ACTIVITY_CATEGORIES, AGE_RANGES
from utils.prompts import get_batch_activity_generation_prompt

# Load environment variables
load_dotenv()

# A stronger model gives better activities; this only runs once when seeding
ACTIVITY_MODEL = os.getenv('ACTIVITY_MODEL', 'gemini-2.5-pro')


def generate_activities_batch(home_area, category, age_range, num_activities, retry_count=0):
    """
    Generate a single bilingual activity using Gemini AI
    
    Args:
        home_area: Key from HOME_AREAS (e.g., "kitchen")
        category: Key from ACTIVITY_CATEGORIES (e.g., "cooking")
        age_range: Age range string (e.g., "3-5 years")
        retry_count: Number of retries attempted (internal use)
    
    Returns:
        dict: Activity data with bilingual content, or None if failed
    """
    
    # Get the prompt
    prompt = get_batch_activity_generation_prompt(home_area, category, age_range, num_activities)
    
    try:
        # Generate content with Gemini
        print(f"Generating {num_activities} activities...")
        data = generate_json(prompt, temperature=1.0, model=ACTIVITY_MODEL)
        
        # Validate structure
        if not isinstance(data, dict) or 'activities' not in data:
            raise ValueError("Missing 'activities' array in response")
        
        activities_list = data['activities']
        
        if len(activities_list) != num_activities:
            print(f"Expected {num_activities} activities, got {len(activities_list)}")
        
        # Validate and enhance each activity
        valid_activities = []
        for idx, activity_data in enumerate(activities_list):
            # Validate required fields
            required_fields = [
                'title_en', 'title_ar', 'description_en', 'description_ar',
                'duration', 'age_range', 'materials', 'steps_en', 'steps_ar'
            ]
            
            missing_fields = [field for field in required_fields if field not in activity_data]
            
            if missing_fields:
                print(f"Activity {idx+1} missing fields: {missing_fields}")
                continue
            
            # Add metadata
            activity_data['category'] = category
            activity_data['age_range'] = age_range
            activity_data['home_area'] = home_area
            
            valid_activities.append(activity_data)
            print(f"Activity {idx+1}: {activity_data['title_en']}")
        
        if len(valid_activities) == 0:
            raise ValueError("No valid activities generated")
        
        return valid_activities
        
    except Exception as e:
        print(f"  ❌ Generation Error: {e}")
        
        # Retry logic
        if retry_count < 2:
            print(f"  🔄 Retrying... (attempt {retry_count + 1})")
            time.sleep(3)
            return generate_activities_batch(home_area, category, age_range, num_activities, retry_count + 1)
        
        return []


def generate_all_activities(activities_per_combination=5):
    """
    Generate all activities for all combinations
    Now generates in batches for better variety and speed
    
    Args:
        activities_per_combination: Number of activities per combination (default: 5)
    
    Returns:
        list: List of all successfully generated activity dictionaries
    """
    all_activities = []
    
    # Calculate totals
    total_combinations = len(HOME_AREAS) * len(ACTIVITY_CATEGORIES) * len(AGE_RANGES)
    total_to_generate = total_combinations * activities_per_combination
    
    # Statistics
    current = 0
    total_successful = 0
    total_failed_combinations = 0
    
    # Header
    print("=" * 70)
    print("  🌟 HEALTH HEROES - BATCH ACTIVITY GENERATION 🌟")
    print("=" * 70)
    print(f"📊 Total combinations: {total_combinations}")
    print(f"📊 Activities per combination: {activities_per_combination}")
    print(f"📊 Total activities to generate: {total_to_generate}")
    print(f"🌍 Languages: Arabic (العربية) + English")
    print(f"🇦🇪 Cultural context: UAE/Islamic values")
    print(f"⚡ Method: Batch generation (faster & better variety)")
    print("=" * 70)
    
    start_time = time.time()
    
    # Generate for each combination
    for home_area in HOME_AREAS.keys():
        for category in ACTIVITY_CATEGORIES.keys():
            for age_range in AGE_RANGES:
                current += 1
                
                # Display current combination
                location_en = HOME_AREAS[home_area]["en"]
                category_en = ACTIVITY_CATEGORIES[category]["en"]
                
                print(f"\n[{current}/{total_combinations}] 📍 {location_en} | 🎯 {category_en} | 👶 {age_range}")
                print("-" * 70)
                
                # Generate batch of activities
                activities_batch = generate_activities_batch(
                    home_area, 
                    category, 
                    age_range,
                    num_activities=activities_per_combination
                )
                
                if activities_batch:
                    all_activities.extend(activities_batch)
                    total_successful += len(activities_batch)
                    print(f"  ✅ Successfully generated {len(activities_batch)} activities")
                else:
                    total_failed_combinations += 1
                    print(f"  ❌ Failed to generate activities for this combination")
                
                # Delay to avoid rate limiting
                time.sleep(1.5)

                # Every 40 requests, wait extra time
                if current % 40 == 0:
                    print(f"\n⏸️  Rate limit protection: Pausing for 70 seconds...")
                    print(f"   (Gemini Free Tier: 50 requests/minute)")
                    time.sleep(70)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    # Summary
    print("\n" + "=" * 70)
    print("  🎉 GENERATION COMPLETE! 🎉")
    print("=" * 70)
    print(f"✅ Successfully generated: {total_successful} activities")
    print(f"❌ Failed combinations: {total_failed_combinations}")
    print(f"📈 Success rate: {(total_successful/total_to_generate)*100:.1f}%")
    print(f"⏱️  Time taken: {minutes} minutes {seconds} seconds")
    print(f"⚡ Average: {elapsed_time/total_combinations:.1f} seconds per combination")
    print(f"💾 Ready to save to database!")
    print("=" * 70)
    
    return all_activities


def test_batch_generation():
    """
    Test generating a batch of activities
    """
    print("🧪 Testing batch activity generation...\n")
    
    activities = generate_activities_batch("kitchen", "cooking", "3-5 years", num_activities=3)
    
    if activities:
        print("\n" + "=" * 70)
        print(f"✅ TEST SUCCESSFUL! Generated {len(activities)} activities")
        print("=" * 70)
        for idx, activity in enumerate(activities):
            print(f"\n--- Activity {idx+1} ---")
            print(f"EN: {activity['title_en']}")
            print(f"AR: {activity['title_ar']}")
        return True
    else:
        print("\n❌ TEST FAILED!")
        return False


if __name__ == "__main__":
    # Run test when script is executed directly
    test_batch_generation()