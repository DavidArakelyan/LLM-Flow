# LLM Flow

A microservices-based application for handling LLM operations with document retrieval and web search capabilities.

## Services

- Backend: Main service orchestrating the flow of operations
- Docs Retriever Tool: Service for semantic document retrieval
- Web Search Tool: Service for web search operations
- CLI Chat Client: Command-line interface for interacting with the LLM Flow system

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key

## Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_api_key_here
SERPER_API_KEY=your_serper_key_here
```

## Setup and Running

1. Clone the repository:
```bash
git clone [repository-url]
cd llm-flow
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Start the services:
```bash
docker compose up --build
```

4. Run the CLI chat client (in a separate terminal):
```bash
cd services/cli_chat_client
./run_cli_chat_client.sh
```

Point your browser to <http://localhost:8000/docs> for backend OpenAPI docs.

## Repository layout
```text
llm-flow/
├─ docker-compose.yml
├─ services/
│  ├─ backend/ …               # FastAPI + LangGraph orchestrator
│  ├─ web_search_tool/ …       # FastMCP micro‑service
│  ├─ docs_retriever_tool/ …   # FastMCP micro‑service
│  └─ cli_chat_client/ …       # Command-line chat interface
├─ docs/
│  └─ architecture.mmd         # mermaid diagram
└─ .vscode/
   └─ launch.json
```

Full design rationale and extension guidance lives in **docs/architecture.mmd**.

The services will be available at:
- Backend: http://localhost:8000
- Docs Retriever: http://localhost:7002
- Web Search: http://localhost:7003
- Vector DB: http://localhost:6333
- Frontend: http://localhost:3000

## Development

Each service is a separate Python application with its own requirements.txt and Dockerfile, except for the frontend which is a React/TypeScript application using Vite.

To run the frontend in development mode:
```bash
cd services/frontend
npm install
npm run dev
```

## Running Services & Debugging

### Service Launch Scripts

Two convenience scripts are provided for running the services:

- `run_all_services_docker.sh`: Launches all services including the backend in Docker containers
- `run_mcp_services_docker.sh`: Launches only the MCP (Micro-service Communication Protocol) services, useful for backend development

#### Default Behaviors

- Without any options, both scripts will:
  - Use existing Docker images (no rebuild)
  - Run in attached mode (showing logs)
  - Preserve existing containers and volumes
  - Use default timeouts (30s for health checks)

#### run_all_services_docker.sh

This script provides a complete deployment of all services in Docker containers:

```bash
./run_all_services_docker.sh [-b] [-d] [-h]
```

Options:
- `-b`: Build images before starting containers
- `-d`: Run in detached mode
- `-h`: Show help message

Default behavior:
```bash
# Equivalent to:
docker compose up
```

#### run_mcp_services_docker.sh

This script launches only the supporting microservices, ideal for backend development:

```bash
./run_mcp_services_docker.sh [-b] [-d] [-h] [-c cleanup]
```

Options:
- `-b`: Build images before starting containers
- `-d`: Run in detached mode
- `-c`: Clean up existing containers and volumes
- `-h`: Show help message

Default behavior:
```bash
# Equivalent to:
docker compose up web_search_tool docs_retriever_tool qdrant
```

#### Service Health Checks

The `check_backend_status.sh` script verifies service health:
```bash
./check_backend_status.sh [-t timeout] [-v]
```

Options:
- `-t`: Set custom timeout in seconds (default: 30)
- `-v`: Verbose output

Default behavior:
- Checks all required services
- Uses 30-second timeout
- Shows only errors and success messages
- Returns exit code 0 if all checks pass, 1 if any fail

### Debugging the Backend Flow

For backend development, use the second script:

```bash
./run_mcp_services_docker.sh
```

This will start:
- Web Search service
- Docs Retriever service
- Vector DB

### CLI Chat Client

The CLI Chat Client (`services/cli_chat_client`) provides a terminal-based interface for testing and interacting with the LLM Flow system. To use it:

1. Set up the backend development environment:
```bash
cd services/cli_chat_client
source setup_env.sh  # Activated bachend's virtual environment providing correct context for debugging.
```

2. Start the backend in debug mode using VS Code:
   - Open the desired backend file(s) and set your breakpoint(s)
   - Open VS Code command palette (Cmd+Shift+P)
   - Select "Debug: Start Debugging" or press F5
   - Choose the "Python: FastAPI" configuration

3. Verify backend status:
```bash
./check_backend_status.sh
```

4. Launch the CLI client:
```bash
./run_cli_chat_client.sh
```

The CLI client provides a REPL-like interface for sending messages to the LLM Flow system. Type your messages and press Enter to send. Use Ctrl+C to exit.

### Debugging Tips

- The `setup_env.sh` script creates a Python virtual environment specific to the backend service and installs all required dependencies. This ensures proper dependency isolation for debugging.
- When running the backend through VS Code's debugger, you can set breakpoints in the code and inspect variables during execution.
- The `check_backend_status.sh` script verifies that the backend API is responsive before attempting to connect with the CLI client.

## License

MIT

