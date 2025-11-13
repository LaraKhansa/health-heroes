"""
Dashboard Helper Functions
Functions to retrieve accurate family-specific data for the dashboard
"""

from db.models import db, ActivityCompletion, Meal, FamilyProfile
from sqlalchemy import func, distinct
from datetime import datetime, timedelta


def get_family_screen_free_activities_count(user_id):
    """
    Get the count of screen-free activities completed by this specific family.
    
    Args:
        user_id (int): The ID of the logged-in user
    
    Returns:
        int: Total number of activities completed by this user's family
    """
    # Count all activity completions for this specific user
    count = ActivityCompletion.query.filter_by(user_id=user_id).count()
    
    return count


def get_family_healthy_meals_count(user_id):
    """
    Get the count of healthy meals added by this specific family.
    
    Args:
        user_id (int): The ID of the logged-in user
    
    Returns:
        int: Total number of meals added by this user's family
    """
    # First, get the family profile for this user
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    # If no family profile exists, return 0
    if not family_profile:
        return 0
    
    # Count all meals for this family profile
    count = Meal.query.filter_by(family_profile_id=family_profile.id).count()
    
    return count


def get_family_streak_days(user_id):
    """
    Get the count of distinct days the family was active in the last 7 days.
    
    Args:
        user_id (int): The ID of the logged-in user
    
    Returns:
        int: Number of unique days with activities in the last 7 days
    """
    # Calculate date 7 days ago
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Count distinct dates where activities were completed
    count = db.session.query(
        func.date(ActivityCompletion.completed_at)
    ).filter(
        ActivityCompletion.user_id == user_id,
        ActivityCompletion.completed_at >= seven_days_ago
    ).distinct().count()
    
    return count


def get_family_weekly_data(user_id):
    """
    Get activity counts for each day of the week (last 7 days).
    
    Args:
        user_id (int): The ID of the logged-in user
    
    Returns:
        dict: Dictionary with weekday names as keys and counts as values
    """
    # Calculate date 7 days ago
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Query activities grouped by weekday
    results = db.session.query(
        func.strftime('%w', ActivityCompletion.completed_at).label('weekday'),
        func.count(ActivityCompletion.id).label('count')
    ).filter(
        ActivityCompletion.user_id == user_id,
        ActivityCompletion.completed_at >= seven_days_ago
    ).group_by('weekday').all()
    
    # Map weekday numbers to names
    weekday_map = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    
    # Initialize all days with 0
    weekly_data = {day: 0 for day in weekday_map}
    
    # Fill in actual counts
    for row in results:
        weekday_num = int(row.weekday)
        weekly_data[weekday_map[weekday_num]] = row.count
    
    return weekly_data


def get_family_monthly_data(user_id):
    """
    Get activity counts for each week of the current month.
    
    Args:
        user_id (int): The ID of the logged-in user
    
    Returns:
        dict: Dictionary with week labels as keys and counts as values
    """
    # Get current month/year
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    
    # Query activities grouped by week in current month
    results = db.session.query(
        func.strftime('%W', ActivityCompletion.completed_at).label('week'),
        func.count(ActivityCompletion.id).label('count')
    ).filter(
        ActivityCompletion.user_id == user_id,
        func.strftime('%m', ActivityCompletion.completed_at) == str(current_month).zfill(2),
        func.strftime('%Y', ActivityCompletion.completed_at) == str(current_year)
    ).group_by('week').all()
    
    # Build monthly data dictionary
    monthly_data = {}
    for i, row in enumerate(results, start=1):
        monthly_data[f"Week {i}"] = row.count
    
    return monthly_data
