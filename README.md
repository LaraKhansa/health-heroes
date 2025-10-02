# Health Heroes ⭐

> Empowering Families for Healthier Lives

A culturally-sensitive, AI-powered family health companion designed to help parents and caregivers in the UAE nurture healthier lifestyles for children aged 0–8.



## 🎯 About the Project

**Health Heroes** is part of the startAD AI for Good Sandbox challenge, tackling the **Homegrown Health Heroes** challenge to combat childhood obesity in the UAE through:

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

### Coming Soon
- 🔄 AI Chat Companion for parental support
- 🔄 Enhanced Progress Analytics
- 🔄 Nutrition tracking



## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **AI:** Google Gemini API (for activity generation and meal recommendations)
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Custom CSS with Google Fonts
- **Deployment:** TBD



## 🚀 Getting Started

### Installation

Follow these steps to set up the project locally:

#### 1. Clone the Repository

```bash
git clone https://github.com/LaraKhansa/health-heroes.git
cd health-heroes
```

#### 2. Create a Virtual Environment

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

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following to your `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
```

> **Note:** Replace `your_gemini_api_key_here` with your actual Google Gemini API key.
> For `SECRET_KEY`, you can generate a random string or use: `python -c "import secrets; print(secrets.token_hex(16))"`

#### 5. Initialize the Database

```bash
python init_db.py
```

#### 6. ⚠️ **IMPORTANT: Populate Activities Database**

**The activities feature requires pre-populated data in the database to function correctly.**

Run the activity population script:

```bash
python populate_activities.py
```

This script will:
- Generate diverse screen-free activities for different age groups
- Add activities in both English and Arabic
- Categorize activities (physical, creative, learning, etc.)
- Match activities with appropriate home resources

**Without this step, the activities page will appear empty!**

#### 7. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

---


**Made with ❤️ for healthier families in the UAE**
