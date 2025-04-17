#!/bin/bash

# Wait a bit for the mounted volume to be available
sleep 2

mkdir -p /artefacts/logs/backend/cron/

# Remove lockfiles from earlier runs
rm /artefacts/tmp/ingest.lock
rm /artefacts/tmp/summarize.lock

# Navigate to the Django project directory (if necessary)
cd /app/pyerudite

# Install dependencies
pip install -r /app/requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# reset potential in_progress jobs
python manage.py reset_in_progress_ingest
python manage.py reset_in_progress_summarize

# Start the cron service
service cron start

# Start the Django development server
python manage.py runserver 0.0.0.0:4242
