#!/bin/bash

# Transmission Client Setup Script
# This script sets up the Python environment and installs dependencies

echo "🚀 Setting up Transmission Client..."

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "❌ pyenv is not installed. Please install pyenv first."
    echo "   Visit: https://github.com/pyenv/pyenv#installation"
    exit 1
fi

# Check if the Python version is installed
if ! pyenv versions | grep -q "3.11.0"; then
    echo "📦 Installing Python 3.11.0..."
    pyenv install 3.11.0
fi

# Set the local Python version
echo "🔧 Setting Python version to 3.11.0..."
pyenv local 3.11.0

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created. Please edit it with your Transmission credentials."
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Transmission credentials"
echo "2. Test the connection: python test_connection.py"
echo "3. Use the client: python transmission_client.py --list"
echo ""
echo "To activate the virtual environment in the future:"
echo "   source .venv/bin/activate"
