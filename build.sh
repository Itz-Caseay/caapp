#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input