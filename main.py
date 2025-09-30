"""
Health Heroes - Main Application Entry Point
"""

import os
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-this')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'health_heroes.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Database will be created at: {database_path}")

# Initialize database
from db import init_db
init_db(app)

# Register blueprints
from app.screen_free_activities.routes import screen_free_bp
app.register_blueprint(screen_free_bp)

# Home route
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Health Heroes</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2e7d32;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .language-selector-container {
                text-align: center;
                margin-bottom: 30px;
            }
            .language-selector-container label {
                display: block;
                margin-bottom: 10px;
                color: #555;
                font-weight: bold;
            }
            .language-selector {
                padding: 12px 20px;
                border: 3px solid #66bb6a;
                border-radius: 25px;
                font-size: 16px;
                font-weight: 600;
                color: #2e7d32;
                background: white;
                cursor: pointer;
                min-width: 200px;
            }
            .language-selector:focus {
                outline: none;
                box-shadow: 0 0 0 3px rgba(102, 187, 106, 0.3);
            }
            .links {
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-top: 30px;
            }
            a {
                background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%);
                color: white;
                padding: 15px 25px;
                text-decoration: none;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                transition: transform 0.2s;
            }
            a:hover {
                transform: translateY(-2px);
            }
            .coming-soon {
                opacity: 0.5;
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 id="mainTitle">Health Heroes</h1>
            <p class="subtitle" id="subtitle">Empowering Families for Healthier Lives</p>
            
            <!-- Language Selector -->
            <div class="language-selector-container">
                <label for="languageSelector" id="langLabel">Choose Your Language / اختر لغتك</label>
                <select class="language-selector" id="languageSelector">
                    <option value="en">English</option>
                    <option value="ar">العربية</option>
                </select>
            </div>
            
            <div class="links">
                <a href="/activities?lang=en" id="activitiesLink">Screen-Free Activities</a>
                <a href="#" class="coming-soon" id="mealsLink">Meal Recommender (Coming Soon)</a>
                <a href="#" class="coming-soon" id="chatLink">AI Chat (Coming Soon)</a>
                <a href="#" class="coming-soon" id="dashboardLink">Progress Dashboard (Coming Soon)</a>
            </div>
        </div>
        
        <script>
            // Get language from localStorage or default to 'en'
            let currentLang = localStorage.getItem('userLanguage') || 'en';
            document.getElementById('languageSelector').value = currentLang;
            
            // Update content based on current language
            updateContent(currentLang);
            
            // Listen for language changes
            document.getElementById('languageSelector').addEventListener('change', function() {
                currentLang = this.value;
                localStorage.setItem('userLanguage', currentLang);
                updateContent(currentLang);
            });
            
            function updateContent(lang) {
                const activitiesLink = document.getElementById('activitiesLink');
                activitiesLink.href = '/activities?lang=' + lang;
                
                if (lang === 'ar') {
                    document.getElementById('mainTitle').textContent = 'أبطال الصحة';
                    document.getElementById('subtitle').textContent = 'تمكين العائلات لحياة أكثر صحة';
                    document.getElementById('activitiesLink').textContent = 'أنشطة بدون شاشات';
                    document.getElementById('mealsLink').textContent = 'توصيات الوجبات (قريباً)';
                    document.getElementById('chatLink').textContent = 'الدردشة الذكية (قريباً)';
                    document.getElementById('dashboardLink').textContent = 'لوحة التقدم (قريباً)';
                    document.body.style.direction = 'rtl';
                } else {
                    document.getElementById('mainTitle').textContent = 'Health Heroes';
                    document.getElementById('subtitle').textContent = 'Empowering Families for Healthier Lives';
                    document.getElementById('activitiesLink').textContent = 'Screen-Free Activities';
                    document.getElementById('mealsLink').textContent = 'Meal Recommender (Coming Soon)';
                    document.getElementById('chatLink').textContent = 'AI Chat (Coming Soon)';
                    document.getElementById('dashboardLink').textContent = 'Progress Dashboard (Coming Soon)';
                    document.body.style.direction = 'ltr';
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 70)
    print("  🌟 HEALTH HEROES - Starting Application")
    print("=" * 70)
    app.run(debug=True, port=5000)