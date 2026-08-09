#!/bin/bash

set -e

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
alembic upgrade head
echo "Migrations complete."

echo "Starting production server..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000