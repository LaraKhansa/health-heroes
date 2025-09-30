"""
AI Prompts for Activity Generation
Bilingual: Arabic + English
Cultural Context: UAE/Islamic values
"""

from constants import (
    HOME_AREAS,
    ACTIVITY_CATEGORIES,
    DURATIONS,
    CULTURAL_REQUIREMENTS,
    CATEGORY_GUIDELINES,
    LOCATION_GUIDELINES
)


def get_batch_activity_generation_prompt(home_area, category, age_range, num_activities=5):
    """
    Generate prompt for creating multiple activities at once
    
    Args:
        home_area: Key from HOME_AREAS (e.g., "kitchen")
        category: Key from ACTIVITY_CATEGORIES (e.g., "cooking")
        age_range: Age range string (e.g., "3-5 years")
        num_activities: Number of activities to generate (default: 5)
    
    Returns:
        Complete prompt string for Gemini AI
    """
    
    # Get translated names
    location_en = HOME_AREAS[home_area]["en"]
    location_ar = HOME_AREAS[home_area]["ar"]
    category_en = ACTIVITY_CATEGORIES[category]["en"]
    category_ar = ACTIVITY_CATEGORIES[category]["ar"]
    
    # Get specific guidelines
    category_guideline = CATEGORY_GUIDELINES.get(category, "")
    location_guideline = LOCATION_GUIDELINES.get(home_area, "")
    
    prompt = f"""
You are a child development expert creating screen-free activities for Arab families in the UAE.

Generate {num_activities} DIFFERENT and UNIQUE activities with these specifications:

SPECIFICATIONS:
- Location: {location_en} ({location_ar})
- Category: {category_en} ({category_ar})
- Age Range: {age_range}
- Duration: Choose from {', '.join(DURATIONS)}
- Must be safe, fun, educational, and screen-free

CRITICAL - VARIETY REQUIREMENT:
Generate {num_activities} COMPLETELY DIFFERENT activities. Each activity must:
- Have a unique approach and concept
- Use different materials and methods
- Offer different learning outcomes
- Avoid any repetition or similarity
- Cover different aspects of {category_en}

{CULTURAL_REQUIREMENTS}

LANGUAGE REQUIREMENTS:
- Provide ALL activities in BOTH Arabic and English
- Arabic must be natural and fluent (not machine-translated)
- Use appropriate cultural terminology
- Keep language simple and age-appropriate

SPECIAL GUIDELINES:
{category_guideline}
{location_guideline}

Provide {num_activities} activities in this EXACT JSON format (no markdown, no extra text):
{{
  "activities": [
    {{
      "title_en": "Creative English Title (under 50 characters)",
      "title_ar": "عنوان إبداعي بالعربية (أقل من 50 حرف)",
      "description_en": "One engaging sentence description (under 120 characters)",
      "description_ar": "وصف جذاب بجملة واحدة (أقل من 120 حرف)",
      "duration": "choose from: {', '.join(DURATIONS)}",
      "age_range": "{age_range}",
      "materials": [
        {{
          "name_en": "Material name in English",
          "name_ar": "اسم المادة بالعربية",
          "icon": "relevant emoji"
        }}
      ],
      "steps_en": [
        "Step 1: Clear instruction",
        "Step 2: Clear instruction",
        "Step 3: Clear instruction",
        "Step 4: Clear instruction",
        "Step 5: Clear instruction"
      ],
      "steps_ar": [
        "الخطوة 1: تعليمات واضحة",
        "الخطوة 2: تعليمات واضحة",
        "الخطوة 3: تعليمات واضحة",
        "الخطوة 4: تعليمات واضحة",
        "الخطوة 5: تعليمات واضحة"
      ],
    }}
  ]
}}

REQUIREMENTS FOR EACH ACTIVITY:
- Include 3-6 materials maximum
- Include 4-6 steps (clear and simple)
- Steps should include Bismillah/Alhamdulillah when appropriate
- Materials commonly available in UAE homes
- Use relevant emojis for icons
- Age-appropriate, safe, and culturally sensitive
- Natural bilingual content
- Practical cultural notes
"""
    
    return prompt

