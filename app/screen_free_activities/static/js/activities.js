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
    
    // Fetch activities
    const url = `/activities/api/activities?category=${category}&child=${child}&lang=en&limit=6`;
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
        activitiesGrid.innerHTML = '<p style="text-align: center; padding: 40px; color: #999;">No activities available. Try changing filters!</p>';
        return;
    }
    
    let html = '';
    
    activities.forEach(activity => {
        html += `
            <div class="activity-card" data-activity-id="${activity.id}">
                <div class="activity-header">
                    <h3 class="activity-title">${activity.title}</h3>
                    <span class="activity-duration">${activity.duration}</span>
                </div>
                
                <p class="activity-age">Ages: ${activity.age_range}</p>
                <p class="activity-description">${activity.description}</p>
                
                <div class="materials-section">
                    <h4 class="materials-title">Materials Needed</h4>
                    <div class="materials-list">
                        ${renderMaterials(activity.materials)}
                    </div>
                </div>

                <div class="instructions-section">
                    <h4 class="instructions-title">Instructions</h4>
                    <ol class="instructions-list">
                        ${renderInstructions(activity.steps)}
                    </ol>
                    ${activity.steps.length > 2 ? `<button class="more-steps">+ ${activity.steps.length - 2} more steps...</button>` : ''}
                </div>

                <button class="start-activity-btn" onclick="openActivity(${activity.id})">Start Activity</button>
            </div>
        `;
    });
    
    activitiesGrid.innerHTML = html;
}

// Helper function to render materials
function renderMaterials(materials) {
    if (!materials || materials.length === 0) return '<p style="color: #999; font-size: 13px;">No materials needed</p>';
    
    const colors = ['purple', 'green', 'orange', 'red', 'blue'];
    
    return materials.map((material, index) => {
        const color = colors[index % colors.length];
        // Handle both object format {name: "...", icon: "..."} and string format
        const materialName = typeof material === 'string' ? material : (material.name || material.name_en || 'Material');
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
    
    const totalSteps = currentActivityData.steps.length;
    
    // Update title
    modalTitle.textContent = currentActivityData.title;
    
    // Update step indicator
    stepIndicator.innerHTML = `Step ${currentStep + 1} of ${totalSteps}`;
    
    // Update progress bar
    const progressPercentage = ((currentStep + 1) / totalSteps) * 100;
    progressBar.style.width = progressPercentage + '%';
    
    // Update progress text
    progressText.textContent = `${currentStep + 1}/${totalSteps} steps`;
    
    // Update intro
    activityIntro.textContent = currentActivityData.description;
    
    // Update step number
    stepNumber.textContent = currentStep + 1;
    
    // Update step instruction
    stepInstruction.textContent = currentActivityData.steps[currentStep];
    
    // Update button text on last step
    if (currentStep === totalSteps - 1) {
        completeBtn.textContent = 'Finish Activity! 🎉';
    } else {
        completeBtn.textContent = 'Mark as Complete';
    }
}

console.log('✅ Activities loaded successfully!');