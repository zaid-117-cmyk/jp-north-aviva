#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "========================================================"
echo "  JP NORTH AVIVA - 3D ARCHITECTURAL WALKTHROUGH"
echo "  Starting local server at http://localhost:8080"
echo "========================================================"
echo ""

# Automatically open default browser after a brief moment
(sleep 1 && open "http://localhost:8080") &

# Start HTTP server on port 8080
if command -v python3 >/dev/null 2>&1; then
    python3 -m http.server 8080
elif command -v python >/dev/null 2>&1; then
    python -m http.server 8080
elif command -v npx >/dev/null 2>&1; then
    npx http-server -p 8080
else
    echo "[ERROR] Neither Python 3 nor Node.js found. Please install Python to run the server."
fi
