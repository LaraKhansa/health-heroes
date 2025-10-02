"""
AI Prompts for Meal Generation
Bilingual: Arabic + English
Cultural Context: UAE/Islamic values
"""

from app.meal_recommender.constants import MEAL_TYPES

def format_child_profiles(child_profiles):
    """
    Format child profiles for prompt
    
    Args:
        child_profiles: list of child profile dicts
    
    Returns:
        formatted string
    """
    
    if not child_profiles:
        return "No specific child profile provided. Create a generally healthy meal for children aged 2-8."
    
    profiles_text = []
    for child in child_profiles:
        age = child.get('age', 'unknown')
        restrictions = child.get('dietary_restrictions', [])
        special_needs = child.get('special_needs', '')
        
        profile = f"- Child aged {age} years"
        
        if restrictions:
            profile += f", allergic to: {', '.join(restrictions)}"
        
        if special_needs:
            profile += f", special needs: {special_needs}"
        
        profiles_text.append(profile)
    
    return '\n'.join(profiles_text)


def format_dietary_restrictions(dietary_restrictions):
    """
    Format dietary restrictions for prompt
    
    Args:
        dietary_restrictions: list of restrictions
    
    Returns:
        formatted string
    """
    
    if not dietary_restrictions:
        return "None - all common ingredients are safe"
    
    return '\n'.join([f"- {restriction}" for restriction in dietary_restrictions])


def get_meal_generation_prompt(selected_ingredients, meal_type, cuisine_type, child_profiles, dietary_restrictions, language='en'):
    """
    Generate prompt for meal creation
    
    Args:
        selected_ingredients: list of ingredient names
        meal_type: breakfast, lunch, dinner, snack, dessert
        cuisine_type: arabic or international
        child_profiles: list of child profile dicts
        dietary_restrictions: list of dietary restrictions
        language: 'en' or 'ar'
    
    Returns:
        Complete prompt string for Gemini AI
    """
    
    # Get meal type display name
    meal_type_display = MEAL_TYPES.get(meal_type, {}).get('en', meal_type)
    
    # Get cuisine guidance
    cuisine_guidance = ""
    if cuisine_type == "arabic":
        cuisine_guidance = """
CUISINE STYLE: Arabic/Middle Eastern
- Focus on traditional UAE and Middle Eastern recipes
- Use Arabic spices and cooking methods (cumin, cardamom, saffron, dried lemon)
- Include dishes like Machboos, Harees, Thareed, Salona, or similar traditional meals
- Emphasize family-style serving
- Use traditional cooking techniques (one-pot meals, slow cooking, etc.)
"""
    else:
        cuisine_guidance = """
CUISINE STYLE: International (Healthy Global)
- Can include Western, Asian, Mediterranean, or fusion dishes
- Focus on internationally recognized healthy meals
- Ensure ingredients and methods are accessible in UAE supermarkets
- Keep it child-friendly and nutritious
- Examples: pasta dishes, stir-fries, salads, grain bowls, etc.
"""
    
    # Format child profiles for display
    children_info = format_child_profiles(child_profiles)
    
    # Format dietary restrictions
    restrictions_text = format_dietary_restrictions(dietary_restrictions)
    
    # Build the prompt
    prompt = f"""
You are a professional nutrition expert and chef specializing in healthy, child-friendly meals for families in the UAE.

FAMILY CONTEXT:
{children_info}

DIETARY RESTRICTIONS (MUST AVOID):
{restrictions_text}

AVAILABLE INGREDIENTS:
{', '.join(selected_ingredients)}

MEAL TYPE: {meal_type_display}

{cuisine_guidance}

YOUR TASK:
Create a healthy, delicious, and culturally appropriate {meal_type_display} recipe that:

1. **Uses mainly the available ingredients** - You may add common UAE pantry items if needed (like salt, oil, spices)
2. **Respects all dietary restrictions** - Absolutely NO ingredients from the restrictions list
3. **Is child-friendly** - Appealing taste, texture, and presentation for children
4. **Is nutritious** - Balanced nutrition suitable for children's growth
5. **Matches the requested cuisine style** - Follow the cuisine guidance above
6. **Is practical** - Simple enough for busy parents to prepare

CRITICAL UAE/ISLAMIC CULTURAL REQUIREMENTS:
- Start cooking with "Bismillah" (بسم الله) in instructions
- ONLY Halal ingredients (no pork, alcohol, non-halal gelatin)
- Use ingredients commonly available in UAE supermarkets
- Consider UAE climate and preferences
- Family-oriented meal (suitable for sharing)
- Emphasize fresh, wholesome ingredients

RECIPE REQUIREMENTS:
- Une the true known recipe name 
- Clear, simple steps
- Realistic prep and cook times
- Explain nutritional benefits in parent-friendly language
- Explain why this is specifically healthy for children

OUTPUT FORMAT (STRICT JSON):
{{
    "name_en": "Appealing recipe name in English (max 50 chars)",
    "name_ar": "اسم الوصفة بالعربية (max 50 chars)",
    "ingredients": [
        {{
            "name_en": "ingredient name",
            "name_ar": "اسم المكون",
            "amount": "quantity with unit (e.g., 2 cups, 100g)",
            "icon": "relevant emoji"
        }}
    ],
    "instructions_en": "Step 1: Say Bismillah and [instruction]\\nStep 2: [instruction]\\nStep 3: [instruction]\\n...",
    "instructions_ar": "الخطوة 1: قل بسم الله و[التعليمات]\\nالخطوة 2: [التعليمات]\\nالخطوة 3: [التعليمات]\\n...",
    "prep_time": "X minutes",
    "cook_time": "Y minutes",
    "nutritional_benefits_en": "Brief explanation of key nutrients and health benefits (2-3 sentences)",
    "nutritional_benefits_ar": "شرح موجز للعناصر الغذائية الرئيسية والفوائد الصحية (2-3 جمل)",
    "why_healthy_en": "Parent-friendly explanation of why this meal is specifically good for children's growth and development (2-3 sentences)",
    "why_healthy_ar": "شرح للوالدين عن سبب فائدة هذه الوجبة لنمو الأطفال وتطورهم (2-3 جمل)"
}}

IMPORTANT:
- Output ONLY valid JSON
- No markdown formatting
- No code blocks
- No extra text
- Arabic text must be natural and fluent (not machine-translated)
- All fields are required
- Instructions must be numbered and clear
"""
    
    return prompt

def get_meal_regeneration_prompt(original_meal, feedback, language='en'):
    """
    Generate prompt for regenerating/modifying a meal based on user feedback
    
    Args:
        original_meal: original meal data dict
        feedback: user's feedback/requested changes
        language: 'en' or 'ar'
    
    Returns:
        prompt string
    """
    
    prompt = f"""
You previously created this meal recipe:
Name: {original_meal.get('name_en')}
Ingredients: {', '.join([ing['name_en'] for ing in original_meal.get('ingredients', [])])}

The user has provided this feedback:
"{feedback}"

Please modify the recipe based on this feedback while:
1. Keeping the same general concept
2. Maintaining nutritional value
3. Respecting all original dietary restrictions
4. Staying culturally appropriate for UAE families

Provide the updated recipe in the same JSON format as before.
"""
    
    return prompt