# AIOSv3 Quick Start Guide

## 🚀 For New Developers

Welcome to AIOSv3! This guide helps you quickly navigate and understand the project.

## 📁 Project Structure

```
bluelabel-AIOSv3/
├── docs/                    # All documentation (START HERE)
│   ├── architecture/        # System design and decisions
│   ├── development/         # Development standards (READ CLAUDE.md)
│   ├── handoff/            # Onboarding guides
│   ├── project/            # Planning and roadmaps
│   ├── sprints/            # Sprint history
│   ├── status/             # Current status
│   └── theatrical/         # Demo system documentation
├── agents/                  # AI agent implementations
│   ├── base/               # Base agent framework
│   └── specialists/        # Specialized agents (Backend, Frontend, etc.)
├── core/                    # Core infrastructure
│   ├── routing/            # LLM routing system
│   ├── memory/             # Memory management
│   └── orchestration/      # Agent orchestration
├── control_center/          # Web UI for monitoring
├── theatrical_monitoring/   # Theatrical demo system
│   ├── theatrical_orchestrator.py      # Core orchestration
│   └── theatrical_monitoring_dashboard.py # TUI dashboard
└── launch_theatrical_demo.py # Main demo launcher (START HERE)
```

## 🎯 Essential Reading Order

1. **Start Here**: `docs/development/CLAUDE.md` - Project overview and conventions
2. **Current Status**: `docs/status/CURRENT_STATUS.md` - Where we are now
3. **Architecture**: `docs/architecture/REFINED_ARCHITECTURE.md` - System design
4. **Latest Sprint**: `docs/sprints/SPRINT_1_9_COMPLETE.md` - Recent work

## 💻 Quick Demo

```bash
# See the system in action (RECOMMENDED)
python3 launch_theatrical_demo.py

# Individual components
python3 -m theatrical_monitoring.theatrical_orchestrator        # Console mode
python3 -m theatrical_monitoring.theatrical_monitoring_dashboard # Dashboard mode
```

## 🔧 Key Technologies

- **Language**: Python 3.9+
- **Web Framework**: FastAPI
- **AI/LLM**: LangChain, Claude API, OpenAI API
- **Infrastructure**: Docker, Redis, RabbitMQ
- **UI**: Textual (TUI), Gradio (Web)
- **Testing**: pytest, mypy, ruff

## 🏗️ Architecture Highlights

- **Multi-Agent System**: Specialized AI agents collaborate on tasks
- **LLM Router**: Intelligent routing between cloud/local models
- **Theatrical Mode**: Visual orchestration for demos
- **ARCH-CTO Model**: Claude acts as technical lead for coding agents

## 📋 Development Workflow

1. **Read Documentation**: Start with docs before diving into code
2. **Run Demo**: Use `launch_theatrical_demo.py` to see system behavior
3. **Make Changes**: Follow conventions in `docs/development/DEVELOPMENT_STANDARDS.md`
4. **Test**: Run `pytest` before committing
5. **Document**: Update relevant docs when adding features

## 🎭 Understanding Theatrical Mode

The theatrical system provides visual orchestration:
- **Slowed execution** to see agent interactions
- **Color-coded events** for different agent roles
- **Real-time dashboard** showing agent activities
- **Performance metrics** for cost and token usage

## 🔑 Key Files to Explore

### Core Implementation
- `agents/base/enhanced_agent.py` - Base agent framework
- `core/routing/router.py` - LLM routing system
- `theatrical_monitoring/theatrical_orchestrator.py` - Main demo orchestrator
- `launch_theatrical_demo.py` - Interactive demo launcher

### Documentation
- `docs/handoff/HANDOFF_DOCUMENTATION.md` - Complete handoff guide
- `docs/project/PROJECT_PHASES.md` - Development roadmap
- `docs/theatrical/THEATRICAL_MONITORING_README.md` - Demo system guide

## 🚨 Common Commands

```bash
# Linting
ruff check .
mypy .

# Testing
pytest

# Run demos
python3 launch_theatrical_demo.py         # Interactive launcher
python3 test_real_llm_providers.py       # Test LLM routing
python3 control_center/main.py           # Web UI

# Git (use --no-verify due to pre-commit issues)
git commit --no-verify -m "your message"
```

## 💡 Tips for Success

1. **Start with the Demo**: Run `launch_theatrical_demo.py` first
2. **Read Error Messages**: They're designed to be helpful
3. **Check Logs**: Detailed logging throughout the system
4. **Ask Questions**: The codebase is well-documented
5. **Follow Patterns**: Consistency is key

## 🔗 Next Steps

1. Run the theatrical demo to see the system in action
2. Read through recent sprint documentation
3. Explore the specialist agents in `agents/specialists/`
4. Try modifying a simple agent behavior
5. Check `docs/project/BACKLOG.md` for areas to contribute

---

**Need Help?** Start with `docs/handoff/ARCH-CTO_ONBOARDING.md` for detailed context.