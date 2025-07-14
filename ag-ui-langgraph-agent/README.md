# AG-UI LangGraph Research Agent

A FastAPI-based research agent built with LangGraph that provides intelligent web research capabilities through the AG-UI protocol. This agent can perform web searches, analyze content, and generate comprehensive research reports.

## Features

- **Intelligent Research**: Automated web searching and content analysis
- **LangGraph Workflow**: State-managed research process with clear execution flow
- **AG-UI Protocol**: Standardized communication interface with real-time streaming
- **FastAPI Backend**: High-performance asynchronous web API
- **Real-time Updates**: Server-sent events for live progress tracking

## Architecture

The project is organized into modular components:

```
src/agui/
├── main.py              # FastAPI application and AG-UI endpoint
├── langgraph/
│   ├── agent.py         # LangGraph workflow builder
│   ├── state.py         # Research state management
│   ├── research.py      # Core research logic
│   ├── report.py        # Report generation
│   └── web_search.py    # Web search functionality
```

## Prerequisites

- Python 3.10 or higher (up to 3.13)
- Poetry for dependency management
- OpenAI API key
- SerpAPI key (for web search)

## Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:TheGreatBonnie/ag-ui-langgraph-agent.git
   cd ag-ui-langgraph-agent
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_key_here
   ```

## Usage

### Running the Server

1. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

2. **Start the FastAPI server:**

   ```bash
   poetry run uvicorn src.agui.main:app
   ```

3. **The API will be available at:**
   - Main endpoint: `http://localhost:8000/`
   - Interactive docs: `http://localhost:8000/docs`
   - OpenAPI spec: `http://localhost:8000/openapi.json`

### API Usage

Send a POST request to the root endpoint with a research query:

```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_thread_123",
    "run_id": "test_run_456",
    "messages": [
      {
        "id": "msg_1",
        "role": "user",
        "content": "Research lifespan of Penguins"
      }
    ],
    "tools": [],
    "context": [],
    "forwarded_props": {},
    "state": {}
  }'
```

The API returns a stream of events following the AG-UI protocol, providing real-time updates on the research process.

### Response Format

The agent responds with Server-Sent Events (SSE) containing:

- **RunStartedEvent**: Research process initialization
- **TextMessageStartEvent**: Beginning of response generation
- **TextMessageContentEvent**: Streaming content chunks
- **TextMessageEndEvent**: Completion of response
- **RunFinishedEvent**: Final research results

## Development

### Project Structure

- **main.py**: FastAPI application with AG-UI protocol integration
- **agent.py**: LangGraph workflow definition and compilation
- **research.py**: Core research logic and orchestration
- **state.py**: State management for tracking research progress
- **web_search.py**: Web search functionality using SerpAPI
- **report.py**: Report generation and formatting

### Dependencies

Key dependencies include:

- **FastAPI**: Modern web framework for building APIs
- **LangGraph**: Workflow orchestration for language model applications
- **OpenAI**: Language model integration
- **SerpAPI**: Web search capabilities
- **AG-UI Protocol**: Standardized communication interface
- **Poetry**: Dependency management and packaging

### Testing

Run tests using pytest:

```bash
poetry run pytest
```

### Code Style

The project follows Python best practices:

- Type hints for better code documentation
- Modular architecture for maintainability
- Comprehensive error handling
- Detailed logging and progress tracking

## Environment Variables

Required environment variables:

| Variable          | Description                              | Required |
| ----------------- | ---------------------------------------- | -------- |
| `OPENAI_API_KEY`  | OpenAI API key for language model access | Yes      |
| `SERPAPI_API_KEY` | SerpAPI key for web search functionality | Yes      |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the GitHub repository
- Check the documentation at `/docs` endpoint when running the server
- Review the AG-UI protocol documentation for integration details

---

**Author**: TheGreatBonnie (mwendabkaberia@gmail.com)
**Version**: 0.1.0
