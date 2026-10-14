from flask import Blueprint, render_template, session
from app.decorators import login_required
from app.dashboard.dashboard_helpers import (
    get_family_screen_free_activities_count,
    get_family_healthy_meals_count,
    get_family_streak_days,
    get_family_weekly_data,
    get_family_monthly_data
)

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Family Dashboard - Shows accurate family-specific statistics
    """
    user_id = session.get('user_id')
    
    # --- Language handling ---
    language = session.get('language', 'en')
    
    # --- Get family-specific counts using helper functions ---
    
    # Screen-Free Activities Completed (for THIS family only)
    screen_free_activities = get_family_screen_free_activities_count(user_id)
    
    # Healthy Meals Added (for THIS family only)
    healthy_meals = get_family_healthy_meals_count(user_id)
    
    # Family streak days (for THIS family only)
    streak_days = get_family_streak_days(user_id)
    
    # Weekly Screen-Free Data (for THIS family only)
    weekly_data = get_family_weekly_data(user_id)
    
    # Monthly Screen-Free Data (for THIS family only)
    monthly_data = get_family_monthly_data(user_id)
    
    # Motivational tip
    motivational_tip = "Keep up the great work! Try 1 more veggie meal next week 🌱"

    return render_template(
        "dashboard.html",
        screen_free_activities=screen_free_activities,
        healthy_meals=healthy_meals,
        streak_days=streak_days,
        weekly_data=weekly_data,
        monthly_data=monthly_data,
        motivational_tip=motivational_tip,
        language=language,
        user_name=session.get('user_name', 'User')
    )