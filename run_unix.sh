#!/bin/bash
# Memory Context Overlay - macOS/Linux Launcher
# Run this script to start the application

echo "================================================"
echo "Memory Context Overlay"
echo "================================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ using your package manager"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo
    echo "WARNING: OPENAI_API_KEY environment variable not set!"
    echo
    echo "Please set your OpenAI API key before running:"
    echo '  export OPENAI_API_KEY="your-api-key-here"'
    echo
    echo "Or add it to your ~/.bashrc or ~/.zshrc file."
    echo
    read -p "Continue anyway? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        exit 0
    fi
fi

# Change to script directory
cd "$(dirname "$0")"

# Run the application
python3 run.py
