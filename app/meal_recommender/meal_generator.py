"""
AI Meal Generator
Handles all AI-related meal generation logic
"""

import os
import json
from openai import OpenAI
from app.meal_recommender.prompts import get_meal_generation_prompt


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
    
    try:
        # Initialize Gemini client
        client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.environ["HF_TOKEN"],
    )

        
        # Build the prompt using prompt template
        prompt = get_meal_generation_prompt(
            selected_ingredients=selected_ingredients,
            meal_type=meal_type,
            cuisine_type=cuisine_type,
            child_profiles=child_profiles,
            dietary_restrictions=dietary_restrictions,
            language=language
        )
        
        print(f"🤖 Generating meal with AI...")
        print(f"   - Meal type: {meal_type}")
        print(f"   - Cuisine: {cuisine_type}")
        print(f"   - Ingredients: {len(selected_ingredients)}")
        print(f"   - Language: {language}")
        
        # Call Gemini API
        completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:groq",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
        )
        response = completion.choices[0].message.content
        
        # Parse response text into JSON
        meal_data = json.loads(response)
        
        # Validate response has required fields
        required_fields = [
            'name_en', 'name_ar', 'ingredients', 
            'instructions_en', 'instructions_ar',
            'prep_time', 'cook_time',
            'nutritional_benefits_en', 'nutritional_benefits_ar',
            'why_healthy_en', 'why_healthy_ar'
        ]
        
        for field in required_fields:
            if field not in meal_data:
                raise ValueError(f"Missing required field: {field}")
        
        print(f"✅ Meal generated successfully: {meal_data['name_en']}")
        
        return meal_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Response text: {response.text[:200]}...")
        raise Exception("Failed to parse AI response. Please try again.")
        
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        raise Exception(f"Failed to generate meal: {str(e)}")


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
    
    for field, expected_type in required_fields.items():
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