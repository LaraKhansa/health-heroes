"""
Starter data for a fresh database
"""

import json
import os

from db.models import db, Activity

SEED_ACTIVITIES_PATH = os.path.join(os.path.dirname(__file__), 'seed_activities.json')


def build_activity(activity_data):
    """Create an Activity from a generated or seed activity dict"""
    activity = Activity(
        title_en=activity_data['title_en'],
        title_ar=activity_data['title_ar'],
        description_en=activity_data['description_en'],
        description_ar=activity_data['description_ar'],
        age_range=activity_data['age_range'],
        duration=activity_data['duration'],
        category=activity_data['category']
    )
    activity.set_materials(activity_data['materials'])
    activity.set_steps_en(activity_data['steps_en'])
    activity.set_steps_ar(activity_data['steps_ar'])
    activity.set_home_requirements([activity_data['home_area']])
    return activity


def load_seed_activities():
    """Add the bundled starter activities. Returns how many were added."""
    with open(SEED_ACTIVITIES_PATH, encoding='utf-8') as f:
        activities_data = json.load(f)
    
    for activity_data in activities_data:
        db.session.add(build_activity(activity_data))
    db.session.commit()
    
    return len(activities_data)


def seed_activities_if_empty():
    """Load starter activities so the activities page works out of the box"""
    if Activity.query.first() is None:
        count = load_seed_activities()
        print(f"🌱 Added {count} starter activities")
