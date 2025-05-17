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

## License

MIT

