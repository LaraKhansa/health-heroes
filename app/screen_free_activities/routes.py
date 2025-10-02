from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from db.models import db, Activity, User, FamilyProfile, Child, ActivityCompletion
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
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Get user and family profile
    user = User.query.get(user_id)
    family_profile = FamilyProfile.query.filter_by(user_id=user_id).first()
    
    # Get all children
    children = Child.query.filter_by(family_profile_id=family_profile.id).all() if family_profile else []
    
    # Get home resources from profile
    home_resources = family_profile.get_home_resources() if family_profile else []
    
    # Get user name for display
    user_name = session.get('user_name', 'User')
    
    # Get filters from query params
    category_filter = request.args.get('category', 'all')
    child_filter = request.args.get('child', 'all')
    language = request.args.get('lang', family_profile.language if family_profile else 'en')
    
    # Base query - get all activities
    query = Activity.query
    
    # Filter by category if specified
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    # Filter by child's age if specified
    selected_child = None
    if child_filter != 'all':
        try:
            child_id = int(child_filter)
            selected_child = Child.query.get(child_id)
            if selected_child:
                age_range = selected_child.get_age_range()
                query = query.filter_by(age_range=age_range)
        except (ValueError, TypeError):
            pass
    
    # Get all matching activities
    all_activities = query.all()
    
    # Smart sorting: prioritize activities matching home resources and interests
    if all_activities:
        scored_activities = []
        child_interests = selected_child.get_interests() if selected_child else []
        
        for activity in all_activities:
            score = 0
            
            # Boost score if matches child's interests
            if child_interests:
                # Map category to interests
                category_interest_map = {
                    'games': 'sports',
                    'cooking': 'cooking',
                    'creative': 'arts',
                    'nature': 'outdoor',
                    'reading': 'reading',
                    'science': 'science'
                }
                if activity.category in category_interest_map:
                    if category_interest_map[activity.category] in child_interests:
                        score += 10
            
            # Boost score if matches home resources
            activity_requirements = activity.get_home_requirements()
            if activity_requirements:
                for req in activity_requirements:
                    if req in home_resources:
                        score += 5
            
            scored_activities.append((activity, score))
        
        # Sort by score (highest first)
        scored_activities.sort(key=lambda x: x[1], reverse=True)
        
        # Select top activities (max 6)
        if len(scored_activities) > 6:
            # Take some high-scored and some random for variety
            top_activities = [act for act, score in scored_activities[:4]]
            remaining = [act for act, score in scored_activities[4:]]
            if len(remaining) >= 2:
                top_activities.extend(random.sample(remaining, 2))
            else:
                top_activities.extend(remaining)
            activities = top_activities
        else:
            activities = [act for act, score in scored_activities]
    else:
        activities = []
    
    return render_template(
        'activities_list.html',
        activities=activities,
        home_resources=home_resources,
        children=children,
        language=language,
        category_filter=category_filter,
        child_filter=child_filter,
        user_name=user_name,
        total_activities=len(all_activities)
    )


@screen_free_bp.route('/api/activities')
def api_get_activities():
    """
    API endpoint to get activities (for "Get New Ideas" button)
    Returns different random activities each time
    """
    category_filter = request.args.get('category', 'all')
    child_filter = request.args.get('child', 'all')
    language = request.args.get('lang', 'en')
    limit = int(request.args.get('limit', 6))
    
    # Base query
    query = Activity.query
    
    # Filter by category
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    # Filter by child's age if specified
    if child_filter != 'all':
        try:
            child_id = int(child_filter)
            selected_child = Child.query.get(child_id)
            if selected_child:
                age_range = selected_child.get_age_range()
                print(f"DEBUG API: Child {selected_child.name}, Age: {selected_child.get_age()}, Age Range: {age_range}")
                query = query.filter_by(age_range=age_range)
        except (ValueError, TypeError):
            pass  # Invalid child_filter, ignore
    
    # Get ALL matching activities first
    all_activities = query.all()
    
    # If "All Activities" is selected and no child filter, get diverse selection
    if category_filter == 'all' and child_filter == 'all':
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

@screen_free_bp.route('/api/complete', methods=['POST'])
def api_complete_activity():
    """
    Mark an activity as completed
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    data = request.get_json()
    activity_id = data.get('activity_id')
    
    if not activity_id:
        return jsonify({'success': False, 'error': 'Missing activity_id'})
    
    # Check if already completed
    existing = ActivityCompletion.query.filter_by(
        user_id=user_id,
        activity_id=activity_id
    ).first()
    
    if existing:
        return jsonify({'success': True, 'message': 'Already completed'})
    
    # Create new completion
    completion = ActivityCompletion(
        user_id=user_id,
        activity_id=activity_id
    )
    
    db.session.add(completion)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Activity completed!'})


@screen_free_bp.route('/api/stats')
def api_get_stats():
    """
    Get user activity statistics
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'completed_count': 0, 'badge': None})
    
    # Count completed activities
    completed_count = ActivityCompletion.query.filter_by(user_id=user_id).count()
    
    # Determine badge
    badge = None
    if completed_count >= 50:
        badge = {'name': 'Champion', 'icon': '🏆', 'color': 'gold'}
    elif completed_count >= 25:
        badge = {'name': 'Expert', 'icon': '⭐', 'color': 'purple'}
    elif completed_count >= 10:
        badge = {'name': 'Explorer', 'icon': '🌟', 'color': 'blue'}
    elif completed_count >= 5:
        badge = {'name': 'Beginner', 'icon': '✨', 'color': 'green'}
    
    return jsonify({
        'completed_count': completed_count,
        'badge': badge
    })

@screen_free_bp.route('/api/activity/<int:activity_id>')
def api_get_activity(activity_id):
    """
    Get a specific activity by ID
    Used when opening the activity detail modal
    """
    language = request.args.get('lang', 'en')
    
    activity = Activity.query.get_or_404(activity_id)
    
    return jsonify(activity.to_dict(language=language))