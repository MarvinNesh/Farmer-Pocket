FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.prod.txt ./
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . /app

EXPOSE 8000

# Run database migrations and start the application
CMD ["sh", "-c", "flask db upgrade && gunicorn -w 1 --threads 2 --timeout 60 -b 0.0.0.0:8000 run:app"]