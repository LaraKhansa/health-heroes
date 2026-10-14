"""
Health Heroes - Main Application Entry Point
"""

import os
import secrets
from flask import Flask, render_template, redirect, url_for, session, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
IS_PRODUCTION = os.getenv('APP_ENV', 'development').lower() == 'production'

secret_key = os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY')
if not secret_key:
    if IS_PRODUCTION:
        raise RuntimeError('SECRET_KEY must be set when APP_ENV=production')
    print("⚠️  SECRET_KEY is not set. Using a temporary key, so logins reset when the app restarts.")
    secret_key = secrets.token_hex(32)
app.secret_key = secret_key

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1 MB request limit

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'health_heroes.db')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{database_path}')
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
    if language not in ('en', 'ar'):
        language = 'en'

    # Update language in session if changed
    session['language'] = language
    if family_profile and family_profile.language != language:
        family_profile.language = language
        from db import db
        db.session.commit()

    return render_template('home.html', user_name=user_name, language=language)


@app.route('/healthz')
def health_check():
    """Health check for hosting platforms"""
    return {'status': 'ok'}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404, language=session.get('language', 'en')), 404


@app.errorhandler(500)
def internal_error(error):
    from db import db
    db.session.rollback()
    return render_template('error.html', code=500, language=session.get('language', 'en')), 500


if __name__ == '__main__':
    print("=" * 70)
    print("  🌟 HEALTH HEROES - Starting Application")
    print("=" * 70)
    debug = os.getenv('FLASK_DEBUG', '0' if IS_PRODUCTION else '1') == '1'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug, host=os.getenv('HOST', '127.0.0.1'), port=port)
