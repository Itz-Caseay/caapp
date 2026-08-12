#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=== Starting build ==="
echo "Python version:"
python --version

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running migrations ==="
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "=== Build complete ==="