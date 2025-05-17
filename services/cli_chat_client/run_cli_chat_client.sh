#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv_chat" ]; then
    python3 -m venv .venv_chat
fi

# Activate virtual environment
source .venv_chat/bin/activate

# Install dependencies if needed
if [ ! -f ".venv_chat/installed" ]; then
    pip install -r requirements.txt
    pip freeze > requirements-lock.txt
    touch .venv_chat/installed
fi

# Run the chat client
python chat.py