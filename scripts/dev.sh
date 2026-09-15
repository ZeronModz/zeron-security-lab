#!/bin/bash
# Zeron Security Lab - Development Server Script
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"

echo "=========================================="
echo "  Zeron Security Lab - Dev Server"
echo "=========================================="

# Check if venv exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo "[!] Virtual environment not found. Run scripts/setup_termux.sh first."
    exit 1
fi

# Activate venv
source "$BACKEND_DIR/venv/bin/activate"

cd "$BACKEND_DIR"

echo ""
echo "[*] Starting backend server..."
echo "[*] API: http://localhost:8000"
echo "[*] Docs: http://localhost:8000/docs"
echo "[*] Health: http://localhost:8000/api/v1/health"
echo "[*] Press Ctrl+C to stop"
echo ""

python run.py
