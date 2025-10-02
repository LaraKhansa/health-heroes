"""
Meal Recommender Routes
Handles meal recommendation and generation
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from db.models import db, User, FamilyProfile, Child, Meal
from app.meal_recommender.constants import INGREDIENTS, MEAL_TYPES
from app.meal_recommender.meal_generator import generate_meal, extract_ingredients

# Create blueprint
meals_bp = Blueprint(
    'meals',
    __name__,
    url_prefix='/meals',
    template_folder='templates',
    static_folder='static',
    static_url_path='/meals/static'
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


@meals_bp.route('/')
@login_required
def meals_home():
    """
    Main meals page - shows form to generate meals
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    # Get user name for display
    user_name = session.get('user_name', 'User')
    
    # Get language preference
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    
    # Get all children for profile context
    children = Child.query.filter_by(family_profile_id=family_profile.id).all() if family_profile else []
    
    return render_template(
        'meals_home.html',
        user_name=user_name,
        language=language,
        ingredients=INGREDIENTS,
        meal_types=MEAL_TYPES,
        children=children,
        family_profile=family_profile
    )


@meals_bp.route('/generate', methods=['POST'])
@login_required
def generate_meal_route(): 
    """
    Generate meal using Gemini AI
    Takes selected ingredients, meal type, and generates recipe
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    if not family_profile:
        flash('Please complete your family profile first', 'error')
        return redirect(url_for('profile.setup'))
    
    # Get form data
    selected_ingredients = request.form.getlist('ingredients')
    custom_ingredient = request.form.get('custom_ingredient', '').strip()
    meal_type = request.form.get('meal_type')
    cuisine_type = request.form.get('cuisine_type', 'arabic')  # NEW: Get cuisine type
    language = request.form.get('language', 'en')
    
    # Validation
    if not selected_ingredients and not custom_ingredient:
        if language == 'ar':
            flash('الرجاء اختيار مكون واحد على الأقل', 'error')
        else:
            flash('Please select at least one ingredient', 'error')
        return redirect(url_for('meals.meals_home', lang=language))
    
    if not meal_type:
        if language == 'ar':
            flash('الرجاء اختيار نوع الوجبة', 'error')
        else:
            flash('Please select a meal type', 'error')
        return redirect(url_for('meals.meals_home', lang=language))
    
    # Combine ingredients
    all_selected = selected_ingredients.copy()
    if custom_ingredient:
        # Split by comma if multiple custom ingredients
        custom_list = [ing.strip() for ing in custom_ingredient.split(',') if ing.strip()]
        all_selected.extend(custom_list)
    
    # Build child profiles for AI
    child_profiles = build_child_profiles(family_profile)
    all_dietary_restrictions = get_all_dietary_restrictions(family_profile)
    
    # Generate meal with AI
    try:
        meal_data = generate_meal(
            selected_ingredients=all_selected,
            meal_type=meal_type,
            cuisine_type=cuisine_type,  # NEW: Pass cuisine type
            child_profiles=child_profiles,
            dietary_restrictions=all_dietary_restrictions,
            language=language
        )
        
        # Save meal to database
        meal = save_meal_to_database(
            family_profile=family_profile,
            meal_data=meal_data,
            meal_type=meal_type,
            selected_ingredients=all_selected
        )
        
        # Success message
        if language == 'ar':
            flash('تم إنشاء الوجبة بنجاح! 🎉', 'success')
        else:
            flash('Meal generated successfully! 🎉', 'success')
        
        # Redirect to view the meal
        return redirect(url_for('meals.view_meal', meal_id=meal.id, lang=language))
        
    except Exception as e:
        print(f"❌ Error generating meal: {e}")
        if language == 'ar':
            flash('فشل في إنشاء الوجبة. الرجاء المحاولة مرة أخرى.', 'error')
        else:
            flash('Failed to generate meal. Please try again.', 'error')
        return redirect(url_for('meals.meals_home', lang=language))


@meals_bp.route('/view/<int:meal_id>')
@login_required
def view_meal(meal_id):
    """
    View a generated meal
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    meal = Meal.query.get_or_404(meal_id)
    
    # Check if meal belongs to user
    if meal.family_profile_id != family_profile.id:
        if family_profile.language == 'ar':
            flash('تم رفض الوصول', 'error')
        else:
            flash('Access denied', 'error')
        return redirect(url_for('meals.meals_home'))
    
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    user_name = session.get('user_name', 'User')
    
    return render_template(
        'view_meal.html',
        meal=meal,
        language=language,
        user_name=user_name
    )

@meals_bp.route('/regenerate/<int:meal_id>', methods=['POST'])
@login_required
def regenerate_meal(meal_id):
    """
    Regenerate a meal with user feedback
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    original_meal = Meal.query.get_or_404(meal_id)
    
    # Check if meal belongs to user
    if original_meal.family_profile_id != family_profile.id:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # Get feedback from request
    data = request.get_json()
    feedback = data.get('feedback', '').strip()
    language = data.get('language', 'en')
    
    if not feedback:
        return jsonify({'success': False, 'error': 'Feedback is required'})
    
    try:
        # Use the regeneration prompt
        from app.meal_recommender.prompts import get_meal_regeneration_prompt
        from google import genai
        from google.genai import types
        import os
        import json
        
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Get original meal data
        original_meal_data = {
            'name_en': original_meal.name_en,
            'ingredients': original_meal.get_ingredients()
        }
        
        prompt = get_meal_regeneration_prompt(
            original_meal=original_meal_data,
            feedback=feedback,
            language=language
        )
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=1.0,
                response_mime_type="application/json"
            )
        )
        
        meal_data = json.loads(response.text)
        
        # Update the existing meal instead of creating new one
        original_meal.name_en = meal_data['name_en']
        original_meal.name_ar = meal_data['name_ar']
        original_meal.instructions_en = meal_data['instructions_en']
        original_meal.instructions_ar = meal_data['instructions_ar']
        original_meal.prep_time = meal_data.get('prep_time', 'N/A')
        original_meal.cook_time = meal_data.get('cook_time', 'N/A')
        original_meal.nutritional_benefits_en = meal_data.get('nutritional_benefits_en', '')
        original_meal.nutritional_benefits_ar = meal_data.get('nutritional_benefits_ar', '')
        original_meal.why_healthy_en = meal_data.get('why_healthy_en', '')
        original_meal.why_healthy_ar = meal_data.get('why_healthy_ar', '')
        
        # Update ingredients
        ai_ingredients = extract_ingredients(meal_data)
        original_meal.set_ingredients(ai_ingredients)
        
        # Recalculate missing ingredients
        missing = original_meal.calculate_missing_ingredients()
        original_meal.set_missing_ingredients(missing)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Meal regenerated successfully!'})
        
    except Exception as e:
        print(f"Error regenerating meal: {e}")
        return jsonify({'success': False, 'error': str(e)})

@meals_bp.route('/history')
@login_required
def meal_history():
    """
    Show user's meal history
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    user_name = session.get('user_name', 'User')
    
    # Get all meals for this family, ordered by newest first
    meals = Meal.query.filter_by(
        family_profile_id=family_profile.id
    ).order_by(Meal.created_at.desc()).all()
    
    return render_template(
        'meal_history.html',
        meals=meals,
        language=language,
        user_name=user_name,
        meal_types=MEAL_TYPES
    )


@meals_bp.route('/favorite/<int:meal_id>', methods=['POST'])
@login_required
def toggle_favorite(meal_id):
    """
    Toggle favorite status of a meal
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    meal = Meal.query.get_or_404(meal_id)
    
    # Check if meal belongs to user
    if meal.family_profile_id != family_profile.id:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # Toggle favorite
    meal.is_favorite = not meal.is_favorite
    db.session.commit()
    
    return jsonify({'success': True, 'is_favorite': meal.is_favorite})


@meals_bp.route('/delete/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    """
    Delete a meal from history
    """
    user_id = session.get('user_id')
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    meal = Meal.query.get_or_404(meal_id)
    
    # Check if meal belongs to user
    if meal.family_profile_id != family_profile.id:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    try:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting meal: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete meal'})


# ============================================
# HELPER FUNCTIONS
# ============================================

def build_child_profiles(family_profile):
    """
    Build child profiles list for AI
    
    Args:
        family_profile: FamilyProfile object
    
    Returns:
        list of child profile dicts
    """
    children = Child.query.filter_by(family_profile_id=family_profile.id).all()
    child_profiles = []
    
    for child in children:
        child_profiles.append({
            "name": child.name,
            "age": child.get_age(),
            "dietary_restrictions": child.get_dietary_restrictions(),
            "special_needs": child.special_needs
        })
    
    return child_profiles


def get_all_dietary_restrictions(family_profile):
    """
    Get all dietary restrictions from all children
    
    Args:
        family_profile: FamilyProfile object
    
    Returns:
        list of unique dietary restrictions
    """
    children = Child.query.filter_by(family_profile_id=family_profile.id).all()
    all_restrictions = []
    
    for child in children:
        restrictions = child.get_dietary_restrictions()
        all_restrictions.extend(restrictions)
    
    # Remove duplicates and filter empty strings
    unique_restrictions = list(set(filter(None, all_restrictions)))
    
    return unique_restrictions


def save_meal_to_database(family_profile, meal_data, meal_type, selected_ingredients):
    """
    Save generated meal to database
    
    Args:
        family_profile: FamilyProfile object
        meal_data: dict from AI generation
        meal_type: meal type string
        selected_ingredients: list of ingredient names user selected
    
    Returns:
        Meal object
    """
    meal = Meal(
        family_profile_id=family_profile.id,
        name_en=meal_data['name_en'],
        name_ar=meal_data['name_ar'],
        meal_type=meal_type
    )
    
    # Set ingredients from AI response
    ai_ingredients = extract_ingredients(meal_data)
    meal.set_ingredients(ai_ingredients)
    
    # Set selected ingredients (what user had)
    selected_formatted = [{"name_en": ing, "name_ar": ing} for ing in selected_ingredients]
    meal.set_selected_ingredients(selected_formatted)
    
    # Calculate and set missing ingredients
    missing = meal.calculate_missing_ingredients()
    meal.set_missing_ingredients(missing)
    
    # Set other fields
    meal.instructions_en = meal_data.get('instructions_en', '')
    meal.instructions_ar = meal_data.get('instructions_ar', '')
    meal.prep_time = meal_data.get('prep_time', 'N/A')
    meal.cook_time = meal_data.get('cook_time', 'N/A')
    meal.nutritional_benefits_en = meal_data.get('nutritional_benefits_en', '')
    meal.nutritional_benefits_ar = meal_data.get('nutritional_benefits_ar', '')
    meal.why_healthy_en = meal_data.get('why_healthy_en', '')
    meal.why_healthy_ar = meal_data.get('why_healthy_ar', '')
    
    db.session.add(meal)
    db.session.commit()
    
    return meal