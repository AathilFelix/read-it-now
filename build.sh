#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "🚀 Starting Render deployment build..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright and browsers
echo "🎭 Installing Playwright browsers..."
python -m playwright install --with-deps chromium

# Verify installations
echo "✅ Verifying installations..."
python -c "import flask; print(f'Flask: {flask.__version__}')"
python -c "import playwright; print('Playwright: OK')"
python -c "import gunicorn; print('Gunicorn: OK')"

echo "✅ Build completed successfully!"
