"""
Shared route decorators
"""

from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for


def login_required(f):
    """Require a logged-in user. API routes get a JSON 401 instead of a redirect."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if '/api/' in request.path:
                return jsonify({'success': False, 'error': 'Not logged in'}), 401
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
