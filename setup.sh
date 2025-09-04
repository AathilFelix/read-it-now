set -e

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

pip install -r requirements.txt

# Install Playwright browsers (chromium only for lighter deployment)
echo "🎭 Installing Playwright browsers..."
python -m playwright install


# Start the application with gunicorn
gunicorn --bind 0.0.0.0:$PORT app:app