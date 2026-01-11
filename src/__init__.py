import os
from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv
import google.generativeai as genai

from .extensions import db, migrate
from .models import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load environment variables from .env file
    load_dotenv()

    database_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set. Please configure it in your .env file or environment variables.")
    if not secret_key:
        raise RuntimeError("SECRET_KEY is not set. Please configure it in your .env file or environment variables.")

    # Convert postgres:// to postgresql:// if needed
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if gemini_api_key:
        try:
            genai.configure(api_key=gemini_api_key)
        except ImportError:
            print("WARNING: google.generativeai package not installed. Chatbot disabled.")
        except Exception as e:
            print(f"WARNING: Gemini API key configuration failed: {e}. Chatbot disabled.")
    else:
        print("WARNING: GEMINI_API_KEY environment variable not set. The chatbot feature will not work.")

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .auth.routes import auth_bp
    from .scanner.routes import scanner_bp
    from .outbreaks.routes import outbreaks_bp
    from .tips.routes import tips_bp
    from .chatbot.routes import chatbot_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(scanner_bp)
    app.register_blueprint(outbreaks_bp)
    app.register_blueprint(tips_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app