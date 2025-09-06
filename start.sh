#!/usr/bin/env bash
# Start script for Render deployment

echo "🚀 Starting Read It Now on Render..."

# Set environment variables for Render
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/.playwright
export PYTHONUNBUFFERED=1

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --worker-class sync app:app
