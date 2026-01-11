#!/bin/sh

# It can take a few seconds for the database to be ready
echo "Waiting for database..."
retries=5
while [ $retries -gt 0 ]; do
    echo "Running database migrations (retries left: $retries)..."
    # The if statement checks the exit code of the command
    if flask db upgrade; then
        echo "Migrations successful!"
        break
    fi
    retries=$((retries - 1))
    echo "Migration failed, sleeping for 5 seconds..."
    sleep 5
done

if [ $retries -eq 0 ]; then
    echo "Could not apply migrations after several attempts. Exiting."
    exit 1
fi

echo "Starting Gunicorn..."
# Use exec to replace the shell process with Gunicorn
exec gunicorn --worker-class gevent --bind 0.0.0.0:8000 run:app