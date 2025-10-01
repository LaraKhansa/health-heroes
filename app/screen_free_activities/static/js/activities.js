// Translation object
const translations = {
    en: {
        welcome: 'Welcome',
        appTitle: 'Health Heroes ⭐',
        logout: 'Logout ⬆',
        pageTitle: 'Screen-Free Activities',
        pageSubtitle: 'Engaging activities tailored for your family',
        activityType: 'Activity Type',
        allActivities: 'All Activities',
        gamesPlay: 'Games & Play',
        healthyCooking: 'Healthy Cooking',
        artsCrafts: 'Arts & Crafts',
        outdoorActivities: 'Outdoor Activities',
        readingStorytelling: 'Reading & Storytelling',
        scienceExperiments: 'Science Experiments',
        childSelection: 'Child Selection',
        allChildren: 'All Children',
        perfectForHome: 'Perfect for Your Home',
        balconySpace: 'Balcony Space',
        kitchenAccess: 'Kitchen Access',
        getNewIdeas: 'Get New Ideas',
        suggestions: 'Suggestions',
        agesLabel: 'Ages',
        materialsNeeded: 'Materials Needed',
        instructions: 'Instructions',
        moreSteps: 'more steps...',
        startActivity: 'Start Activity',
        markComplete: 'Mark as Complete',
        finishActivity: 'Finish Activity! 🎉',
        pauseCelebrate: 'Pause & Celebrate! ✨',
        stepOf: 'Step',
        of: 'of',
        steps: 'steps',
        noActivities: 'No activities available. Try changing filters!',
        loadingActivities: 'Loading activities...',
        noMaterials: 'No materials needed'
    },
    ar: {
        welcome: 'مرحباً',
        appTitle: 'أبطال الصحة ⭐',
        logout: 'تسجيل الخروج ⬆',
        pageTitle: 'أنشطة بدون شاشات',
        pageSubtitle: 'أنشطة جذابة مصممة لعائلتك',
        activityType: 'نوع النشاط',
        allActivities: 'جميع الأنشطة',
        gamesPlay: 'ألعاب',
        healthyCooking: 'طبخ صحي',
        artsCrafts: 'فنون وحرف يدوية',
        outdoorActivities: 'أنشطة خارجية',
        readingStorytelling: 'قراءة ورواية القصص',
        scienceExperiments: 'تجارب علمية',
        childSelection: 'اختيار الطفل',
        allChildren: 'جميع الأطفال',
        perfectForHome: 'مناسب لمنزلك',
        balconySpace: 'مساحة الشرفة',
        kitchenAccess: 'الوصول للمطبخ',
        getNewIdeas: 'احصل على أفكار جديدة',
        suggestions: 'اقتراحات',
        agesLabel: 'الأعمار',
        materialsNeeded: 'المواد المطلوبة',
        instructions: 'التعليمات',
        moreSteps: 'خطوات إضافية...',
        startActivity: 'ابدأ النشاط',
        markComplete: 'تم الإنجاز',
        finishActivity: 'إنهاء النشاط! 🎉',
        pauseCelebrate: 'توقف واحتفل! ✨',
        stepOf: 'خطوة',
        of: 'من',
        steps: 'خطوات',
        noActivities: 'لا توجد أنشطة متاحة. حاول تغيير الفلاتر!',
        loadingActivities: 'جاري تحميل الأنشطة...',
        noMaterials: 'لا توجد مواد مطلوبة'
    }
};

// Get translation helper
function t(key) {
    return translations[currentLanguage][key] || translations['en'][key] || key;
}

// Update page text based on language
function updatePageText() {
    // Header
    const welcomeText = document.querySelector('.welcome-text');
    const appTitle = document.querySelector('.app-title');
    const logoutBtn = document.querySelector('.logout-btn');
    
    if (welcomeText) {
        const userName = welcomeText.textContent.split(', ')[1] || 'User';
        welcomeText.textContent = `${t('welcome')}, ${userName}`;
    }
    if (appTitle) appTitle.textContent = t('appTitle');
    if (logoutBtn) logoutBtn.textContent = t('logout');
    
    // Page title and subtitle
    const pageTitle = document.querySelector('.page-title');
    const pageSubtitle = document.querySelector('.page-subtitle');
    
    if (pageTitle) pageTitle.textContent = t('pageTitle');
    if (pageSubtitle) pageSubtitle.textContent = t('pageSubtitle');
    
    // Filter dropdowns - Activity Type
    const activityTypeDropdown = document.getElementById('activity-type');
    if (activityTypeDropdown) {
        activityTypeDropdown.options[0].text = t('allActivities');
        activityTypeDropdown.options[1].text = t('gamesPlay');
        activityTypeDropdown.options[2].text = t('healthyCooking');
        activityTypeDropdown.options[3].text = t('artsCrafts');
        activityTypeDropdown.options[4].text = t('outdoorActivities');
        activityTypeDropdown.options[5].text = t('readingStorytelling');
        activityTypeDropdown.options[6].text = t('scienceExperiments');
    }
    
    // Filter dropdowns - Child Selection
    const childSelectionDropdown = document.getElementById('child-selection');
    if (childSelectionDropdown) {
        childSelectionDropdown.options[0].text = t('allChildren');
        // Keep children names as is (Sarah, Ahmed, Layla)
    }
    
    // Perfect for Your Home section
    const sectionTitles = document.querySelectorAll('.section-title');
    if (sectionTitles[0]) sectionTitles[0].textContent = t('perfectForHome');

    const resourceItems = document.querySelectorAll('.resource-item span:not(.check-icon)');
    if (resourceItems[0]) resourceItems[0].textContent = t('balconySpace');
    if (resourceItems[1]) resourceItems[1].textContent = t('kitchenAccess');
    
    // Get New Ideas button
    const newIdeasBtn = document.querySelector('.new-ideas-btn');
    if (newIdeasBtn) newIdeasBtn.textContent = t('getNewIdeas');
    
    // Suggestions header
    if (sectionTitles[1]) sectionTitles[1].textContent = t('suggestions');
    
    // Loading text
    const loadingSpinner = document.querySelector('.loading-spinner p');
    if (loadingSpinner) loadingSpinner.textContent = t('loadingActivities');
    
    // Modal buttons
    const completeBtn = document.getElementById('completeBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    
    if (completeBtn) completeBtn.textContent = t('markComplete');
    if (pauseBtn) pauseBtn.textContent = t('pauseCelebrate');
}

// Translate existing activity cards on page load
function translateExistingCards() {
    const activityCards = document.querySelectorAll('.activity-card');
    
    activityCards.forEach(card => {
        // Translate "Ages:"
        const ageLabel = card.querySelector('.activity-age');
        if (ageLabel) {
            const ageRange = ageLabel.textContent.replace('Ages:', '').trim();
            ageLabel.textContent = `${t('agesLabel')}: ${ageRange}`;
        }
        
        // Translate "Materials Needed"
        const materialsTitle = card.querySelector('.materials-title');
        if (materialsTitle) {
            materialsTitle.textContent = t('materialsNeeded');
        }
        
        // Translate "Instructions"
        const instructionsTitle = card.querySelector('.instructions-title');
        if (instructionsTitle) {
            instructionsTitle.textContent = t('instructions');
        }
        
        // Translate "more steps"
        const moreStepsBtn = card.querySelector('.more-steps');
        if (moreStepsBtn) {
            const match = moreStepsBtn.textContent.match(/\+ (\d+)/);
            if (match) {
                const num = match[1];
                moreStepsBtn.textContent = `+ ${num} ${t('moreSteps')}`;
            }
        }
        
        // Translate "Start Activity"
        const startBtn = card.querySelector('.start-activity-btn');
        if (startBtn) {
            startBtn.textContent = t('startActivity');
        }
    });
}

// Current activity being viewed
let currentActivityId = null;
let currentActivityData = null;
let currentStep = 0;

// DOM Elements
const modal = document.getElementById('activityModal');
const closeModalBtn = document.getElementById('closeModal');
const completeBtn = document.getElementById('completeBtn');
const pauseBtn = document.getElementById('pauseBtn');

// Modal content elements
const modalTitle = document.querySelector('.modal-title');
const stepIndicator = document.querySelector('.modal-step-indicator');
const progressBar = document.getElementById('progressBar');
const progressText = document.querySelector('.progress-text');
const activityIntro = document.querySelector('.activity-intro');
const stepNumber = document.querySelector('.step-num');
const stepInstruction = document.querySelector('.step-text p');

// Filter elements
const loadingSpinner = document.getElementById('loadingSpinner');
const activitiesGrid = document.querySelector('.activities-grid');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Detect current language (variable already declared in HTML)
    const urlParams = new URLSearchParams(window.location.search);
    currentLanguage = urlParams.get('lang') || localStorage.getItem('userLanguage') || 'en';
    
    // Update page text based on language
    updatePageText();
    
    // Translate existing activity cards
    translateExistingCards();
    
    setupFilterListeners();
    setupModalListeners();
    setupNewIdeasButton();
});

// Setup filter listeners
function setupFilterListeners() {
    const activityTypeDropdown = document.getElementById('activity-type');
    const childSelectionDropdown = document.getElementById('child-selection');
    
    if (activityTypeDropdown) {
        activityTypeDropdown.addEventListener('change', function() {
            loadActivities();
        });
    }
    
    if (childSelectionDropdown) {
        childSelectionDropdown.addEventListener('change', function() {
            loadActivities();
        });
    }
}

// Load activities via AJAX
function loadActivities() {
    const activityTypeDropdown = document.getElementById('activity-type');
    const childSelectionDropdown = document.getElementById('child-selection');
    
    const category = activityTypeDropdown ? activityTypeDropdown.value : 'all';
    const child = childSelectionDropdown ? childSelectionDropdown.value : 'all';
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    if (activitiesGrid) {
        activitiesGrid.classList.add('loading');
    }
    
    // Fetch activities with current language
    const url = `/activities/api/activities?category=${category}&child=${child}&lang=${currentLanguage}&limit=6`;
    console.log('Fetching from:', url);
    
    fetch(url)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            renderActivities(data);
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            if (activitiesGrid) {
                activitiesGrid.classList.remove('loading');
            }
        })
        .catch(error => {
            console.error('Error loading activities:', error);
            loadingSpinner.style.display = 'none';
            if (activitiesGrid) {
                activitiesGrid.classList.remove('loading');
                activitiesGrid.innerHTML = '<p style="text-align: center; padding: 40px; color: #999;">Failed to load activities. Please try again.</p>';
            }
        });
}

// Render activities in the grid
function renderActivities(activities) {
    if (!activitiesGrid) return;
    
    if (activities.length === 0) {
        activitiesGrid.innerHTML = `<p style="text-align: center; padding: 40px; color: #999;">${t('noActivities')}</p>`;
        return;
    }
    
    let html = '';
    
    activities.forEach(activity => {
        const title = currentLanguage === 'ar' ? activity.title_ar : activity.title_en;
        const description = currentLanguage === 'ar' ? activity.description_ar : activity.description_en;

        html += `
            <div class="activity-card" data-activity-id="${activity.id}">
                <div class="activity-header">
                    <h3 class="activity-title">${title}</h3>
                    <span class="activity-duration">${activity.duration}</span>
                </div>
                
                <p class="activity-age">${t('agesLabel')}: ${activity.age_range}</p>
                <p class="activity-description">${description}</p>
                
                <div class="materials-section">
                    <h4 class="materials-title">${t('materialsNeeded')}</h4>
                    <div class="materials-list">
                        ${renderMaterials(activity.materials)}
                    </div>
                </div>

                <div class="instructions-section">
                    <h4 class="instructions-title">${t('instructions')}</h4>
                    <ol class="instructions-list">
                        ${renderInstructions(activity.steps)}
                    </ol>
                    ${activity.steps.length > 2 ? `<button class="more-steps">+ ${activity.steps.length - 2} ${t('moreSteps')}</button>` : ''}
                </div>

                <button class="start-activity-btn" onclick="openActivity(${activity.id})">${t('startActivity')}</button>
            </div>
        `;
    });
    
    activitiesGrid.innerHTML = html;
}

// Helper function to render materials
function renderMaterials(materials) {
    if (!materials || materials.length === 0) return `<p style="color: #999; font-size: 13px;">${t('noMaterials')}</p>`;
    
    const colors = ['purple', 'green', 'orange', 'red', 'blue'];
    
    return materials.map((material, index) => {
        const color = colors[index % colors.length];
        const materialName = typeof material === 'string' 
            ? material 
            : (currentLanguage === 'ar' ? (material.name_ar || material.name_en) : (material.name_en || material.name_ar));
        const materialIcon = typeof material === 'object' ? (material.icon || '') : '';
        const icon = materialIcon ? `<span class="material-icon">${materialIcon}</span>` : '';
        return `<div class="material-badge ${color}">${icon}<span>${materialName}</span></div>`;
    }).join('');
}

// Helper function to render instructions (first 2 steps)
function renderInstructions(steps) {
    if (!steps || steps.length === 0) return '<li>No instructions available</li>';
    
    const firstTwo = steps.slice(0, 2);
    return firstTwo.map(step => {
        const truncated = step.length > 60 ? step.substring(0, 60) + '...' : step;
        return `<li>${truncated}</li>`;
    }).join('');
}

// Setup "Get New Ideas" button
function setupNewIdeasButton() {
    const newIdeasBtn = document.querySelector('.new-ideas-btn');
    if (newIdeasBtn) {
        newIdeasBtn.addEventListener('click', function() {
            loadActivities();
        });
    }
}

// Open activity modal
function openActivity(activityId) {
    currentActivityId = activityId;
    currentStep = 0;
    
    // Fetch activity data
    fetch(`/activities/api/activity/${activityId}?lang=en`)
        .then(response => response.json())
        .then(data => {
            currentActivityData = data;
            openModal();
        })
        .catch(error => {
            console.error('Error loading activity:', error);
            alert('Failed to load activity. Please try again.');
        });
}

// Setup modal event listeners
function setupModalListeners() {
    // Close modal
    closeModalBtn.addEventListener('click', closeModal);
    
    // Close on outside click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Mark as complete
    completeBtn.addEventListener('click', function() {
        if (currentStep < currentActivityData.steps.length - 1) {
            currentStep++;
            updateModalContent();
        } else {
            alert('🎉 Congratulations! Activity completed!');
            closeModal();
        }
    });
    
    // Pause & Celebrate
    pauseBtn.addEventListener('click', function() {
        alert('🌟 Great job! Take a break and celebrate!');
        closeModal();
    });
    
    // ESC key to close
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

// Open modal
function openModal() {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    updateModalContent();
}

// Close modal
function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Update modal content
function updateModalContent() {
    if (!currentActivityData) return;
    
    // Get correct language steps
    const steps = currentLanguage === 'ar' && currentActivityData.steps_ar
        ? currentActivityData.steps_ar 
        : currentActivityData.steps_en;
    
    const totalSteps = steps.length;
    
    // Update title
    const title = currentLanguage === 'ar' && currentActivityData.title_ar
        ? currentActivityData.title_ar
        : currentActivityData.title_en;
    modalTitle.textContent = title;
    
    // Update step indicator
    stepIndicator.innerHTML = `Step ${currentStep + 1} of ${totalSteps}`;
    
    // Update progress bar
    const progressPercentage = ((currentStep + 1) / totalSteps) * 100;
    progressBar.style.width = progressPercentage + '%';
    
    // Update progress text
    progressText.textContent = `${currentStep + 1}/${totalSteps} steps`;
    
    // Update intro
    const description = currentLanguage === 'ar' && currentActivityData.description_ar
        ? currentActivityData.description_ar
        : currentActivityData.description_en;
    activityIntro.textContent = description;
    
    // Update step number
    stepNumber.textContent = currentStep + 1;
    
    // Update step instruction
    stepInstruction.textContent = steps[currentStep];
    
    // Update button text on last step
    if (currentStep === totalSteps - 1) {
        completeBtn.textContent = t('finishActivity');
    } else {
        completeBtn.textContent = t('markComplete');
    }
}