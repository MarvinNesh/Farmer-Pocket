from flask import Flask, render_template
from .extensions import db, login_manager
from .models import User
import os

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'a-very-secret-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../resources/users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .scanner import scanner_bp
    app.register_blueprint(scanner_bp)

    @app.route('/')
    def dashboard():
        """lending page"""
        fact = None
        try:
            import google.generativeai as genai
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                prompt = "Tell me one interesting and surprising 'did you know' fact about livestock (e.g., cows, goats, sheep, chickens, pigs)."
                response = model.generate_content(prompt)
                fact = response.text
        except Exception:
            # If the API call fails  show this fact.\\\\
            fact = "Did you know? Cows have an excellent sense of smell and can detect odors up to six miles away."

        return render_template('index.html', fact=fact)

    with app.app_context():
        db.create_all()

    return app