import os
from src import create_app
from src.extensions import db
from src.models import User

app = create_app()

USERNAME = os.environ.get('ADMIN_USER', 'admin')
EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

with app.app_context():
    if User.query.filter_by(username=USERNAME).first():
        print('Admin user already exists')
    else:
        user = User(username=USERNAME, email=EMAIL)
        user.set_password(PASSWORD)
        db.session.add(user)
        db.session.commit()
        print('Created admin user:', USERNAME)
