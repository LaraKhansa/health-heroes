"""
AI Meal Generator
Handles all AI-related meal generation logic
"""

from app.ai_client import generate_json
from app.meal_recommender.prompts import get_meal_generation_prompt, get_meal_regeneration_prompt


def generate_meal(selected_ingredients, meal_type, cuisine_type, child_profiles, dietary_restrictions, language='en'):
    """
    Generate meal using Gemini AI
    
    Args:
        selected_ingredients: list of ingredient names
        meal_type: breakfast, lunch, dinner, snack, dessert
        cuisine_type: arabic or international
        child_profiles: list of child profile dicts
        dietary_restrictions: list of dietary restrictions
        language: 'en' or 'ar'
    
    Returns:
        dict with meal data (bilingual)
    
    Raises:
        Exception: if AI generation fails
    """
    
    # Build the prompt using prompt template
    prompt = get_meal_generation_prompt(
        selected_ingredients=selected_ingredients,
        meal_type=meal_type,
        cuisine_type=cuisine_type,
        child_profiles=child_profiles,
        dietary_restrictions=dietary_restrictions,
        language=language
    )
    
    print(f"🤖 Generating {meal_type} ({cuisine_type}) from {len(selected_ingredients)} ingredients...")
    
    meal_data = generate_json(prompt)
    validate_meal_data(meal_data)
    
    print(f"✅ Meal generated successfully: {meal_data['name_en']}")
    
    return meal_data


def regenerate_meal(original_meal_data, feedback, dietary_restrictions, language='en'):
    """
    Modify an existing meal based on parent feedback
    
    Args:
        original_meal_data: dict with 'name_en' and 'ingredients'
        feedback: what the parent wants changed
        dietary_restrictions: list of dietary restrictions
        language: 'en' or 'ar'
    
    Returns:
        dict with the updated meal data (bilingual)
    """
    
    prompt = get_meal_regeneration_prompt(
        original_meal=original_meal_data,
        feedback=feedback,
        dietary_restrictions=dietary_restrictions,
        language=language
    )
    
    meal_data = generate_json(prompt, temperature=1.0)
    validate_meal_data(meal_data)
    
    return meal_data


def validate_meal_data(meal_data):
    """
    Validate that meal data has all required fields and correct format
    
    Args:
        meal_data: dict with meal information
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: if validation fails with specific error message
    """
    
    # Check required fields
    required_fields = {
        'name_en': str,
        'name_ar': str,
        'ingredients': list,
        'instructions_en': str,
        'instructions_ar': str,
        'prep_time': str,
        'cook_time': str,
        'nutritional_benefits_en': str,
        'nutritional_benefits_ar': str,
        'why_healthy_en': str,
        'why_healthy_ar': str
    }
    
    if not isinstance(meal_data, dict):
        raise ValueError("Meal data must be a JSON object")
    
    for field, expected_type in required_fields.items():
        # Models sometimes return instructions as a list of steps, or times as numbers
        if expected_type is str and isinstance(meal_data.get(field), list):
            meal_data[field] = '\n'.join(str(item) for item in meal_data[field])
        elif expected_type is str and isinstance(meal_data.get(field), (int, float)):
            meal_data[field] = str(meal_data[field])
        
        if field not in meal_data:
            raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(meal_data[field], expected_type):
            raise ValueError(f"Field {field} must be {expected_type.__name__}")
    
    # Check ingredients structure
    if len(meal_data['ingredients']) == 0:
        raise ValueError("Ingredients list cannot be empty")
    
    for ing in meal_data['ingredients']:
        if not isinstance(ing, dict):
            raise ValueError("Each ingredient must be a dictionary")
        
        if 'name_en' not in ing or 'name_ar' not in ing:
            raise ValueError("Each ingredient must have name_en and name_ar")
    
    return True


def extract_ingredients(meal_data):
    """
    Extract and format ingredients from AI response
    
    Args:
        meal_data: dict with meal information
    
    Returns:
        list: formatted ingredient dictionaries
    """
    
    ingredients = meal_data.get('ingredients', [])
    formatted = []
    
    for ing in ingredients:
        formatted.append({
            'name_en': ing.get('name_en', ''),
            'name_ar': ing.get('name_ar', ''),
            'amount': ing.get('amount', ''),
            'icon': ing.get('icon', '🥘')
        })
    
    return formatted