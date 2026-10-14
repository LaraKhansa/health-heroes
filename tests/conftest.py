"""
Test setup: a throwaway SQLite database and no real AI calls
"""

import os
import sys
import tempfile

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

# Must be set before main is imported, because main configures the app at import time
_db_dir = tempfile.mkdtemp()
os.environ['DATABASE_URL'] = f"sqlite:///{os.path.join(_db_dir, 'test.db')}"
os.environ['SECRET_KEY'] = 'test-secret'
os.environ.pop('GEMINI_API_KEY', None)
os.environ.pop('GOOGLE_API_KEY', None)
os.environ['APP_ENV'] = 'development'

from main import app as flask_app  # noqa: E402
from db.models import db, User, FamilyProfile, Child, ChatConversation, Meal, ActivityCompletion  # noqa: E402


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app
    # Clean user data between tests, keep the seeded activities
    with flask_app.app_context():
        for model in (ActivityCompletion, Meal, ChatConversation, Child, FamilyProfile, User):
            for row in model.query.all():
                db.session.delete(row)
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, name='Sara', email='sara@example.com', password='password123'):
    return client.post('/auth/register', data={
        'name': name,
        'email': email,
        'password': password,
        'confirm_password': password,
    })


def add_child(client, name='Omar', birthdate='2021-03-15', **extra):
    data = {'name': name, 'birthdate': birthdate, 'gender': 'male'}
    data.update(extra)
    return client.post('/profile/add-child', data=data)


@pytest.fixture
def logged_in(client):
    register(client)
    client.post('/profile/setup', data={
        'language': 'en',
        'home_resources': ['kitchen', 'living_room'],
        'breakfast_time': '07:30',
        'lunch_time': '13:00',
        'dinner_time': '19:00',
    })
    return client
