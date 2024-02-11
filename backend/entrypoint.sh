#!/bin/bash

# Wait a bit for the mounted volume to be available
sleep 2

# Navigate to the Django project directory (if necessary)
cd /app/pyerudite

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
