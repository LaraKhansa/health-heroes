"""
Constants for Health Heroes Activity Generation
Bilingual support: Arabic (العربية) + English
"""

# ============================================
# HOME AREAS
# ============================================
HOME_AREAS = {
    "kitchen": {
        "en": "Kitchen Access",
        "ar": "المطبخ"
    },
    "balcony": {
        "en": "Balcony/Terrace",
        "ar": "الشرفة"
    },
    "garden": {
        "en": "Garden/Backyard",
        "ar": "الحديقة"
    },
    "living_room": {
        "en": "Living Room Space",
        "ar": "غرفة المعيشة"
    },
    "outdoor_nearby": {
        "en": "Nearby Park/Outdoor Space",
        "ar": "حديقة قريبة أو مساحة خارجية"
    }
}

# ============================================
# ACTIVITY CATEGORIES
# ============================================
ACTIVITY_CATEGORIES = {
    "games": {
        "en": "Games & Play",
        "ar": "ألعاب"
    },
    "cooking": {
        "en": "Healthy Cooking",
        "ar": "طبخ الصحي"
    },
    "creative": {
        "en": "Arts & Crafts",
        "ar": "فنون وحرف يدوية"
    },
    "nature": {
        "en": "Nature Activities",
        "ar": "أنشطة في الطبيعة"
    },
    "reading": {
        "en": "Reading & Storytelling",
        "ar": "قراءة ورواية القصص"
    },
    "science": {
        "en": "Science Experiments",
        "ar": "تجارب علمية"
    }
}

# ============================================
# AGE RANGES
# ============================================
AGE_RANGES = [
    "2-3 years",
    "3-5 years", 
    "5-7 years",
    "7-8 years"
]

# ============================================
# DURATIONS
# ============================================
DURATIONS = [
    "5-10 min",
    "10-15 min",
    "15-30 min",
    "30-45 min"
]

# ============================================
# MATERIAL COLORS
# ============================================
MATERIAL_COLORS = [
    "purple",
    "green",
    "orange",
    "blue",
    "yellow",
]

# ============================================
# UAE/ISLAMIC CULTURAL REQUIREMENTS
# ============================================
CULTURAL_REQUIREMENTS = """
CRITICAL UAE/ISLAMIC CULTURAL REQUIREMENTS:
1. Start activities with "Bismillah" (بسم الله) when appropriate
2. End with "Alhamdulillah" (الحمد لله) or gratitude expression when appropriate
3. 100% Halal ingredients ONLY (no pork, alcohol, non-halal gelatin)
4. Use ingredients commonly available in UAE markets
5. Consider UAE climate (very hot summers 40°C+, mild winters)
6. Family values: respect for parents, sibling cooperation, modesty
7. Activities should be modest and appropriate for conservative families
8. Promote healthy eating and active lifestyle aligned with Islamic teachings
9. Use natural Arabic terminology (not machine-translated)
10. Emphasize safety and parental supervision

"""

# ============================================
# CATEGORY-SPECIFIC GUIDELINES
# ============================================
CATEGORY_GUIDELINES = {
    "cooking": "ONLY healthy recipes with NO junk food, excessive sugar, or processed ingredients. Use fresh, wholesome ingredients.",
    "creative": "Use safe, non-toxic materials commonly found in UAE homes. Avoid small parts for younger children.",
    "outdoor": "Consider UAE hot climate - outdoor activities should be early morning (6-9 AM) or evening (5-7 PM).",
    "reading": "Include Islamic values and teachings naturally. Use stories with moral lessons.",
    "science": "Use safe, simple experiments with household items. Emphasize adult supervision.",
    "games": "Promote physical activity and family bonding. Ensure activities are safe indoors."
}

# ============================================
# LOCATION-SPECIFIC GUIDELINES
# ============================================
LOCATION_GUIDELINES = {
    "garden": "Consider UAE hot climate - activities should be early morning or evening. Provide shade and water breaks.",
    "balcony": "Ensure safety measures. Activities should be suitable for limited space and hot weather.",
    "outdoor_nearby": "Recommend early morning or evening timing. Emphasize sun protection and hydration.",
    "kitchen": "Emphasize safety and adult supervision. Keep activities simple and mess-free.",
    "living_room": "Ensure activities don't damage furniture. Keep space requirements minimal."
}