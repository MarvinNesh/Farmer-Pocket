FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.prod.txt requirements.prod.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy the rest of the application code
COPY . .

# Make the start script executable
RUN chmod +x ./start.sh

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=run.py

# Healthcheck to give the app time to start
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run the start script
CMD ./start.sh