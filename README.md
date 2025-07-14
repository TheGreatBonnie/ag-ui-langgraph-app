# CopilotKit + AG-UI + LangGraph Research Agent

A powerful AI-driven research application that combines **CopilotKit**, **AG-UI Protocol**, and **LangGraph** to create an intelligent research assistant. This application enables users to conduct comprehensive research through a conversational interface, automatically gathering information from the web and generating detailed reports.

## 🚀 Features

- **AI-Powered Research**: Leverage LangGraph agents to conduct autonomous web research
- **Interactive Chat Interface**: Built with CopilotKit for seamless human-AI collaboration
- **AG-UI Protocol Integration**: Standardized communication between frontend and agent backend
- **Real-time Progress Tracking**: Monitor research phases and progress in real-time
- **Report Generation**: Automatically generate comprehensive reports from research findings
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Streaming Responses**: Real-time updates using Server-Sent Events via AG-UI protocol

## 🏗️ Architecture

This project demonstrates the integration of three powerful technologies:

- **CopilotKit**: Provides the React framework for building AI-powered chat interfaces
- **AG-UI Protocol**: Enables standardized communication between the frontend and AI agents via Server-Sent Events
- **LangGraph**: Powers the intelligent research agent with state management and workflow orchestration

The application consists of two main components:

### Frontend (Next.js + CopilotKit)

- **Framework**: Next.js 15 with React 19
- **UI Library**: CopilotKit React components
- **Styling**: Tailwind CSS
- **Features**: Chat interface, report canvas, progress tracking

### Backend (Python + AG-UI + LangGraph)

- **Framework**: FastAPI for API server
- **Protocol**: AG-UI protocol for standardized agent communication
- **Agent Framework**: LangGraph for research workflows
- **Search**: Google Search integration via SerpAPI
- **LLM**: OpenAI GPT models for analysis and report generation

## 📋 Prerequisites

- Node.js 18+
- Python 3.10-3.13
- Poetry (for Python dependency management)
- OpenAI API key
- SerpAPI key (for web search)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/TheGreatBonnie/ag-ui-langgraph-app.git
cd ag-ui-langgraph-app
```

### 2. Set up the Frontend (Next.js)

```bash
# Install dependencies
npm install

# Copy and configure environment variables
cp .env.example .env.local
```

### 3. Set up the Backend (Python Agent)

```bash
cd ag-ui-langgraph-agent

# Install dependencies with Poetry
poetry install

# Copy and configure environment variables
cp .env.example .env
```

### 4. Configure Environment Variables

#### Frontend (.env.local)

```env
# Add any frontend-specific environment variables
```

#### Backend (.env)

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

## 🚀 Getting Started

### 1. Start the Backend Agent Server

```bash
cd ag-ui-langgraph-agent
poetry run server
```

The agent server will start on `http://localhost:8000`

### 2. Start the Frontend Development Server

```bash
# In the root directory
npm run dev
```

The web application will be available at `http://localhost:3000`

### 3. Access the Application

- **Home Page**: `http://localhost:3000` - Welcome page
- **Research Interface**: `http://localhost:3000/copilotkit` - Main research application

## 💡 Usage

1. Navigate to the CopilotKit interface at `/copilotkit`
2. Start a conversation with the research agent
3. Ask questions or request research on any topic
4. Watch as the agent:
   - Searches the web for relevant information
   - Analyzes and processes the findings
   - Generates a comprehensive report
5. View the generated report in the canvas area
6. Continue the conversation to refine or expand the research

## 🔧 Development

### Project Structure

```
├── src/                          # Next.js frontend
│   ├── app/                     # App router pages
│   │   ├── copilotkit/         # Main research interface
│   │   └── api/                # API routes
│   ├── components/             # React components
│   └── lib/                    # Utilities and types
├── ag-ui-langgraph-agent/      # Python backend
│   └── src/agui/              # Agent implementation
│       ├── langgraph/         # LangGraph agent logic
│       └── main.py           # FastAPI server
└── public/                     # Static assets
```

### Key Technologies

- **CopilotKit**: AI copilot framework for React
- **AG-UI Protocol**: Standardized protocol for agent-UI communication
- **LangGraph**: State machine framework for building LLM agents
- **Next.js**: React framework for web applications
- **FastAPI**: Modern Python web framework
- **OpenAI**: Large language models
- **SerpAPI**: Web search capabilities

## 🧪 Scripts

### Frontend

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Backend

- `poetry run server` - Start the agent server
- `poetry install` - Install dependencies
- `poetry shell` - Activate virtual environment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Review the documentation for [CopilotKit](https://docs.copilotkit.ai) and [LangGraph](https://langchain-ai.github.io/langgraph/)
3. Create a new issue with detailed information about your problem

## 🙏 Acknowledgments

- **CopilotKit** team for the amazing AI copilot framework
- **LangChain** team for LangGraph and related tools
- **Vercel** team for Next.js
- **FastAPI** team for the excellent Python web framework
