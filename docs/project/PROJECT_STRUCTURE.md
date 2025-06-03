# AIOSv3 Project Structure

**Clean Production-Ready Architecture** (Post-Sprint 1.8 Reorganization)

## Overview

This document describes the clean, production-ready structure of AIOSv3 following the comprehensive codebase reorganization completed in Sprint 1.8. All experimental and legacy files have been moved to the `ARCHIVE/` directory for preservation while maintaining a professional, navigable codebase.

## Production Directory Structure

```
AIOSv3/
├── 📁 agents/                      # Core Agent Framework
│   ├── base/                       # Enhanced base agent system
│   │   ├── enhanced_agent.py       # 🔧 Current production base
│   │   ├── types.py                # Agent type definitions
│   │   ├── lifecycle.py            # Agent lifecycle management
│   │   ├── health.py               # Health monitoring
│   │   ├── recovery.py             # Error recovery
│   │   └── exceptions.py           # Agent exceptions
│   └── specialists/                # Specialist Agent Implementations
│       ├── backend_agent.py        # ✅ Backend Developer Agent
│       ├── frontend_agent.py       # ✅ Frontend Developer Agent
│       ├── qa_agent.py             # ✅ QA Engineer Agent
│       ├── devops_agent.py         # ✅ DevOps Engineer Agent
│       └── cto_agent.py            # ✅ CTO Agent
│
├── 📁 core/                        # Core Infrastructure
│   ├── routing/                    # LLM Routing & Providers
│   │   ├── router.py               # 🎯 Intelligent LLM routing
│   │   ├── llm_client.py           # LLM client interface
│   │   └── providers/              # LLM Provider Implementations
│   │       ├── base.py             # Provider base interface
│   │       ├── claude.py           # 🔵 Anthropic Claude integration
│   │       ├── openai.py           # 🟢 OpenAI GPT integration
│   │       ├── local.py            # Local LLM integration
│   │       └── mock_provider.py    # Mock provider for testing
│   ├── memory/                     # Memory Management
│   │   ├── base.py                 # Memory base classes
│   │   ├── context_manager.py      # Context management
│   │   ├── memory_manager.py       # Memory operations
│   │   └── backends/               # Memory backends
│   │       └── redis_backend.py    # Redis memory backend
│   ├── intelligence/               # Intelligence Layer
│   │   └── error_recovery.py       # Error recovery system
│   ├── monitoring/                 # Metrics & Monitoring
│   │   └── metrics.py              # Metrics collection
│   ├── messaging/                  # Inter-Agent Communication
│   │   ├── agent_router.py         # Agent message routing
│   │   ├── error_handling.py       # Message error handling
│   │   ├── queue.py                # Message queuing
│   │   └── routing.py              # Message routing logic
│   ├── orchestration/              # Agent Discovery & Registry
│   │   ├── discovery.py            # Agent discovery
│   │   └── registry.py             # Agent registry
│   ├── storage/                    # Storage Systems
│   │   ├── object_store.py         # Object storage
│   │   └── versioning.py           # Version management
│   └── workspace/                  # Workspace Management
│       └── manager.py              # Workspace operations
│
├── 📁 control_center/              # Production Control Center UI
│   ├── main.py                     # 🖥️ Control Center application
│   ├── simple_app.py               # Compatibility layer
│   ├── run_control_center.py       # Control Center launcher
│   └── components/                 # UI Components
│       ├── agent_orchestra.py      # Agent orchestration UI
│       ├── activity_monitor.py     # Activity monitoring
│       ├── task_manager.py         # Task management UI
│       └── pr_review.py            # PR review interface
│
├── 📁 monitoring_system/           # Production Monitoring Server
│   ├── server.py                   # 📊 Monitoring server
│   ├── run_monitoring.py           # Monitoring launcher
│   ├── metrics_collector.py        # Metrics collection
│   └── src/                        # Monitoring components
│       ├── monitoring_server.py    # Core monitoring server
│       └── activity_store.py       # Activity storage
│
├── 📁 api/                         # REST API Interface
│   ├── main.py                     # 🌐 FastAPI application
│   └── routes/                     # API routes
│
├── 📁 config/                      # Configuration Files
│   ├── agents.yaml                 # 🔧 Agent configurations
│   ├── llm_config.py              # LLM configuration
│   ├── models.yaml                 # Model definitions
│   └── routing.yaml                # Routing configuration
│
├── 📁 infrastructure/              # Deployment Infrastructure
│   ├── docker/                     # Docker configurations
│   ├── grafana/                    # Grafana dashboards
│   └── prometheus/                 # Prometheus configuration
│
├── 📁 scripts/                     # Production Scripts
│   ├── dev-setup.sh               # Development setup
│   ├── install_python.sh          # Python installation
│   └── start.sh                    # System startup
│
├── 📁 tests/                       # Organized Test Suite
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   ├── e2e/                        # End-to-end tests
│   └── conftest.py                 # Test configuration
│
├── 📁 docs/                        # Documentation
│   └── sprints/                    # Sprint documentation
│
├── 📁 research/                    # Research & Planning
│   └── aiosv3_blueprint.md         # System blueprint
│
├── 📁 ARCHIVE/                     # 🗄️ Archived Experimental Code
│   ├── legacy_agents/              # Old agent implementations
│   ├── dev_tests/                  # Development test files
│   ├── prototypes/                 # Early prototypes
│   ├── collaboration_experiments/  # Collaboration experiments
│   ├── legacy_scripts/             # Old launch scripts
│   └── old_orchestration/          # Previous orchestration systems
│
├── 🚀 enhanced_mock_provider.py    # Current Working Mock Provider
├── 🎬 demo_orchestration.py        # Current Agent Demo
├── 🎬 demo_real_llm_orchestration.py # Real LLM Multi-Agent Demo
├── 🎬 demo_multi_agent_todo.py     # Multi-Agent Todo Demo
├── 🧪 test_real_llm_providers.py   # Real LLM Provider Tests
├── 🧪 test_agents_real_llm.py      # Agent Real LLM Tests
├── 🚀 start_system.sh              # Production System Launcher
└── 📋 pyproject.toml               # Package Configuration
```

## Core Component Status

### ✅ Production Ready Components

| Component | Status | Description |
|-----------|--------|-------------|
| **Specialist Agents** | 🟢 PRODUCTION | All 5 agents working with real LLMs |
| **LLM Router** | 🟢 PRODUCTION | Intelligent routing with Claude/OpenAI |
| **Control Center** | 🟢 PRODUCTION | Full monitoring UI (Sprint 1.6) |
| **Monitoring System** | 🟢 PRODUCTION | WebSocket server with metrics |
| **Memory System** | 🟢 PRODUCTION | Redis backend with context management |
| **Real LLM Integration** | 🟢 PRODUCTION | Claude + OpenAI providers (Sprint 1.8) |

### 🔧 Development Components

| Component | Status | Description |
|-----------|--------|-------------|
| **API Interface** | 🟡 BASIC | FastAPI structure exists |
| **Authentication** | 🔴 TODO | Planned for Sprint 1.9 |
| **Local LLM Support** | 🟡 PARTIAL | Ollama integration planned |
| **Task Dependencies** | 🔴 TODO | Inter-agent dependencies |

## Key Entry Points

### Production Operations
- **🚀 System Startup**: `start_system.sh`
- **🖥️ Control Center**: `python3 control_center/main.py`
- **📊 Monitoring**: `python3 monitoring_system/run_monitoring.py`

### Development & Testing
- **🧪 LLM Provider Tests**: `python3 test_real_llm_providers.py`
- **🧪 Agent Integration Tests**: `python3 test_agents_real_llm.py`
- **🎬 Multi-Agent Demo**: `python3 demo_real_llm_orchestration.py`

### Configuration
- **🔧 Agent Config**: `config/agents.yaml`
- **🔧 LLM Config**: `config/llm_config.py`
- **🔧 Environment**: `.env` (API keys, settings)

## Archive Organization

The `ARCHIVE/` directory preserves all experimental and development work:

- **legacy_agents/**: Original agent implementations and theatrical experiments
- **dev_tests/**: Development test files and experiments
- **prototypes/**: Early UI prototypes and proof-of-concepts
- **collaboration_experiments/**: Various collaboration approaches tested
- **legacy_scripts/**: Sprint-specific and experimental launch scripts
- **old_orchestration/**: Previous orchestration system implementations

## Navigation Guidelines

### For Production Development
1. **Agent Work**: Focus on `agents/specialists/` and `agents/base/`
2. **Infrastructure**: Work in `core/` subdirectories
3. **UI Development**: Use `control_center/` and `monitoring_system/`
4. **Testing**: Use organized `tests/` structure

### For Research & Learning
1. **Current Capabilities**: Run demos in root directory
2. **Historical Context**: Explore `ARCHIVE/` directories
3. **Documentation**: Check `docs/` and sprint completion files

## Benefits of This Structure

1. **🎯 Professional**: Clean, production-ready organization
2. **📍 Navigable**: Easy to find current implementations
3. **🏛️ Preserved**: All experimental work archived for reference
4. **🔧 Scalable**: Room for future components without clutter
5. **🧪 Testable**: Clear test organization matching code structure
6. **📚 Documented**: Comprehensive documentation and examples

## Next Steps

Following this reorganization, the codebase is now ready for:
- **Sprint 1.9**: Production infrastructure development
- **Customer Pilots**: Professional codebase presentation
- **Team Onboarding**: Clear structure for new developers
- **Scaling**: Additional agents and capabilities

---

**Last Updated**: Sprint 1.8 (January 6, 2025)  
**Status**: 🟢 Production Ready Structure  
**Next Sprint**: Production Infrastructure & Complex Projects