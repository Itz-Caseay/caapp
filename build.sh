#!/usr/bin/env bash
# Exit on error
set -o errexit

# Use Python 3.11 explicitly
export PYTHON_VERSION=3.11.8

echo "=== Starting build ==="
echo "Python version:"
python --version

# Ensure we're using Python 3.11
if [[ $(python -c "import sys; print(sys.version_info.major)") -ge 3 ]]; then
    echo "Python version is 3.x, continuing..."
else
    echo "Python version is not 3.x, please check setup."
    exit 1
fi

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running migrations ==="
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "=== Build complete ==="