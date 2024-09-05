#!/bin/bash

# Wait for the database to be ready

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting the server..."
exec python -m manage.py runserver 8000
