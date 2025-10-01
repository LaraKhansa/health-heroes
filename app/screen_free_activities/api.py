from flask import Blueprint, jsonify
from db.models import Activity, ActivityCompletion
from db import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/activities", methods=["GET"])
def get_activities():
    """Return all activities as JSON (default English)."""
    activities = Activity.query.all()
    return jsonify([a.to_dict(language="en") for a in activities])

@api_bp.route("/api/activities/completed/<int:user_id>", methods=["GET"])
def get_user_completions(user_id):
    """Return activities completed by a user."""
    completions = ActivityCompletion.query.filter_by(user_id=user_id).all()
    return jsonify([c.to_dict() for c in completions])

@api_bp.route("/api/screen-time/weekly", methods=["GET"])
def get_screen_time():
    """
    Mock endpoint for screen time (since no ScreenTime model exists).
    Replace this later with real DB queries once you add ScreenTime.
    """
    # Example weekly data
    daily_hours = [2, 1, 3, 2, 4, 0, 1]  # Mon-Sun
    return jsonify({
        "total_hours": sum(daily_hours),
        "daily_hours": daily_hours
    })
