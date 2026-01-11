FROM python:3.11-slim

# Set the working directory
WORKDIR /app

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

# Run the start script
CMD ["./start.sh"]