#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv_web_search" ]; then
    python3 -m venv .venv_web_search
fi

# Activate virtual environment
source .venv_web_search/bin/activate

# Install dependencies if needed
if [ ! -f ".venv_web_search/installed" ]; then
    pip install -r requirements.txt
    pip freeze > requirements-lock.txt
    touch .venv_web_search/installed
fi

# Run the service
python server.py