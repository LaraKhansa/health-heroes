// Ingredient category translations
const categoryTranslations = {
    proteins: { en: "Proteins", ar: "البروتينات" },
    grains: { en: "Grains & Carbs", ar: "الحبوب والنشويات" },
    vegetables: { en: "Vegetables", ar: "الخضروات" },
    fruits: { en: "Fruits", ar: "الفواكه" },
    dairy: { en: "Dairy Products", ar: "منتجات الألبان" },
    spices: { en: "Spices & Seasonings", ar: "البهارات والتوابل" },
    others: { en: "Other Ingredients", ar: "مكونات أخرى" }
};

// Translation object
const translations = {
    en: {
        welcomeText: 'Welcome',
        logoutBtn: 'Logout ⬆',
        pageTitle: '🍽️ Meal Recommender',
        pageSubtitle: 'Create healthy, personalized meals for your family',
        ingredientsTitle: 'Select Your Ingredients',
        ingredientsDesc: 'Choose the ingredients you have at home',
        customIngLabel: '+ Add Custom Ingredients (comma-separated)',
        customIngPlaceholder: 'e.g., Avocado, Quinoa, Chia Seeds',
        cuisineTypeTitle: 'Cuisine Type',
        cuisineTypeDesc: 'Choose your preferred cuisine style',
        mealTypeTitle: 'Choose Meal Type',
        mealTypeDesc: 'What type of meal do you want to prepare?',
        generateText: '🎨 Generate Healthy Meal',
        historyLink: '📖 View Meal History',
        countText: '{count} ingredients selected',
        generating: '⏳ Generating...',
        selectIngredient: 'Please select at least one ingredient',
        loadingTitle: 'Generating Your Meal',
        loadingSubtitle: 'Our AI chef is preparing something delicious...',
        regeneratingTitle: 'Modifying Your Recipe',
        regeneratingSubtitle: 'Making it even better...'
    },
    ar: {
        welcomeText: 'مرحباً',
        logoutBtn: 'تسجيل الخروج ⬆',
        pageTitle: '🍽️ موصي الوجبات',
        pageSubtitle: 'أنشئ وجبات صحية مخصصة لعائلتك',
        ingredientsTitle: 'اختر المكونات',
        ingredientsDesc: 'اختر المكونات المتوفرة في منزلك',
        customIngLabel: '+ أضف مكونات مخصصة (مفصولة بفواصل)',
        customIngPlaceholder: 'مثال: أفوكادو، كينوا، بذور الشيا',
        cuisineTypeTitle: 'نوع المطبخ',
        cuisineTypeDesc: 'اختر نمط المطبخ المفضل لديك',
        mealTypeTitle: 'اختر نوع الوجبة',
        mealTypeDesc: 'ما نوع الوجبة التي تريد تحضيرها؟',
        generateText: '🎨 إنشاء وجبة صحية',
        historyLink: '📖 عرض سجل الوجبات',
        countText: '{count} مكونات محددة',
        generating: '⏳ جاري الإنشاء...',
        selectIngredient: 'الرجاء اختيار مكون واحد على الأقل',
        loadingTitle: 'جاري إنشاء وجبتك',
        loadingSubtitle: 'الطاهي الذكي يحضر لك شيئاً لذيذاً...',
        regeneratingTitle: 'جاري تعديل الوصفة',
        regeneratingSubtitle: 'نجعلها أفضل...'
    }
};

// Update page text based on language
function updatePageText() {
    const t = translations[currentLanguage];
    
    // Header
    const userName = document.getElementById('welcomeText').textContent.split(', ')[1] || 'User';
    document.getElementById('welcomeText').textContent = `${t.welcomeText}, ${userName}`;
    document.getElementById('logoutBtn').textContent = t.logoutBtn;
    
    // Page header
    document.getElementById('pageTitle').textContent = t.pageTitle;
    document.getElementById('pageSubtitle').textContent = t.pageSubtitle;
    
    // Ingredients section
    document.getElementById('ingredientsTitle').textContent = t.ingredientsTitle;
    document.getElementById('ingredientsDesc').textContent = t.ingredientsDesc;
    document.getElementById('customIngLabel').textContent = t.customIngLabel;
    document.getElementById('custom_ingredient').placeholder = t.customIngPlaceholder;
    
    // Translate category headers
    document.querySelectorAll('.category-header').forEach(header => {
        const category = header.getAttribute('data-category');
        if (category && categoryTranslations[category]) {
            header.textContent = categoryTranslations[category][currentLanguage];
        }
    });
    
    // Translate ingredient names
    document.querySelectorAll('.ingredient-item label').forEach(label => {
        const enText = label.getAttribute('data-en');
        const arText = label.getAttribute('data-ar');
        const nameSpan = label.querySelector('.ingredient-name');
        if (nameSpan && enText && arText) {
            nameSpan.textContent = currentLanguage === 'ar' ? arText : enText;
        }
    });
    
    // Cuisine type section
    document.getElementById('cuisineTypeTitle').textContent = t.cuisineTypeTitle;
    document.getElementById('cuisineTypeDesc').textContent = t.cuisineTypeDesc;
    
    // Translate cuisine type labels
    document.querySelectorAll('.cuisine-type-name').forEach(elem => {
        const enText = elem.getAttribute('data-en');
        const arText = elem.getAttribute('data-ar');
        if (enText && arText) {
            elem.textContent = currentLanguage === 'ar' ? arText : enText;
        }
    });
    
    document.querySelectorAll('.cuisine-type-desc').forEach(elem => {
        const enText = elem.getAttribute('data-en');
        const arText = elem.getAttribute('data-ar');
        if (enText && arText) {
            elem.textContent = currentLanguage === 'ar' ? arText : enText;
        }
    });
    
    // Meal type section
    document.getElementById('mealTypeTitle').textContent = t.mealTypeTitle;
    document.getElementById('mealTypeDesc').textContent = t.mealTypeDesc;
    
    // Translate meal type labels
    document.querySelectorAll('.meal-type-name').forEach(elem => {
        const enText = elem.getAttribute('data-en');
        const arText = elem.getAttribute('data-ar');
        if (enText && arText) {
            elem.textContent = currentLanguage === 'ar' ? arText : enText;
        }
    });
    
    // Buttons
    document.getElementById('generateText').textContent = t.generateText;
    document.getElementById('historyLink').textContent = t.historyLink;

    // Regenerate button and modal
    document.getElementById('regenerateText').textContent = t.regenerateText;
    document.getElementById('dialogTitle').textContent = t.dialogTitle;
    document.getElementById('dialogDesc').textContent = t.dialogDesc;
    document.getElementById('submitBtn').textContent = t.submitBtn;
    document.getElementById('cancelBtn').textContent = t.cancelBtn;
    document.getElementById('feedbackInput').placeholder = t.feedbackPlaceholder;
}

// Update selected ingredients count
function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('input[name="ingredients"]:checked');
    const count = checkboxes.length;
    
    const t = translations[currentLanguage];
    const countText = t.countText.replace('{count}', count);
    
    document.getElementById('countText').textContent = countText;
    
    // Enable/disable generate button
    const generateBtn = document.getElementById('generateBtn');
    const customInput = document.getElementById('custom_ingredient').value.trim();
    
    if (count > 0 || customInput) {
        generateBtn.disabled = false;
    } else {
        generateBtn.disabled = true;
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    updatePageText();
    updateSelectedCount();

    // Listen for custom ingredient changes
    document.getElementById('custom_ingredient').addEventListener('input', updateSelectedCount);

    // Form validation
    document.getElementById('mealForm').addEventListener('submit', function(e) {
        const checkboxes = document.querySelectorAll('input[name="ingredients"]:checked');
        const customInput = document.getElementById('custom_ingredient').value.trim();
        
        if (checkboxes.length === 0 && !customInput) {
            e.preventDefault();
            alert(translations[currentLanguage].selectIngredient);
            return false;
        }
        
        // Show loading overlay
        showLoadingOverlay();
        
        // Form will submit normally, loading will show until page redirects
    });
});

// Show loading overlay
function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('active');
        
        // Update text based on language
        const t = translations[currentLanguage];
        document.getElementById('loadingTitle').textContent = t.loadingTitle || 'Generating Your Meal';
        document.getElementById('loadingSubtitle').textContent = t.loadingSubtitle || 'Our AI chef is preparing something delicious...';
    }
}

// Hide loading overlay
function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

console.log('✅ Meals JS loaded successfully!');