"""
Authentication Routes
Handles user registration, login, and logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.models import db, User, FamilyProfile
from datetime import datetime

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
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create empty family profile
        family_profile = FamilyProfile(user_id=user.id)
        db.session.add(family_profile)
        db.session.commit()

        # Log the user in automatically
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email

        flash('Welcome to Health Heroes! Let\'s set up your family profile.', 'success')
        return redirect(url_for('profile.setup'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        # Login successful - create session
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        
        # Update last login
        user.last_login = datetime.utcnow()
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