from datetime import date

from conftest import add_child, register
from db.models import db, Child, Meal, User


SAMPLE_MEAL = {
    'name_en': 'Chicken Machboos',
    'name_ar': 'مجبوس دجاج',
    'ingredients': [
        {'name_en': 'Chicken', 'name_ar': 'دجاج', 'amount': '500g', 'icon': '🍗'},
        {'name_en': 'Rice', 'name_ar': 'أرز', 'amount': '2 cups', 'icon': '🍚'},
    ],
    'instructions_en': ['Step 1: Say Bismillah', 'Step 2: Cook'],
    'instructions_ar': 'الخطوة 1: قل بسم الله',
    'prep_time': 15,
    'cook_time': '40 minutes',
    'nutritional_benefits_en': 'Protein',
    'nutritional_benefits_ar': 'بروتين',
    'why_healthy_en': 'Good for growth',
    'why_healthy_ar': 'مفيد للنمو',
}


# ---------- general ----------

def test_health_check(client):
    assert client.get('/healthz').get_json() == {'status': 'ok'}


def test_unknown_page_shows_friendly_404(client):
    response = client.get('/does-not-exist')
    assert response.status_code == 404
    assert b'Page not found' in response.data


def test_pages_require_login(client):
    for path in ['/', '/dashboard', '/activities/', '/meals/', '/meals/history', '/chatbot/', '/profile/view']:
        response = client.get(path)
        assert response.status_code == 302, path
        assert '/auth/login' in response.headers['Location']


def test_api_requires_login_with_json(client):
    response = client.get('/activities/api/activities')
    assert response.status_code == 401
    assert response.get_json()['success'] is False


# ---------- auth ----------

def test_register_and_login_flow(client):
    response = register(client, email='Sara@Example.com')
    assert response.status_code == 302
    assert '/profile/setup' in response.headers['Location']

    client.get('/auth/logout')
    response = client.post('/auth/login', data={'email': 'sara@example.com', 'password': 'password123'})
    assert response.status_code == 302
    assert client.get('/').status_code == 200


def test_register_rejects_short_password(client):
    response = register(client, password='short')
    assert response.status_code == 200
    assert b'at least 8 characters' in response.data


def test_register_rejects_duplicate_email(client):
    register(client)
    client.get('/auth/logout')
    response = register(client, email='SARA@example.com')
    assert b'Email already registered' in response.data


def test_wrong_password(client):
    register(client)
    client.get('/auth/logout')
    response = client.post('/auth/login', data={'email': 'sara@example.com', 'password': 'wrongpassword'})
    assert b'Invalid email or password' in response.data


# ---------- profile ----------

def test_setup_is_prefilled_and_profile_page_renders(logged_in):
    page = logged_in.get('/profile/setup').get_data(as_text=True)
    assert 'value="kitchen" checked' in page
    assert 'value="07:30"' in page

    add_child(logged_in, interests=['reading'], dietary_restrictions=['nuts'])
    page = logged_in.get('/profile/view').get_data(as_text=True)
    assert 'Omar' in page
    assert 'Kitchen Access' in page
    assert 'Nuts' in page


def test_add_child_rejects_future_birthdate(logged_in):
    response = add_child(logged_in, birthdate=f'{date.today().year + 1}-01-01')
    assert b'cannot be in the future' in response.data


def test_delete_child_only_own(app, client):
    register(client, email='a@example.com')
    add_child(client)
    client.get('/auth/logout')
    register(client, name='Other', email='b@example.com')

    with app.app_context():
        child_id = Child.query.filter_by(name='Omar').first().id

    assert client.post(f'/profile/child/{child_id}/delete').status_code == 404

    client.get('/auth/logout')
    client.post('/auth/login', data={'email': 'a@example.com', 'password': 'password123'})
    assert client.post(f'/profile/child/{child_id}/delete').status_code == 302
    with app.app_context():
        assert db.session.get(Child, child_id) is None


# ---------- activities ----------

def test_activities_page_has_seeded_activities(logged_in):
    response = logged_in.get('/activities/')
    assert response.status_code == 200
    assert b'activity' in response.data.lower()


def test_toddler_under_two_still_gets_activities(app, logged_in):
    this_year = date.today().year
    add_child(logged_in, name='Baby', birthdate=f'{this_year - 1}-01-01')
    with app.app_context():
        baby_id = Child.query.filter_by(name='Baby').first().id

    activities = logged_in.get(f'/activities/api/activities?child={baby_id}').get_json()
    assert len(activities) > 0
    assert all(a['age_range'] == '2-3 years' for a in activities)


def test_complete_activity_and_dashboard(logged_in):
    activity = logged_in.get('/activities/api/activities?limit=1').get_json()[0]

    response = logged_in.post('/activities/api/complete', json={'activity_id': activity['id']})
    assert response.get_json()['success'] is True
    assert logged_in.get('/activities/api/stats').get_json()['completed_count'] == 1

    assert logged_in.post('/activities/api/complete', json={'activity_id': 999999}).status_code == 404
    assert logged_in.get('/dashboard').status_code == 200


# ---------- meals ----------

def test_meal_generation_without_api_key_shows_message(logged_in):
    response = logged_in.post('/meals/generate', data={
        'ingredients': ['Chicken'], 'meal_type': 'lunch', 'language': 'en',
    }, follow_redirects=True)
    assert b'GEMINI_API_KEY' in response.data


def test_meal_generate_view_history_favorite_regenerate_delete(app, logged_in, monkeypatch):
    import app.meal_recommender.meal_generator as meal_generator
    monkeypatch.setattr(meal_generator, 'generate_json', lambda *a, **k: dict(SAMPLE_MEAL))

    response = logged_in.post('/meals/generate', data={
        'ingredients': ['Chicken'], 'meal_type': 'lunch', 'language': 'en',
    })
    assert response.status_code == 302
    assert '/meals/view/' in response.headers['Location']

    with app.app_context():
        meal = Meal.query.first()
        meal_id = meal.id
        assert meal.prep_time == '15'
        assert [i['name_en'] for i in meal.get_missing_ingredients()] == ['Rice']

    assert b'Chicken Machboos' in logged_in.get(f'/meals/view/{meal_id}').data
    assert b'Chicken Machboos' in logged_in.get('/meals/history').data
    assert logged_in.post(f'/meals/favorite/{meal_id}').get_json()['is_favorite'] is True

    modified = dict(SAMPLE_MEAL, name_en='Lighter Machboos')
    monkeypatch.setattr(meal_generator, 'generate_json', lambda *a, **k: modified)
    response = logged_in.post(f'/meals/regenerate/{meal_id}', json={'feedback': 'less oil'})
    assert response.get_json()['success'] is True
    with app.app_context():
        assert db.session.get(Meal, meal_id).name_en == 'Lighter Machboos'

    assert logged_in.post(f'/meals/delete/{meal_id}').get_json()['success'] is True
    assert b'No meals yet' in logged_in.get('/meals/history').data


def test_other_family_cannot_access_meal(app, client, monkeypatch):
    import app.meal_recommender.meal_generator as meal_generator
    monkeypatch.setattr(meal_generator, 'generate_json', lambda *a, **k: dict(SAMPLE_MEAL))

    register(client, email='a@example.com')
    client.post('/meals/generate', data={'ingredients': ['Rice'], 'meal_type': 'lunch'})
    with app.app_context():
        meal_id = Meal.query.first().id
    client.get('/auth/logout')

    register(client, name='Other', email='b@example.com')
    assert client.get(f'/meals/view/{meal_id}').status_code == 302
    assert client.post(f'/meals/favorite/{meal_id}').status_code == 403
    assert client.post(f'/meals/delete/{meal_id}').status_code == 403


# ---------- chatbot ----------

def test_chat_send_message_and_title(app, logged_in, monkeypatch):
    import app.chatbot.chat_ai as chat_ai
    calls = []

    def fake_generate_text(contents, system_instruction=None, **kwargs):
        calls.append((contents, system_instruction))
        return 'Picky Eating Tips' if system_instruction is None else 'Try offering small portions.'

    monkeypatch.setattr(chat_ai, 'generate_text', fake_generate_text)
    add_child(logged_in)

    response = logged_in.post('/chatbot/api/send-message', json={'message': 'My son is a picky eater'})
    data = response.get_json()
    assert data['success'] is True
    assert data['ai_message']['message_text'] == 'Try offering small portions.'
    assert 'Omar' in calls[0][1]  # family context reaches the system prompt

    conversations = logged_in.get('/chatbot/api/conversations').get_json()['conversations']
    assert conversations[0]['title'] == 'Picky Eating Tips'

    # Follow-up messages include the earlier conversation
    logged_in.post('/chatbot/api/send-message', json={
        'message': 'What about vegetables?', 'conversation_id': data['conversation_id'],
    })
    assert len(calls[-1][0]) == 3


def test_chat_without_api_key_returns_friendly_error(logged_in):
    data = logged_in.post('/chatbot/api/send-message', json={'message': 'Hello'}).get_json()
    assert data['success'] is True
    assert 'Sorry' in data['ai_message']['message_text']


def test_chat_rejects_empty_message(logged_in):
    assert logged_in.post('/chatbot/api/send-message', json={'message': '   '}).status_code == 400
