#!/bin/bash
# Translation Test Framework Setup Script
# Creates Python virtual environment and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==================================="
echo "Translation Test Framework Setup"
echo "==================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Create virtual environment
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
fi

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate"
echo ""
echo "To run a test:"
echo "  python run_test.py <test-spec.md>"
echo ""
echo "Example:"
echo "  python run_test.py base-20251127.md"
echo ""
