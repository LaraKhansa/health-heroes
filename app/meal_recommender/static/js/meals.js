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
        regeneratingSubtitle: 'Making it even better...',
        regenerateText: 'Modify Recipe',
        dialogTitle: 'Modify This Recipe',
        dialogDesc: "Tell us what you'd like to change:",
        submitBtn: 'Submit',
        cancelBtn: 'Cancel',
        feedbackPlaceholder: 'e.g., Make it less spicy, Add more vegetables, Use less oil'
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
        regeneratingSubtitle: 'نجعلها أفضل...',
        regenerateText: 'تعديل الوصفة',
        dialogTitle: 'تعديل هذه الوصفة',
        dialogDesc: 'أخبرنا بما تريد تغييره:',
        submitBtn: 'إرسال',
        cancelBtn: 'إلغاء',
        feedbackPlaceholder: 'مثال: اجعلها أقل حرارة، أضف المزيد من الخضروات، استخدم زيت أقل'
    }
};

// Update page text based on language
function updatePageText() {
    const t = translations[currentLanguage];
    
    // FIXED: Add null checks for ALL elements before accessing properties
    
    // Header (may not exist on all pages)
    const welcomeEl = document.getElementById('welcomeText');
    if (welcomeEl) {
        const userName = welcomeEl.textContent.split(', ')[1] || 'User';
        welcomeEl.textContent = `${t.welcomeText}, ${userName}`;
    }
    
    const logoutEl = document.getElementById('logoutBtn');
    if (logoutEl) {
        logoutEl.textContent = t.logoutBtn;
    }
    
    // Page header
    const pageTitleEl = document.getElementById('pageTitle');
    if (pageTitleEl) {
        pageTitleEl.textContent = t.pageTitle;
    }
    
    const pageSubtitleEl = document.getElementById('pageSubtitle');
    if (pageSubtitleEl) {
        pageSubtitleEl.textContent = t.pageSubtitle;
    }
    
    // Ingredients section
    const ingredientsTitleEl = document.getElementById('ingredientsTitle');
    if (ingredientsTitleEl) {
        ingredientsTitleEl.textContent = t.ingredientsTitle;
    }
    
    const ingredientsDescEl = document.getElementById('ingredientsDesc');
    if (ingredientsDescEl) {
        ingredientsDescEl.textContent = t.ingredientsDesc;
    }
    
    const customIngLabelEl = document.getElementById('customIngLabel');
    if (customIngLabelEl) {
        customIngLabelEl.textContent = t.customIngLabel;
    }
    
    const customIngEl = document.getElementById('custom_ingredient');
    if (customIngEl) {
        customIngEl.placeholder = t.customIngPlaceholder;
    }
    
    // Translate category headers
    document.querySelectorAll('.category-header').forEach(header => {
        const category = header.getAttribute('data-category');
        if (category && categoryTranslations[category]) {
            const span = header.querySelector('span');
            if (span) {
                span.textContent = categoryTranslations[category][currentLanguage];
            }
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
    const cuisineTypeTitleEl = document.getElementById('cuisineTypeTitle');
    if (cuisineTypeTitleEl) {
        cuisineTypeTitleEl.textContent = t.cuisineTypeTitle;
    }
    
    const cuisineTypeDescEl = document.getElementById('cuisineTypeDesc');
    if (cuisineTypeDescEl) {
        cuisineTypeDescEl.textContent = t.cuisineTypeDesc;
    }
    
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
    const mealTypeTitleEl = document.getElementById('mealTypeTitle');
    if (mealTypeTitleEl) {
        mealTypeTitleEl.textContent = t.mealTypeTitle;
    }
    
    const mealTypeDescEl = document.getElementById('mealTypeDesc');
    if (mealTypeDescEl) {
        mealTypeDescEl.textContent = t.mealTypeDesc;
    }
    
    // Translate meal type labels
    document.querySelectorAll('.meal-type-name').forEach(elem => {
        const enText = elem.getAttribute('data-en');
        const arText = elem.getAttribute('data-ar');
        if (enText && arText) {
            elem.textContent = currentLanguage === 'ar' ? arText : enText;
        }
    });
    
    // Buttons
    const generateTextEl = document.getElementById('generateText');
    if (generateTextEl) {
        generateTextEl.textContent = t.generateText;
    }
    
    const historyLinkEl = document.getElementById('historyLink');
    if (historyLinkEl) {
        historyLinkEl.textContent = t.historyLink;
    }

    // Check if elements exist before updating (for modal dialog that may not be on page)
    const regenerateTextEl = document.getElementById('regenerateText');
    if (regenerateTextEl) {
        regenerateTextEl.textContent = t.regenerateText;
    }
    
    const dialogTitleEl = document.getElementById('dialogTitle');
    if (dialogTitleEl) {
        dialogTitleEl.textContent = t.dialogTitle;
    }
    
    const dialogDescEl = document.getElementById('dialogDesc');
    if (dialogDescEl) {
        dialogDescEl.textContent = t.dialogDesc;
    }
    
    const submitBtnEl = document.getElementById('submitBtn');
    if (submitBtnEl) {
        submitBtnEl.textContent = t.submitBtn;
    }
    
    const cancelBtnEl = document.getElementById('cancelBtn');
    if (cancelBtnEl) {
        cancelBtnEl.textContent = t.cancelBtn;
    }
    
    const feedbackInputEl = document.getElementById('feedbackInput');
    if (feedbackInputEl) {
        feedbackInputEl.placeholder = t.feedbackPlaceholder;
    }
}

// Update selected ingredients count
function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('input[name="ingredients"]:checked');
    const count = checkboxes.length;
    
    const t = translations[currentLanguage];
    const countText = t.countText.replace('{count}', count);
    
    const countTextEl = document.getElementById('countText');
    if (countTextEl) {
        countTextEl.textContent = countText;
    }
    
    // Enable/disable generate button
    const generateBtn = document.getElementById('generateBtn');
    const customInput = document.getElementById('custom_ingredient');
    
    if (generateBtn && customInput) {
        const customInputValue = customInput.value.trim();
        
        if (count > 0 || customInputValue) {
            generateBtn.disabled = false;
        } else {
            generateBtn.disabled = true;
        }
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    updatePageText();
    updateSelectedCount();

    // Listen for custom ingredient changes
    const customIngEl = document.getElementById('custom_ingredient');
    if (customIngEl) {
        customIngEl.addEventListener('input', updateSelectedCount);
    }

    // Form validation
    const mealFormEl = document.getElementById('mealForm');
    if (mealFormEl) {
        mealFormEl.addEventListener('submit', function(e) {
            const checkboxes = document.querySelectorAll('input[name="ingredients"]:checked');
            const customInput = document.getElementById('custom_ingredient');
            const customInputValue = customInput ? customInput.value.trim() : '';
            
            if (checkboxes.length === 0 && !customInputValue) {
                e.preventDefault();
                alert(translations[currentLanguage].selectIngredient);
                return false;
            }
            
            // Show loading overlay
            showLoadingOverlay();
            
            // Form will submit normally, loading will show until page redirects
        });
    }
});

// Show loading overlay
function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('active');
        
        // Update text based on language
        const t = translations[currentLanguage];
        const loadingTitleEl = document.getElementById('loadingTitle');
        const loadingSubtitleEl = document.getElementById('loadingSubtitle');
        
        if (loadingTitleEl) {
            loadingTitleEl.textContent = t.loadingTitle || 'Generating Your Meal';
        }
        if (loadingSubtitleEl) {
            loadingSubtitleEl.textContent = t.loadingSubtitle || 'Our AI chef is preparing something delicious...';
        }
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