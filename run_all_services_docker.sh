#!/bin/bash

# Default command is 'up' if no argument is provided
command=${1:-up}
detached=${2:-""}

# Options for 'up' command:
# --build: Forces rebuilding of service images before starting containers
# -d: Runs containers in detached mode (background)
#     - Without -d: Runs in foreground, showing real-time logs
#     - With -d: Runs in background, no logs, terminal remains available
case "$command" in
    "up")
        if [ "$detached" = "-d" ]; then
            # Start containers in background (detached mode)
            docker compose up --build -d
        else
            # Start containers in foreground with live logs
            docker compose up --build
        fi
        ;;
    "down")
        docker compose down
        ;;
    "stop")
        docker compose stop
        ;;
    "restart")
        docker compose restart
        ;;
    "ps")
        docker compose ps
        ;;
    *)
        echo "Usage: $0 [up|down|stop|restart|ps] [-d]"
        echo "  up      - Start and build the containers (default)"
        echo "           Use '-d' as second argument to run in detached mode"
        echo "  down    - Stop and remove the containers"
        echo "  stop    - Stop the containers"
        echo "  restart - Restart the containers"
        echo "  ps      - Show container status"
        exit 1
        ;;
esac
