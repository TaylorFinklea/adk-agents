# ADK Fun - Google Agent Development Kit Learning Project

A comprehensive learning project for Google's Agent Development Kit (ADK) featuring multiple agent implementations with observability, tracing, and deployment capabilities.

## 🚀 Features

- **Multi-Tool Agent**: Weather and time information agent for Kansas City
- **Google Search Agent**: AI-powered search agent with real-time web search capabilities
- **Dual Deployment Options**: Cloud Run (with full observability) or Agent Engine (native tracing)
- **Comprehensive Observability**: LangWatch, Langfuse, and Opik integration
- **OpenTelemetry**: Full tracing and monitoring setup
- **Evaluation Framework**: Built-in agent evaluation capabilities

## 📁 Project Structure

```
adk/
├── .env                          # Environment variables (use .env.example as template)
├── .env.example                  # Template for environment setup
├── config.yaml                   # OpenTelemetry collector configuration
├── docker-compose.yml            # OTEL collector deployment
├── pyproject.toml               # Python project configuration
├── google-search-agent/         # Google Search AI agent
│   ├── agent.py                 # Main agent implementation
│   ├── interact.py              # Interactive testing script
│   └── .env.example             # Agent-specific environment template
└── multi-tool-agent/           # Multi-tool demonstration agent
    ├── agent.py                 # Weather/time agent implementation
    └── .env.example             # Agent-specific environment template
```

## 🛠️ Prerequisites

- Python 3.11+ (< 3.12)
- Google Cloud Project with Vertex AI enabled
- API keys for observability platforms (optional but recommended)

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd adk
```

### 2. Install Dependencies

```bash
pip install -e .
```

### 3. Environment Configuration

Copy the example environment files and configure your API keys:

```bash
# Main configuration
cp .env.example .env

# Agent-specific configurations
cp google-search-agent/.env.example google-search-agent/.env
cp multi-tool-agent/.env.example multi-tool-agent/.env
```

Edit each `.env` file with your actual API keys:

#### Required API Keys:
- **Google API Key**: For Gemini models and search functionality
- **LangWatch API Key**: For conversation monitoring (optional)
- **Langfuse Keys**: For detailed tracing and analytics (optional)

### 4. Quick Test

Test the multi-tool agent locally:

```bash
adk run multi-tool-agent
```

## 🤖 Agents

### Multi-Tool Agent

A demonstration agent providing weather and time information for Kansas City.

**Capabilities:**
- Weather reports
- Current time lookup
- Kansas City specific data

**Usage:**
```bash
# Local testing
adk run multi-tool-agent

# Web interface
adk web multi-tool-agent
```

### Google Search Agent

An intelligent search agent powered by Google's search capabilities.

**Capabilities:**
- Real-time web search
- Intelligent result synthesis
- Fact-based responses
- Source attribution

**Usage:**
```bash
# Local testing
adk run google-search-agent

# Web interface  
adk web google-search-agent
```

## 🚀 Deployment Options

### Option 1: Cloud Run (Recommended)

Full observability with Opik integration:

```bash
cd google-search-agent
python agent.py deploy-cloudrun
```

**Features:**
- Auto-scaling
- Full Opik observability
- Production-ready
- HTTPS endpoints

### Option 2: Agent Engine

Native Google Cloud integration:

```bash
cd google-search-agent
python agent.py deploy-agent-engine
```

**Features:**
- Native Vertex AI integration
- Built-in tracing
- Google Cloud monitoring
- Serverless execution

## 📊 Observability & Monitoring

### OpenTelemetry Setup

Start the OTEL collector for comprehensive tracing:

```bash
docker-compose up -d
```

This enables:
- **LangWatch**: Real-time conversation monitoring
- **Langfuse**: Detailed trace analytics and cost tracking
- **Distributed Tracing**: End-to-end request tracking

### Monitoring Dashboards

- **LangWatch**: [https://app.langwatch.ai](https://app.langwatch.ai)
- **Langfuse**: [https://us.cloud.langfuse.com](https://us.cloud.langfuse.com)
- **Google Cloud Traces**: [Google Cloud Console](https://console.cloud.google.com/traces/list)

### Interactive Testing

For deployed Agent Engine agents:

```bash
cd google-search-agent
python interact.py
```

Features:
- Interactive chat interface
- Debug mode for event inspection
- Session management
- Batch testing capabilities

## 🧪 Evaluation

Run agent evaluations:

```bash
# Run evaluation on multi-tool agent
adk eval multi-tool-agent

# View evaluation history
ls multi-tool-agent/.adk/eval_history/
```

## 🔧 Configuration

### Deployment Modes

Set `DEPLOYMENT_MODE` in your `.env` files:

- `cloudrun`: Full Opik observability (default)
- `agent_engine`: Native tracing only

### Google Cloud Configuration

Update these values in `agent.py` files:
```python
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"  
STAGING_BUCKET = "gs://your-bucket-name"
```

## 📚 Development Guide

### Creating New Agents

1. Create new directory under `adk/`
2. Implement `agent.py` with your agent logic
3. Copy `.env.example` for environment variables
4. Add agent-specific dependencies to `pyproject.toml`

### Agent Structure

```python
from google.adk.agents import Agent

def your_tool_function(param: str) -> dict:
    """Your tool implementation"""
    return {"result": "success"}

root_agent = Agent(
    name="your_agent_name",
    model="gemini-2.5-flash-preview-05-20",
    description="Agent description",
    instruction="System instructions",
    tools=[your_tool_function]
)
```

### Adding Observability

For Cloud Run deployments with full observability:

```python
from opik.integrations.adk import OpikTracer

opik_tracer = OpikTracer()
root_agent = Agent(
    # ... your agent config
    before_agent_callback=opik_tracer.before_agent_callback,
    after_agent_callback=opik_tracer.after_agent_callback,
    # ... other callbacks
)
```

## 🔐 Security

- **Never commit real API keys** - Use `.env.example` templates
- **Environment variables only** - All sensitive data in `.env` files
- **`.gitignore` protection** - Prevents accidental credential commits

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -e .
```

**Authentication errors:**
- Verify API keys in `.env` files
- Check Google Cloud authentication: `gcloud auth list`

**Deployment failures:**
- Ensure Google Cloud project has Vertex AI enabled
- Verify bucket permissions and project ID

### Debug Mode

Enable debug logging in interactive sessions:
```
You: debug
Debug mode: ON
```

### Logs and Traces

- Local logs: `agent_conversations.log`
- Cloud traces: Google Cloud Console → Traces
- OTEL collector logs: `docker-compose logs otel-collector`

## 📖 Resources

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit)
- [LangWatch Documentation](https://docs.langwatch.ai)
- [Langfuse Documentation](https://langfuse.com/docs)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Vertex AI team for the ADK framework
- OpenTelemetry community for observability standards
- LangWatch and Langfuse teams for monitoring solutions

---

**Happy agent building! 🤖✨**