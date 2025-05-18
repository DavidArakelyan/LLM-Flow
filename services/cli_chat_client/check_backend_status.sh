#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Checking backend status..."

# Check if process is listening on port 8000
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend process is listening on port 8000"
    PROCESS_INFO=$(lsof -i :8000 | grep -v COMMAND)
    echo -e "  Process details: $PROCESS_INFO"
else
    echo -e "${RED}✗${NC} No process found listening on port 8000"
fi

# Try to connect to the backend
if nc -z localhost 8000 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Port 8000 is accepting connections"
else
    echo -e "${RED}✗${NC} Cannot connect to port 8000"
fi

# Test backend health endpoint
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Backend health check passed"
else
    echo -e "${RED}✗${NC} Backend health check failed (HTTP $RESPONSE)"
fi

# Check if backend can access required services
echo -e "\nChecking required services:"

# Check Vector DB
if nc -z localhost 6333 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Vector DB (port 6333) is accessible"
else
    echo -e "${YELLOW}!${NC} Vector DB is not accessible - backend may have limited functionality"
fi

# Check Web Search Tool
if nc -z localhost 7001 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Web Search Tool (port 7001) is accessible"
else
    echo -e "${YELLOW}!${NC} Web Search Tool is not accessible - backend may have limited functionality"
fi

# Check Docs Retriever Tool
if nc -z localhost 7002 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Docs Retriever Tool (port 7002) is accessible"
else
    echo -e "${YELLOW}!${NC} Docs Retriever Tool is not accessible - backend may have limited functionality"
fi

# Try a simple API request
echo -e "\nTesting backend API:"
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"id": "test-id", "content": "test", "message": "test"}' 2>/dev/null)
#    -d '{"message":"test"}' 2>/dev/null)

if [ ! -z "$CHAT_RESPONSE" ]; then
    echo -e "${GREEN}✓${NC} Backend API responded to test message"
    echo "  Response: $CHAT_RESPONSE"
else
    echo -e "${RED}✗${NC} Backend API did not respond to test message"
fi
