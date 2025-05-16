#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv_backend" ]; then
    python3 -m venv .venv_backend
fi

# Activate virtual environment
source .venv_backend/bin/activate

# Install dependencies if needed
if [ ! -f ".venv_backend/installed" ]; then
    pip install -r requirements.txt
    pip freeze > requirements-lock.txt
    touch .venv_backend/installed
fi

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
