#!/bin/bash

# Animal Classification App Launch Script
# This script sets up and launches the Streamlit application

set -e  # Exit on any error

echo "🐾 Animal Classification App - Launch Script"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "animal_classifier.py" ]; then
    echo "❌ Error: animal_classifier.py not found in current directory"
    echo "Please run this script from the src/ directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📚 Installing requirements..."
    pip install -r requirements.txt
else
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# Test the setup (optional)
if [ "$1" = "--test" ] || [ "$1" = "-t" ]; then
    echo "🧪 Running setup tests..."
    python test_setup.py
    if [ $? -ne 0 ]; then
        echo "❌ Setup tests failed. Please check the errors above."
        exit 1
    fi
    echo "✅ Setup tests passed!"
fi

# Get network settings
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-"8501"}

echo "🚀 Starting Streamlit application..."
echo "📍 Access the app at:"
echo "   Local:   http://localhost:$PORT"
echo "   Network: http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Launch Streamlit
streamlit run animal_classifier.py --server.port $PORT --server.address $HOST