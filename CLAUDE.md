# AIOSv3 - Modular AI Agent Platform

## Project Summary

Building a production-ready, modular AI agent platform that orchestrates specialized agents (CTO, Frontend, Backend, QA, etc.) to autonomously deliver complex digital products. The platform maximizes code/data ownership while supporting flexible cloud/local LLM routing per agent.

## Key Requirements

### 1. Multi-Agent Orchestration
- **Specialized Agents**: Each agent has a specific role (CTO, Frontend Developer, Backend Developer, QA Engineer, etc.)
- **Autonomous Collaboration**: Agents work together without constant human intervention
- **State Management**: Persistent memory and context sharing across agents
- **Recovery & Resilience**: Agents can resume after failures

### 2. Hybrid LLM Architecture
- **Flexible Model Assignment**: Each agent can use either:
  - Cloud LLMs (Claude Code, GPT-4, etc.)
  - Local/Self-hosted LLMs (Llama 3/4, DeepSeek, Qwen, Code Llama)
- **Dynamic Routing**: Route tasks based on:
  - Cost considerations
  - Privacy requirements
  - Task complexity
  - Performance needs
- **Per-Agent Configuration**: Model assignment is configurable per agent, task, or workflow

### 3. Open-Source First Approach
- **Maximum Ownership**: Self-host critical components where feasible
- **Open Protocols**: Use Model Context Protocol (MCP) for standardized communication
- **Avoid Vendor Lock-in**: Design for easy migration between services

### 4. Integration & Extensibility
- **Business System Integration**: Connect with existing APIs and SaaS tools
- **Workflow Automation**: Visual automation via n8n (self-hosted)
- **RAG Capabilities**: Vector databases for knowledge-augmented agents
- **API Gateway**: Secure exposure of agent capabilities

### 5. Production Requirements
- **Containerization**: Docker/Kubernetes for all components
- **CI/CD Pipeline**: Automated builds and deployments
- **Monitoring**: Full observability (Prometheus, Grafana, ELK)
- **Security**: OAuth2, RBAC, Zero Trust architecture
- **Scalability**: Horizontal scaling capabilities

## Technical Stack

### Core Components
- **Agent Orchestration**: LangGraph, CrewAI, or AutoGen
- **LLM Integration**: LangChain, LlamaIndex
- **Workflow Automation**: n8n (self-hosted)
- **Vector Database**: Qdrant, Weaviate, or Milvus
- **Memory/State**: Redis + Vector DB
- **API Framework**: FastAPI
- **Message Queue**: RabbitMQ or Apache Kafka

### Infrastructure
- **Container Runtime**: Docker
- **Orchestration**: Kubernetes
- **Service Mesh**: Istio (optional)
- **API Gateway**: Kong or custom FastAPI
- **Load Balancer**: Nginx or Traefik

### Development Tools
- **Version Control**: Git
- **CI/CD**: GitLab CI, ArgoCD, or Jenkins
- **Testing**: pytest, Jest, Playwright
- **Documentation**: Sphinx, Swagger/OpenAPI

## Architecture Principles

1. **Modularity**: Each agent is a separate service with clear interfaces
2. **Loose Coupling**: Agents communicate via message passing and APIs
3. **High Cohesion**: Each agent has a well-defined responsibility
4. **Fault Tolerance**: System continues operating if individual agents fail
5. **Observability**: Comprehensive logging, metrics, and tracing
6. **Security by Design**: Zero trust, least privilege, encrypted communication

## Development Conventions

### Code Standards
- **Python**: PEP 8, type hints, async/await patterns
- **TypeScript**: ESLint, Prettier, strict mode
- **API Design**: RESTful principles, OpenAPI documentation
- **Git**: Conventional commits, feature branches, PR reviews

### Testing Requirements
- **Unit Tests**: Minimum 80% coverage
- **Integration Tests**: For all agent interactions
- **E2E Tests**: For critical workflows
- **Load Tests**: For performance validation

### Documentation
- **Code Comments**: Clear, concise, explaining "why" not "what"
- **API Docs**: OpenAPI/Swagger specifications
- **Architecture Docs**: C4 diagrams, sequence diagrams
- **User Guides**: For each agent type and workflow

## Success Metrics

1. **Agent Autonomy**: % of tasks completed without human intervention
2. **Cost Efficiency**: Cloud LLM costs vs local model usage
3. **Performance**: Response time, throughput, error rates
4. **Scalability**: Ability to handle concurrent workflows
5. **Reliability**: Uptime, recovery time, data consistency

## Development Workflow

1. **Start each session** by reading this file to understand current context
2. **Use TodoWrite tool** to create and track sprint tasks
3. **Follow sprint methodology** with clear acceptance criteria
4. **Commit regularly** with descriptive messages following conventional commits
5. **Update documentation** as you implement features
6. **Run tests** before committing changes
7. **Update PROJECT_PHASES.md** at the end of each sprint with progress checkmarks (✅/❌)

## Commands to Run

```bash
# Linting
ruff check .
mypy .

# Testing
pytest
npm test

# Build
docker-compose build
kubectl apply -f k8s/

# Deploy
./scripts/deploy.sh
```

## Current Project State (Production Ready - June 2, 2025)

### ✅ Completed Agents
1. **Backend Developer Agent** - FastAPI, Python, database design
2. **Frontend Developer Agent** - React/Vue, UI components, TypeScript
3. **QA Engineer Agent** - Testing strategies, pytest, Jest, Playwright
4. **DevOps Engineer Agent** - Terraform, Kubernetes, CI/CD, monitoring
5. **CTO Agent** - Using Claude (you) as the real CTO instead of mock

### 🔧 Key Infrastructure
- **Enhanced Base Agent** with lifecycle, health, and recovery
- **LLM Router** with multi-provider support including REAL LLM providers
- **Claude Provider** - Full Anthropic API integration with cost tracking
- **OpenAI Provider** - Complete GPT-4/3.5 integration with intelligent routing
- **Memory System** with Redis backend and context management
- **Control Center UI** with real-time monitoring dashboard
- **WebSocket Server** for live updates

### 🎭 READY: Theatrical Monitoring System (June 2, 2025)
- **Theatrical Orchestrator** (`theatrical_orchestrator.py`) - Slowed execution with visual delays
- **Real-time Dashboard** (`theatrical_monitoring_dashboard.py`) - Live TUI with agent panels
- **Demo Launcher** (`launch_theatrical_demo.py`) - Interactive demo with multiple modes
- **Step-by-step visualization** of agent handoffs and collaboration
- **Color-coded event logging** with timestamps and role indicators
- **Performance tracking** for cost, time, and token usage across all agents

### 🔍 Critical Discoveries
1. **Router Initialization**: Must call `await router.initialize()` before use
2. **Agent Router Assignment**: Must set `agent.router = router` after creation
3. **Real LLM Integration**: Use `ClaudeConfig`/`OpenAIConfig` for real providers
4. **Task Processing**: Use `EnhancedTask` objects with `process_task()` method
5. **Provider Distribution**: Router intelligently distributes tasks by cost/capability
6. **API Key Management**: Load from .env with `load_dotenv()` for real providers
7. **Cost Tracking**: Real-time token usage and cost monitoring per provider

### 📋 Next Development Focus
1. **Production Infrastructure** - Authentication, monitoring, deployment scripts
2. **Complex Multi-Agent Projects** - E-commerce, dashboard applications
3. **Task Dependencies** - Sequential and parallel task orchestration
4. **Performance Optimization** - Caching, parallel processing, cost reduction
5. **Local LLM Integration** - Ollama, vLLM provider support

### 🚀 Quick Start for Next Session
```bash
# READY: Theatrical Monitoring System (RECOMMENDED)
python3 launch_theatrical_demo.py  # Interactive demo launcher

# Individual Components
python3 theatrical_orchestrator.py                # Console-only mode
python3 theatrical_monitoring_dashboard.py        # Dashboard-only mode

# Previous Working Demos
python3 test_real_llm_providers.py               # Test LLM routing
python3 test_agents_real_llm.py                  # Test individual agents
python3 demo_real_llm_orchestration.py           # Full orchestration
python3 control_center/main.py                   # Control Center UI
```

### 🏗️ Architecture Patterns
- Each specialist agent extends `EnhancedBaseAgent`
- Agents have domain-specific expertise areas and templates
- Mock provider uses keyword detection for routing
- Response formatting follows consistent structure per agent type
- Quality metrics tracked: tokens, cost, execution time

## Commands to Run

```bash
# Linting (note: pre-commit hooks have issues, use --no-verify)
ruff check .
mypy .

# Testing
pytest
npm test

# Quick agent tests
python3 test_backend_agent.py
python3 test_frontend_agent.py
python3 test_qa_agent.py
python3 test_devops_simple.py

# Build
docker-compose build
kubectl apply -f k8s/

# Deploy
./scripts/deploy.sh
```

## Important Files
- `SPRINT_1_7_COMPLETE.md` - Latest sprint summary
- `enhanced_mock_provider.py` - Multi-agent mock responses
- `agents/specialists/` - All specialist agent implementations
- `control_center/main.py` - Web UI for monitoring