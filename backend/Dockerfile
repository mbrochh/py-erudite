# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ wget gunicorn cron vim logrotate

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY crontab.txt /app/
RUN crontab /app/crontab.txt

RUN python -m spacy download en_core_web_sm

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Command to run the application
CMD /app/entrypoint.sh
# CMD tail -f /dev/null
# CMD ./manage.py runserver 0.0.0.0:8000
