"""
Database Models for Health Heroes
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


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