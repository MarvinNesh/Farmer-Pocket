import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import create_app
from src.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    print('Database initialized at', app.config.get('SQLALCHEMY_DATABASE_URI'))