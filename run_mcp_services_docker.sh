#!/bin/bash

# Default command is 'up' if no argument is provided
command=${1:-up}

# List of microservices needed by backend
SERVICES="vector_db web_search_tool docs_retriever_tool"

case "$command" in
    "up")
        echo "Starting backend microservices..."
        docker compose up -d $SERVICES
        ;;
    "down")
        echo "Stopping and removing backend microservices..."
        docker compose down $SERVICES
        ;;
    "stop")
        echo "Stopping backend microservices (containers preserved)..."
        docker compose stop $SERVICES
        ;;
    "ps")
        echo "Checking backend microservices status..."
        docker compose ps $SERVICES
        ;;
    *)
        echo "Usage: $0 [up|down|stop|ps]"
        echo "  up   - Start backend microservices (default)"
        echo "  down - Stop and remove backend microservices"
        echo "  stop - Stop backend microservices (preserves containers)"
        echo "  ps   - Show microservices status"
        exit 1
        ;;
esac
