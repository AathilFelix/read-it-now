#!/bin/bash
# Post-deployment script for HackClub Nest
PORT=${1:-8000}

lsof -ti:$PORT | xargs kill -9 2>/dev/null || true

git pull origin main

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Installing Playwright browsers..."
python -m playwright install chromium

echo "✅ Deployment setup complete!"

# Start the application with gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app