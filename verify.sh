#!/bin/bash
# Quick deployment verification script for HackClub Nest

echo "🔍 Verifying Read It Now deployment..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Are you in the project directory?"
    exit 1
fi

# Check Python version
echo "🐍 Python version:"
python3 --version

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
python -m playwright install chromium

# Verify installations
echo "✅ Verifying installations..."
python -c "import flask; print(f'Flask: {flask.__version__}')" || echo "❌ Flask failed"
python -c "import playwright; print('Playwright: OK')" || echo "❌ Playwright failed"
python -c "import gunicorn; print('Gunicorn: OK')" || echo "❌ Gunicorn failed"
python -c "import bs4, langchain_core; print('AI libraries: OK')" || echo "❌ AI libraries failed"


# Test Flask app
echo "🧪 Testing Flask app..."
python -c "from app import app; print('✅ Flask app loads successfully')" || echo "❌ Flask app failed to load"

echo "🎉 Deployment verification complete!"
echo ""
echo "🚀 To start the application:"
echo "   source venv/bin/activate"
echo "   gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 120 app:app"
echo ""
echo "🌐 Your app will be available at: https://your-nest-id.nest.hackclub.com"
