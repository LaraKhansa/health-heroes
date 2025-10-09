"""
Health Heroes - Main Application Entry Point
"""

import os
from flask import Flask, render_template, redirect, url_for, session
from dotenv import load_dotenv
from flask import request

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'health_heroes.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
from db import init_db
init_db(app)

# Register blueprints
from app.auth.routes import auth_bp
from app.profile.routes import profile_bp
from app.meal_recommender.routes import meals_bp
from app.screen_free_activities.routes import screen_free_bp
from app.chatbot.routes import chatbot_bp
from app.dashboard.routes import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(meals_bp)
app.register_blueprint(screen_free_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(dashboard_bp, url_prefix="/")

# Home route
@app.route('/')
def home_page():
    # Check if user is logged in
    user_name = session.get('user_name', None)
    user_id = session.get('user_id', None)
    
    # If not logged in, redirect to login
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Get language from query params or session
    from db.models import FamilyProfile
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    
    # Update language in session if changed
    if language:
        session['language'] = language
        if family_profile:
            family_profile.language = language
            from db import db
            db.session.commit()
    
    return render_template('home.html', user_name=user_name, language=language)

if __name__ == '__main__':
    print("=" * 70)
    print("  🌟 HEALTH HEROES - Starting Application")
    print("=" * 70)
    app.run(debug=True, port=5000)

