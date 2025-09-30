from flask import Blueprint, render_template, jsonify, request
from db.models import db, Activity
from sqlalchemy import func
import random

# Create blueprint
screen_free_bp = Blueprint(
    'screen_free',
    __name__,
    url_prefix='/activities',
    template_folder='templates',
    static_folder='static',
    static_url_path='/activities/static'
)


@screen_free_bp.route('/')
def activities_list():
    """
    Main activities page
    Shows filtered activities based on user preferences
    """
    # For now, hardcode home resources (later from family profile)
    home_resources = ["balcony", "kitchen"]
    
    # Get filters from query params (for dynamic filtering)
    category_filter = request.args.get('category', 'all')
    child_filter = request.args.get('child', 'all')
    language = request.args.get('lang', 'en')  # Language preference
    
    # Base query - get all activities
    query = Activity.query
    
    # Filter by category if specified
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    # Filter by home resources (show activities that match user's home)
    # For now, show all activities (we'll add smart filtering later)
    
    # Get random 6 activities for display
    all_activities = query.all()
    
    if len(all_activities) > 6:
        activities = random.sample(all_activities, 6)
    else:
        activities = all_activities
    
    return render_template(
        'activities_list.html',
        activities=activities,
        home_resources=home_resources,
        language=language,
        category_filter=category_filter,
        child_filter=child_filter
    )


@screen_free_bp.route('/api/activities')
def api_get_activities():
    """
    API endpoint to get activities (for "Get New Ideas" button)
    Returns different random activities each time
    """
    category_filter = request.args.get('category', 'all')
    language = request.args.get('lang', 'en')
    limit = int(request.args.get('limit', 6))
    
    # Base query
    query = Activity.query
    
    # Filter by category
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
        # Get ALL matching activities first
        all_activities = query.all()
    else:
        # When "All Activities" is selected, get diverse selection from all categories
        all_activities = Activity.query.all()
        
        # Group activities by category
        from collections import defaultdict
        activities_by_category = defaultdict(list)
        for activity in all_activities:
            activities_by_category[activity.category].append(activity)
        
        # Try to get at least one from each category if possible
        diverse_activities = []
        categories = list(activities_by_category.keys())
        
        # First pass: get one from each category
        for category in categories:
            if len(diverse_activities) < limit and activities_by_category[category]:
                activity = random.choice(activities_by_category[category])
                diverse_activities.append(activity)
                activities_by_category[category].remove(activity)
        
        # Second pass: fill remaining slots randomly from remaining activities
        remaining = []
        for cat_activities in activities_by_category.values():
            remaining.extend(cat_activities)
        
        if remaining and len(diverse_activities) < limit:
            needed = limit - len(diverse_activities)
            if len(remaining) >= needed:
                diverse_activities.extend(random.sample(remaining, needed))
            else:
                diverse_activities.extend(remaining)
        
        all_activities = diverse_activities
    
    # If we have more activities than requested, randomly sample WITHOUT replacement
    if len(all_activities) > limit:
        activities = random.sample(all_activities, limit)
    else:
        activities = all_activities
    
    # Convert to dict - this ensures unique activities
    activities_data = [activity.to_dict(language=language) for activity in activities]
    
    return jsonify(activities_data)


@screen_free_bp.route('/api/activity/<int:activity_id>')
def api_get_activity(activity_id):
    """
    Get a specific activity by ID
    Used when opening the activity detail modal
    """
    language = request.args.get('lang', 'en')
    
    activity = Activity.query.get_or_404(activity_id)
    
    return jsonify(activity.to_dict(language=language))