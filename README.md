# Afiyah⭐ 

> Empowering Families for Healthier Lives

A culturally-sensitive, AI-powered family health companion designed to help parents and caregivers in the UAE nurture healthier lifestyles for children aged 0–8.



## 🎯 About the Project

**Afiyah** is part of the startAD AI for Good Sandbox challenge, tackling the **Homegrown Health Heroes** challenge to combat childhood obesity in the UAE through:

- Personalized nutrition and meal recommendations
- Screen-free activity suggestions
- AI-powered parental support
- Bilingual support (Arabic & English)
- Cultural sensitivity for UAE families

### Challenge Context
This solution addresses childhood obesity by supporting families with practical tools to consistently nurture healthy eating and active living habits at home.



## ✨ Features

### Currently Implemented
- ✅ **User Authentication** - Register, login, and secure sessions
- ✅ **Family Profile Setup** - Customize home resources, meal times, and language preferences
- ✅ **Child Management** - Add multiple children with ages, interests, and dietary restrictions
- ✅ **Screen-Free Activities** - Bilingual (Arabic/English) activity suggestions
- ✅ **Activity Filtering** - Filter by category, child age, and home resources
- ✅ **Activity Tracking** - Mark activities as complete and earn badges
- ✅ **Progress Dashboard** - View family activity statistics
- ✅ **Meal Recommender** - Personalized meal suggestions based on family preferences, dietary restrictions, and cultural context
- ✅ **AI Chat Companion for parental support** 




## 🛠 Tech Stack

- **Backend:** Flask (Python 3.10+)
- **Database:** SQLite (via Flask-SQLAlchemy)
- **AI:** Google Gemini API (chatbot, meal recommendations, activity generation)
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Custom CSS with Google Fonts
- **Deployment:** Gunicorn, with a Dockerfile and Procfile included


## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/LaraKhansa/health-heroes.git
cd health-heroes
```

### 2. Create a virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | For AI features | Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). Powers the chatbot and meal recommender. |
| `SECRET_KEY` | Yes in production | Random string that signs login sessions. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `GEMINI_MODEL` | No | Gemini model to use (default `gemini-2.5-flash`) |
| `DATABASE_URL` | No | Database location (default `sqlite:///health_heroes.db` in the project folder) |
| `APP_ENV` | No | Set to `production` to require `SECRET_KEY`, enable secure cookies and turn off debug mode |

> The app runs without `GEMINI_API_KEY`: login, profiles, activities and the dashboard all work, and the AI features show a friendly message until a key is added.

### 5. Run the application

```bash
python main.py
```

Open `http://localhost:5000`, create an account, set up your family profile and add your children.

The database is created automatically on first run and filled with **24 starter activities** in English and Arabic (one per category and age group), so the activities page works straight away.

---

## 🎯 Generating More Activities (optional)

The starter set is a small sample. To generate a full, AI-written activity library with Gemini:

```bash
python utils/populate_activities.py --generate 3
```

This creates 3 activities for every combination of home area, category and age group (120 API calls, about 15 minutes). It replaces the existing activities only after generation succeeds. Other options:

```bash
python utils/populate_activities.py --stats   # show what is in the database
python utils/populate_activities.py --seed    # reset to the bundled starter activities
```

---

## 🌐 Deploying

The app is ready for any platform that runs Python or Docker.

**Docker**

```bash
docker build -t afiyah .
docker run -p 8000:8000 \
  -e SECRET_KEY=your_secret_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -v afiyah-data:/app/data \
  afiyah
```

The `-v` volume keeps the SQLite database between restarts.

**Render, Railway, Heroku and similar**

A `Procfile` is included. Set `APP_ENV=production`, `SECRET_KEY` and `GEMINI_API_KEY` in the platform's environment settings. If the platform's disk is temporary, point `DATABASE_URL` at a persistent disk so user data is not lost on redeploy.

A health check endpoint is available at `/healthz`.

---

## 🧪 Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The tests use a temporary database and mock all AI calls, so no API key is needed.

---

## 📁 Project Structure

```
main.py                     App entry point and configuration
app/
  ai_client.py              Shared Gemini client used by every AI feature
  decorators.py             login_required
  auth/                     Register, login, logout
  profile/                  Family setup, children, profile page
  screen_free_activities/   Activity suggestions and tracking
  meal_recommender/         AI meal generation, history, favorites
  chatbot/                  AI parenting assistant
  dashboard/                Family progress statistics
db/
  models.py                 Database models
  seed_activities.json      Starter activities loaded on first run
utils/
  populate_activities.py    Generate activities with Gemini
templates/, static/         Shared layout, header, navigation and styles
tests/                      Automated tests
```

---

## 👥 Team Members

- **Lara Al Khansa**
- **Mohammad Ali Oussayli**
- **Maab Majzoub**


**Made with ❤️ for healthier families in the UAE**
