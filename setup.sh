#!/bin/bash
# Post-deployment script for HackClub Nest
set -e  # Exit on any error

PORT=${1:-8000}
echo "🚀 Starting deployment on port $PORT..."

# Kill any existing process on the port
echo "🔄 Killing existing processes on port $PORT..."
lsof -ti:$PORT | xargs kill -9 2>/dev/null || true

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Remove old virtual environment if it exists
echo "🧹 Cleaning up old environment..."
rm -rf venv

# Create and activate virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip first
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers (chromium only for lighter deployment)
echo "🎭 Installing Playwright browsers..."
python -m playwright install chromium

# Verify critical installations
echo "✅ Verifying installations..."
python -c "import flask; print(f'Flask: {flask.__version__}')"
python -c "import playwright; print('Playwright: OK')"
python -c "import gunicorn; print('Gunicorn: OK')"
python -c "import bs4, langchain_core; print('AI libraries: OK')"

echo "✅ Deployment setup complete!"
echo "🌐 Starting application on port $PORT..."

# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app