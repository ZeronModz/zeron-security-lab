#!/bin/bash
# Zeron Security Lab - Termux Setup Script
set -e

echo "=========================================="
echo "  Zeron Security Lab - Setup Script"
echo "=========================================="

# Check if in Termux
if [ -d /data/data/com.termux ]; then
    echo "[*] Running in Termux"
else
    echo "[!] Not running in Termux"
fi

# Check required tools
echo ""
echo "[*] Checking required tools..."

check_tool() {
    if command -v "$1" &> /dev/null; then
        echo "  [OK] $1"
    else
        echo "  [MISSING] $1"
    fi
}

check_tool python3
check_tool pip
check_tool node
check_tool npm
check_tool git
check_tool java
check_tool gradle

# Setup backend
echo ""
echo "[*] Setting up backend..."

cd "$(dirname "$0")/../backend"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "  Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov httpx

# Create .env from example
if [ ! -f ".env" ]; then
    echo "  Creating .env from .env.example..."
    cp .env.example .env
    echo "  [!] Edit .env with your settings"
fi

echo ""
echo "[*] Setup complete!"
echo ""
echo "To start the backend:"
echo "  cd backend && source venv/bin/activate && python run.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""
