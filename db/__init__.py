"""
Database initialization
"""

from db.models import db, Activity, User, FamilyProfile, Child, ActivityCompletion


def init_db(app):
    """
    Initialize database with Flask app
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database initialized!")