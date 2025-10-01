"""
Database Models for Health Heroes
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    """
    User accounts for the application
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    family_profile = db.relationship('FamilyProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    activity_completions = db.relationship('ActivityCompletion', backref='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (exclude password)"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class FamilyProfile(db.Model):
    """
    Family profile - one per user
    Stores family information and preferences
    """
    __tablename__ = 'family_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Home resources (stored as JSON)
    home_resources = db.Column(db.Text)
    
    # Language preference
    language = db.Column(db.String(10), default='en')  # 'en' or 'ar'

    # Meal times (stored as strings in HH:MM format)
    breakfast_time = db.Column(db.String(5), default='07:00')
    lunch_time = db.Column(db.String(5), default='13:00')
    dinner_time = db.Column(db.String(5), default='19:00')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    children = db.relationship('Child', backref='family_profile', cascade='all, delete-orphan')
    
    # Helper methods for JSON fields
    def get_home_resources(self):
        """Get home resources as a list"""
        return json.loads(self.home_resources) if self.home_resources else []
    
    def set_home_resources(self, resources_list):
        """Set home resources from a list"""
        self.home_resources = json.dumps(resources_list)
    
    def to_dict(self):
        """Convert family profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'home_resources': self.get_home_resources(),
            'language': self.language,
            'breakfast_time': self.breakfast_time,
            'lunch_time': self.lunch_time,
            'dinner_time': self.dinner_time,
            'children_count': len(self.children),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
    def __repr__(self):
        return f'<FamilyProfile user_id={self.user_id}>'

class Child(db.Model):
    """
    Children in a family
    Stores child information for personalized activities
    """
    __tablename__ = 'children'
    
    id = db.Column(db.Integer, primary_key=True)
    family_profile_id = db.Column(db.Integer, db.ForeignKey('family_profiles.id'), nullable=False)
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20))
    
    # Interests and preferences (stored as JSON)
    interests = db.Column(db.Text)
    
    # Dietary restrictions/allergies (stored as JSON)
    dietary_restrictions = db.Column(db.Text)
    
    # Special needs or notes (optional)
    special_needs = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Helper methods for JSON fields
    def get_interests(self):
        """Get interests as a list"""
        return json.loads(self.interests) if self.interests else []
    
    def set_interests(self, interests_list):
        """Set interests from a list"""
        self.interests = json.dumps(interests_list)
    
    def get_dietary_restrictions(self):
        """Get dietary restrictions as a list"""
        return json.loads(self.dietary_restrictions) if self.dietary_restrictions else []
    
    def set_dietary_restrictions(self, restrictions_list):
        """Set dietary restrictions from a list"""
        self.dietary_restrictions = json.dumps(restrictions_list)
    
    def get_age(self):
        """Calculate current age from birthdate"""
        if not self.birthdate:
            return None
        today = datetime.utcnow().date()
        age = today.year - self.birthdate.year
        # Adjust if birthday hasn't occurred this year
        if today.month < self.birthdate.month or (today.month == self.birthdate.month and today.day < self.birthdate.day):
            age -= 1
        return age
    
    def get_age_range(self):
        """Get age range category for activities"""
        age = self.get_age()
        if age is None:
            return None
        
        if age < 2:
            return "0-2 years"
        elif age < 3:
            return "2-3 years"
        elif age < 5:
            return "3-5 years"
        elif age < 7:
            return "5-7 years"
        elif age <= 8:
            return "7-8 years"
        else:
            return "8+ years"
    
    def to_dict(self):
        """Convert child to dictionary"""
        return {
            'id': self.id,
            'family_profile_id': self.family_profile_id,
            'name': self.name,
            'birthdate': self.birthdate.isoformat() if self.birthdate else None,
            'age': self.get_age(),
            'age_range': self.get_age_range(),
            'gender': self.gender,
            'interests': self.get_interests(),
            'dietary_restrictions': self.get_dietary_restrictions(),
            'special_needs': self.special_needs,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Child {self.name} age {self.get_age()}>'
            
class Activity(db.Model):
    """
    Screen-free activities
    Pre-generated, global activities shown to all users
    """
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Bilingual title and description
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200), nullable=False)
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    
    # Activity metadata
    age_range = db.Column(db.String(50), nullable=False)  
    duration = db.Column(db.String(20), nullable=False)  
    category = db.Column(db.String(50), nullable=False)   
    
    # JSON fields (stored as text)
    materials = db.Column(db.Text)           
    steps_en = db.Column(db.Text)            
    steps_ar = db.Column(db.Text)           
    home_requirements = db.Column(db.Text)     
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Helper methods for JSON fields
    def get_materials(self):
        """Get materials as a list of dicts"""
        return json.loads(self.materials) if self.materials else []
    
    def set_materials(self, materials_list):
        """Set materials from a list of dicts"""
        self.materials = json.dumps(materials_list, ensure_ascii=False)
    
    def get_steps_en(self):
        """Get English steps as a list"""
        return json.loads(self.steps_en) if self.steps_en else []
    
    def set_steps_en(self, steps_list):
        """Set English steps from a list"""
        self.steps_en = json.dumps(steps_list, ensure_ascii=False)
    
    def get_steps_ar(self):
        """Get Arabic steps as a list"""
        return json.loads(self.steps_ar) if self.steps_ar else []
    
    def set_steps_ar(self, steps_list):
        """Set Arabic steps from a list"""
        self.steps_ar = json.dumps(steps_list, ensure_ascii=False)
    
    def get_home_requirements(self):
        """Get home requirements as a list"""
        return json.loads(self.home_requirements) if self.home_requirements else []
    
    def set_home_requirements(self, req_list):
        """Set home requirements from a list"""
        self.home_requirements = json.dumps(req_list)
    
    def to_dict(self, language='en'):
        """
        Convert activity to dictionary for API/frontend
        
        Args:
            language: 'en' or 'ar' for language preference
        
        Returns:
            dict with activity data
        """
        return {
            'id': self.id,
            'title': self.title_en if language == 'en' else self.title_ar,
            'title_en': self.title_en,
            'title_ar': self.title_ar,
            'description': self.description_en if language == 'en' else self.description_ar,
            'description_en': self.description_en,
            'description_ar': self.description_ar,
            'age_range': self.age_range,
            'duration': self.duration,
            'category': self.category,
            'materials': self.get_materials(),
            'steps': self.get_steps_en() if language == 'en' else self.get_steps_ar(),
            'steps_en': self.get_steps_en(),
            'steps_ar': self.get_steps_ar(),
            'home_requirements': self.get_home_requirements(),
        }
    
    def __repr__(self):
        return f'<Activity {self.title_en}>'

class ActivityCompletion(db.Model):
    """
    Track completed activities for users
    """
    __tablename__ = 'activity_completions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    # Which child did this activity (optional)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=True)
    
    # Completion details
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)  # Optional notes from parent
    
    # Rating (1-5 stars, optional)
    rating = db.Column(db.Integer)
    
    def to_dict(self):
        """Convert completion to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_id': self.activity_id,
            'child_id': self.child_id,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes,
            'rating': self.rating
        }
    
    def __repr__(self):
        return f'<ActivityCompletion user={self.user_id} activity={self.activity_id}>'