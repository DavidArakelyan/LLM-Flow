#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv_docs_retriever" ]; then
    python3 -m venv .venv_docs_retriever
fi

# Activate virtual environment
source .venv_docs_retriever/bin/activate

# Install dependencies if needed
if [ ! -f ".venv_docs_retriever/installed" ]; then
    pip install -r requirements.txt
    pip freeze > requirements-lock.txt
    touch .venv_docs_retriever/installed
fi

# Run the service
export VECTOR_DB_URL=${VECTOR_DB_URL:-"http://localhost:6333"}
python server.py