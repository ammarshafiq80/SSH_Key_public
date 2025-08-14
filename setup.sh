#!/bin/bash

# GitHub Models GPT API Setup Script

set -e

echo "🚀 GitHub Models GPT API Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
    echo "⚠️  Please edit .env file and add your GitHub token!"
else
    echo "✅ .env file already exists"
fi

# Make example scripts executable
echo "🔧 Making example scripts executable..."
chmod +x examples/*.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GitHub token"
echo "2. Get your GitHub token from: https://github.com/settings/tokens"
echo "3. Start the API with: python app.py"
echo "4. Test with: python examples/test_api.py"
echo ""
echo "API will be available at: http://localhost:5000"