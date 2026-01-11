# LivestockLink
LivestockLink SA is an open-source Python application designed to empower smallholder livestock farmers in rural South Africa. It provides tools for herd tracking, disease symptom scanning (using simple image analysis), outbreak alerts, and tele-vet connections. Built as an MVP for WeThinkCode_ students, this starts as a CLI tool with offline capabilities, expandable to a full mobile/web app via integrations like Flask for backend or Kivy for cross-platform UI.

This project addresses key challenges: 20% annual livestock losses from diseases like foot-and-mouth, stock theft, and limited vet access in areas like the Eastern Cape and Limpopo. Early pilots in similar African contexts show 30-50% loss reductions.

## Features

- **Herd Tracker**: Log and monitor animals offline with basic health metrics (e.g., weight, temperature via manual input or Bluetooth sim).
- **Symptom Scanner**: Analyze uploaded photos for common SA-specific issues (e.g., lumpy skin disease) using lightweight ML models.
- **Outbreak Alerts**: Pull and notify on public DAFF (Department of Agriculture, Forestry and Fisheries) feeds for local risks.
- **Tele-Vet Connect**: Simulate/SMS-based vet matching (expandable to Twilio integration).
- **Theft Shield**: Basic geo-fencing alerts via user-input GPS.
- **Multilingual Support**: English, isiZulu, isiXhosa prompts (via simple string translations).
- **Offline-First**: Uses SQLite for data persistence; syncs when online.

## Deployment & Database

Recommended deployment options:

- Docker Compose (recommended): builds the app and a Postgres DB. See `docker-compose.yml`.
- Platform (Heroku/GCP/Render): use `Procfile` and set `DATABASE_URL`.

Quick steps to initialize the database when you can't run `flask db`:

1. Install minimal deps locally (skip heavy ML deps if not needed right now):

```bash
python3 -m pip install --user --upgrade pip
python3 -m pip install --user flask==3.0.3 flask-sqlalchemy==3.0.2 flask-migrate==4.0.4 psycopg2-binary==2.9.6 python-dotenv==1.0.0
```

2. To create tables without Alembic migrations, run:

```bash
cd /path/to/project
python3 scripts/init_db.py
```

3. When you can install full requirements or use Docker, create real migrations:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial"
flask db upgrade
```

Notes:
- The app prefers `DATABASE_URL` or `SQLALCHEMY_DATABASE_URI` from environment and falls back to `resources/users.db` (SQLite).
- For production use Postgres (see `docker-compose.yml`).


Future expansions: Integrate with Hugging Face for advanced AI, Firebase for cloud sync, and Flutter for a native Android app.

