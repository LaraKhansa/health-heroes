"""
Constants for Meal Recommender
UAE-focused ingredients with Arabic translations
Organized by categories
"""

# ============================================
# INGREDIENT CATEGORIES (UAE-FOCUSED)
# ============================================

INGREDIENTS = {
    # Proteins - البروتينات
    "proteins": {
        "en": "Proteins",
        "ar": "البروتينات",
        "items": [
            {"name_en": "Chicken", "name_ar": "دجاج", "icon": "🍗"},
            {"name_en": "Beef", "name_ar": "لحم بقري", "icon": "🥩"},
            {"name_en": "Lamb", "name_ar": "لحم خروف", "icon": "🍖"},
            {"name_en": "Fish", "name_ar": "سمك", "icon": "🐟"},
            {"name_en": "Shrimp", "name_ar": "روبيان", "icon": "🦐"},
            {"name_en": "Eggs", "name_ar": "بيض", "icon": "🥚"},
            {"name_en": "Lentils", "name_ar": "عدس", "icon": "🫘"},
            {"name_en": "Chickpeas", "name_ar": "حمص", "icon": "🫘"},
            {"name_en": "Fava Beans", "name_ar": "فول", "icon": "🫘"},
        ]
    },
    
    # Grains & Carbs - الحبوب والنشويات
    "grains": {
        "en": "Grains & Carbs",
        "ar": "الحبوب والنشويات",
        "items": [
            {"name_en": "Rice (Basmati)", "name_ar": "أرز بسمتي", "icon": "🍚"},
            {"name_en": "Brown Rice", "name_ar": "أرز بني", "icon": "🍚"},
            {"name_en": "Bread (Khubz)", "name_ar": "خبز", "icon": "🥖"},
            {"name_en": "Oats", "name_ar": "شوفان", "icon": "🌾"},
            {"name_en": "Pasta", "name_ar": "معكرونة", "icon": "🍝"},
            {"name_en": "Bulgur", "name_ar": "برغل", "icon": "🌾"},
            {"name_en": "Vermicelli", "name_ar": "شعيرية", "icon": "🍝"},
        ]
    },
    
    # Vegetables - الخضروات
    "vegetables": {
        "en": "Vegetables",
        "ar": "الخضروات",
        "items": [
            {"name_en": "Tomato", "name_ar": "طماطم", "icon": "🍅"},
            {"name_en": "Cucumber", "name_ar": "خيار", "icon": "🥒"},
            {"name_en": "Onion", "name_ar": "بصل", "icon": "🧅"},
            {"name_en": "Garlic", "name_ar": "ثوم", "icon": "🧄"},
            {"name_en": "Potato", "name_ar": "بطاطس", "icon": "🥔"},
            {"name_en": "Sweet Potato", "name_ar": "بطاطا حلوة", "icon": "🍠"},
            {"name_en": "Carrot", "name_ar": "جزر", "icon": "🥕"},
            {"name_en": "Zucchini", "name_ar": "كوسة", "icon": "🥒"},
            {"name_en": "Eggplant", "name_ar": "باذنجان", "icon": "🍆"},
            {"name_en": "Bell Pepper", "name_ar": "فلفل رومي", "icon": "🫑"},
            {"name_en": "Spinach", "name_ar": "سبانخ", "icon": "🥬"},
            {"name_en": "Lettuce", "name_ar": "خس", "icon": "🥬"},
            {"name_en": "Parsley", "name_ar": "بقدونس", "icon": "🌿"},
            {"name_en": "Mint", "name_ar": "نعناع", "icon": "🌿"},
            {"name_en": "Coriander", "name_ar": "كزبرة", "icon": "🌿"},
        ]
    },
    
    # Fruits - الفواكه
    "fruits": {
        "en": "Fruits",
        "ar": "الفواكه",
        "items": [
            {"name_en": "Dates", "name_ar": "تمر", "icon": "🫒"},
            {"name_en": "Banana", "name_ar": "موز", "icon": "🍌"},
            {"name_en": "Apple", "name_ar": "تفاح", "icon": "🍎"},
            {"name_en": "Orange", "name_ar": "برتقال", "icon": "🍊"},
            {"name_en": "Mango", "name_ar": "مانجو", "icon": "🥭"},
            {"name_en": "Strawberries", "name_ar": "فراولة", "icon": "🍓"},
            {"name_en": "Grapes", "name_ar": "عنب", "icon": "🍇"},
            {"name_en": "Watermelon", "name_ar": "بطيخ", "icon": "🍉"},
            {"name_en": "Pomegranate", "name_ar": "رمان", "icon": "🍒"},
            {"name_en": "Lemon", "name_ar": "ليمون", "icon": "🍋"},
        ]
    },
    
    # Dairy - منتجات الألبان
    "dairy": {
        "en": "Dairy Products",
        "ar": "منتجات الألبان",
        "items": [
            {"name_en": "Milk", "name_ar": "حليب", "icon": "🥛"},
            {"name_en": "Yogurt (Laban)", "name_ar": "لبن", "icon": "🥛"},
            {"name_en": "Cheese (White)", "name_ar": "جبنة بيضاء", "icon": "🧀"},
            {"name_en": "Labneh", "name_ar": "لبنة", "icon": "🥛"},
            {"name_en": "Butter", "name_ar": "زبدة", "icon": "🧈"},
        ]
    },
    
    # Spices & Flavorings - البهارات والتوابل
    "spices": {
        "en": "Spices & Seasonings",
        "ar": "البهارات والتوابل",
        "items": [
            {"name_en": "Olive Oil", "name_ar": "زيت زيتون", "icon": "🫒"},
            {"name_en": "Vegetable Oil", "name_ar": "زيت نباتي", "icon": "🌻"},
            {"name_en": "Salt", "name_ar": "ملح", "icon": "🧂"},
            {"name_en": "Black Pepper", "name_ar": "فلفل أسود", "icon": "⚫"},
            {"name_en": "Cumin", "name_ar": "كمون", "icon": "🌿"},
            {"name_en": "Turmeric", "name_ar": "كركم", "icon": "🟡"},
            {"name_en": "Cinnamon", "name_ar": "قرفة", "icon": "🟤"},
            {"name_en": "Cardamom", "name_ar": "هيل", "icon": "🟢"},
            {"name_en": "Bay Leaves", "name_ar": "ورق غار", "icon": "🍃"},
            {"name_en": "Dried Lemon", "name_ar": "لومي", "icon": "🍋"},
        ]
    },
    
    # Others - أخرى
    "others": {
        "en": "Other Ingredients",
        "ar": "مكونات أخرى",
        "items": [
            {"name_en": "Honey", "name_ar": "عسل", "icon": "🍯"},
            {"name_en": "Tahini", "name_ar": "طحينة", "icon": "🥜"},
            {"name_en": "Tomato Paste", "name_ar": "معجون طماطم", "icon": "🍅"},
            {"name_en": "Nuts (Mixed)", "name_ar": "مكسرات", "icon": "🥜"},
        ]
    }
}

# ============================================
# MEAL TYPES
# ============================================

MEAL_TYPES = {
    "breakfast": {
        "en": "Breakfast",
        "ar": "فطور",
        "icon": "🌅"
    },
    "lunch": {
        "en": "Lunch",
        "ar": "غداء",
        "icon": "☀️"
    },
    "dinner": {
        "en": "Dinner",
        "ar": "عشاء",
        "icon": "🌙"
    },
    "snack": {
        "en": "Snack",
        "ar": "وجبة خفيفة",
        "icon": "🍎"
    },
    "dessert": {
        "en": "Dessert",
        "ar": "حلى",
        "icon": "🍰"
    }
}

# ============================================
# CUISINE TYPES
# ============================================

CUISINE_TYPES = {
    "arabic": {
        "en": "Arabic Cuisine",
        "ar": "مطبخ عربي",
        "icon": "🕌",
        "description_en": "Traditional UAE & Middle Eastern dishes",
        "description_ar": "أطباق إماراتية وشرق أوسطية تقليدية"
    },
    "international": {
        "en": "International",
        "ar": "عالمي",
        "icon": "🌍",
        "description_en": "Healthy global cuisines",
        "description_ar": "مطابخ عالمية صحية"
    }
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_all_ingredients_flat():
    """
    Get all ingredients as a flat list (for easier processing)
    Returns list of ingredient dictionaries
    """
    all_ingredients = []
    for category_key, category_data in INGREDIENTS.items():
        for item in category_data["items"]:
            item_copy = item.copy()
            item_copy["category"] = category_key
            all_ingredients.append(item_copy)
    return all_ingredients


def get_ingredient_by_name(name, language='en'):
    """
    Find an ingredient by name (case-insensitive)
    
    Args:
        name: ingredient name to search for
        language: 'en' or 'ar'
    
    Returns:
        ingredient dict or None
    """
    name_lower = name.lower().strip()
    key = f"name_{language}"
    
    for category_data in INGREDIENTS.values():
        for item in category_data["items"]:
            if item[key].lower() == name_lower:
                return item
    return None


def get_ingredients_by_category(category_key, language='en'):
    """
    Get all ingredients in a specific category
    
    Args:
        category_key: one of the category keys (proteins, grains, etc.)
        language: 'en' or 'ar'
    
    Returns:
        list of ingredient names
    """
    if category_key not in INGREDIENTS:
        return []
    
    key = f"name_{language}"
    return [item[key] for item in INGREDIENTS[category_key]["items"]]