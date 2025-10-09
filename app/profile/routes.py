"""
Profile Management Routes
Handles family profile setup and management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.models import db, User, FamilyProfile, Child
from datetime import datetime

# Create blueprint
profile_bp = Blueprint(
    'profile',
    __name__,
    url_prefix='/profile',
    template_folder='templates',
    static_folder='static',
    static_url_path='/profile/static'
)


def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@profile_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """
    Initial family profile setup (one-time wizard)
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    if request.method == 'POST':
        # Get form data
        home_resources = request.form.getlist('home_resources')
        language = request.form.get('language', 'en')
        breakfast_time = request.form.get('breakfast_time', '07:00')
        lunch_time = request.form.get('lunch_time', '13:00')
        dinner_time = request.form.get('dinner_time', '19:00')
        
        # Update family profile
        family_profile.set_home_resources(home_resources)
        family_profile.language = language
        family_profile.breakfast_time = breakfast_time
        family_profile.lunch_time = lunch_time
        family_profile.dinner_time = dinner_time
        
        db.session.commit()
        
        # Update session language
        session['language'] = language
        
        flash('Family profile setup complete!', 'success')
        return redirect(url_for('profile.add_child'))
    
    return render_template('setup.html', user=user, family_profile=family_profile)


@profile_bp.route('/add-child', methods=['GET', 'POST'])
@login_required
def add_child():
    """
    Add a child to the family
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        birthdate_str = request.form.get('birthdate')
        gender = request.form.get('gender')
        interests = request.form.getlist('interests')
        dietary_restrictions = request.form.getlist('dietary_restrictions')
        other_allergies = request.form.get('other_allergies', '').strip()
        special_needs = request.form.get('special_needs', '').strip()
    
        # Process other allergies (comma-separated)
        if other_allergies:
            # Split by comma, strip whitespace, and add to dietary_restrictions list
            other_allergies_list = [allergy.strip() for allergy in other_allergies.split(',') if allergy.strip()]
            dietary_restrictions.extend(other_allergies_list)
        
        # Validation
        if not name or not birthdate_str or not gender:
            flash('Name, birthdate, and gender are required', 'error')
            return render_template('add_child.html', family_profile=family_profile)
        
        # Parse birthdate
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid birthdate format', 'error')
            return render_template('add_child.html', family_profile=family_profile)
        
        # Create child
        child = Child(
            family_profile_id=family_profile.id,
            name=name,
            birthdate=birthdate,
            gender=gender,
            special_needs=special_needs if special_needs else None
        )
        
        child.set_interests(interests)
        child.set_dietary_restrictions(dietary_restrictions)
        
        db.session.add(child)
        db.session.commit()
        
        flash(f'{name} added successfully!', 'success')
        
        # Ask if they want to add another child
        add_another = request.form.get('add_another')
        if add_another == 'yes':
            return redirect(url_for('profile.add_child'))
        else:
            return redirect(url_for('home_page'))
    
    return render_template('add_child.html', family_profile=family_profile)


@profile_bp.route('/view')
@login_required
def view_profile():
    """
    View and manage family profile
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    children = Child.query.filter_by(family_profile_id=family_profile.id).all()
    
    return render_template('profile.html', user=user, family_profile=family_profile, children=children)