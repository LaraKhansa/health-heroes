"""
Authentication Routes
Handles user registration, login, and logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.models import db, User, FamilyProfile, utcnow
from sqlalchemy import func

MIN_PASSWORD_LENGTH = 8


def find_user_by_email(email):
    """Case-insensitive email lookup"""
    return User.query.filter(func.lower(User.email) == email.lower()).first()


def start_session(user):
    """Log the user in with a fresh session"""
    language = session.get('language')
    session.clear()
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['user_email'] = user.email
    if user.family_profile and user.family_profile.language:
        session['language'] = user.family_profile.language
    elif language:
        session['language'] = language

# Create blueprint
auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    template_folder='templates'
)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration page
    """
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm_password = request.form.get('confirm_password') or ''
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(name) > 100 or len(email) > 120 or '@' not in email:
            flash('Please enter a valid name and email address', 'error')
            return render_template('register.html')
        
        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f'Password must be at least {MIN_PASSWORD_LENGTH} characters', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = find_user_by_email(email)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create empty family profile
        family_profile = FamilyProfile(user_id=user.id, language=session.get('language', 'en'))
        db.session.add(family_profile)
        db.session.commit()

        # Log the user in automatically
        start_session(user)

        flash('Welcome to Afiyah! Let\'s set up your family profile.', 'success')
        return redirect(url_for('profile.setup'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page
    """
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''
        
        # Validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        # Find user
        user = find_user_by_email(email)
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        # Login successful - create session
        start_session(user)
        
        # Update last login
        user.last_login = utcnow()
        db.session.commit()
        
        flash(f'Welcome back, {user.name}!', 'success')
        return redirect(url_for('home_page'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    User logout
    """
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))