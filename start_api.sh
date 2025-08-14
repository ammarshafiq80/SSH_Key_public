#!/bin/bash

# SSH Key Management API - Quick Start Script
# This script helps you get the API up and running quickly

set -e

echo "🔑 SSH Key Management API - Quick Start"
echo "======================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if API files exist
if [ ! -f "api_server.py" ]; then
    echo "❌ api_server.py not found!"
    exit 1
fi

# Start the API server
echo "🚀 Starting SSH Key Management API..."
echo "   - Server will run on http://localhost:5000"
echo "   - Press Ctrl+C to stop the server"
echo "   - See README.md for usage examples"
echo ""

python3 api_server.py