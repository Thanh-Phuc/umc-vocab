#!/bin/bash

# UMC Vocabulary Search Portal - Startup Script

echo "🔍 Starting UMC Vocabulary Search Portal..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 setup.py
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if data directory has files
if [ ! "$(ls -A data 2>/dev/null)" ]; then
    echo "⚠️  Warning: Data directory is empty!"
    echo "Please add your vocabulary files to the 'data/' directory"
    echo "See data/README.md for required files"
fi

# Start the application
echo "🚀 Launching application..."
streamlit run app.py

# Deactivate virtual environment on exit
deactivate
