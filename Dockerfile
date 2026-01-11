FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . /app

EXPOSE 8000

# Define environment variable
ENV FLASK_APP=run.py

# Run the application
CMD flask db upgrade && gunicorn --worker-class gevent --bind 0.0.0.0:8000 run:app