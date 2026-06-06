#!/bin/bash

source venv/bin/activate

# Auto-run database migrations on startup
echo "Running database migrations..."
alembic upgrade head
echo "Migrations complete."

uvicorn app.main:app --reload
