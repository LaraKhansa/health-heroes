from flask import Blueprint, render_template, request, session
from sqlalchemy import text
from db import db

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
def dashboard():
    # --- Language handling ---
    lang = request.args.get('lang')
    if lang:
        session['language'] = lang  # store chosen language
    language = session.get('language', 'en')  # fallback to English if not set

    # --- Screen-Free Activities Completed ---
    result = db.session.execute(text("SELECT COUNT(*) FROM activity_completions"))
    screen_free_activities = result.scalar() or 0

    # --- Healthy Meals Added ---
    result = db.session.execute(text("SELECT COUNT(*) FROM meals"))
    healthy_meals = result.scalar() or 0

    # --- Family streak days ---
    streak_days_result = db.session.execute(text("""
        SELECT COUNT(DISTINCT DATE(completed_at))
        FROM activity_completions
        WHERE completed_at >= DATE('now', '-7 day')
    """))
    streak_days = streak_days_result.scalar() or 0

    # --- Weekly Screen-Free Data ---
    weekly_query = db.session.execute(text("""
        SELECT strftime('%w', completed_at) AS weekday, COUNT(*) as count
        FROM activity_completions
        WHERE completed_at >= DATE('now', '-7 day')
        GROUP BY weekday
        ORDER BY weekday
    """))
    weekday_map = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    weekly_data = {day: 0 for day in weekday_map}
    for row in weekly_query:
        weekly_data[weekday_map[int(row[0])]] = row[1]

    # --- Monthly Screen-Free Data ---
    monthly_query = db.session.execute(text("""
        SELECT strftime('%W', completed_at) AS week, COUNT(*) as count
        FROM activity_completions
        WHERE strftime('%m', completed_at) = strftime('%m', 'now')
        GROUP BY week
        ORDER BY week
    """))
    monthly_data = {}
    for i, row in enumerate(monthly_query, start=1):
        monthly_data[f"Week {i}"] = row[1]

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
