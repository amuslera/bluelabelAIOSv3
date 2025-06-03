# AIOSv3 Repository Structure Guide

## Overview

This document provides a comprehensive overview of the AIOSv3 repository structure after the v1.0.0 reorganization. The repository follows a clean, professional layout optimized for maintainability and ease of navigation.

## Root Directory

The root directory contains only essential files:

```
/
├── README.md                    # Project overview and getting started
├── launch_theatrical_demo.py    # Main entry point for theatrical monitoring
├── start_system.sh             # System startup script
├── pyproject.toml              # Python project configuration
├── docker-compose.*.yml        # Docker configurations
├── Dockerfile.dev              # Development container
└── .gitignore, .env.example    # Configuration files
```

## Core Project Structure

### `/agents/`
Specialized AI agent implementations
- `base/` - Base agent classes and lifecycle management
- `specialists/` - Role-specific agents (CTO, Backend, Frontend, QA, DevOps)

### `/api/`
REST API implementation
- `main.py` - FastAPI application
- `routes/` - API endpoints

### `/config/`
Configuration files
- `agents.yaml` - Agent configurations
- `llm_config.py` - LLM provider settings
- `models.yaml` - Model definitions
- `routing.yaml` - Routing rules

### `/control_center/`
Web-based monitoring UI
- `main.py` - Control center application
- `components/` - UI components
- `styles.css` - Styling

### `/core/`
Core framework components
- `intelligence/` - AI and error recovery
- `memory/` - State management and persistence
- `messaging/` - Inter-agent communication
- `monitoring/` - Metrics and observability
- `orchestration/` - Agent coordination
- `routing/` - LLM provider routing
- `storage/` - Data persistence
- `workspace/` - Workspace management

### `/theatrical_monitoring/`
Theatrical monitoring system (v1.0.0 feature)
- `theatrical_monitoring_dashboard.py` - Main TUI dashboard
- `theatrical_orchestrator.py` - Orchestration engine
- `dashboards/` - Alternative dashboard versions
- `THEATRICAL_MONITORING_TECHNICAL_GUIDE.md` - Technical documentation

## Documentation Structure (`/docs/`)

### `/docs/architecture/`
System design and architecture decisions
- `ARCHITECTURE_DECISIONS.md`
- `CONTROL_CENTER_UI.md`
- `REFINED_ARCHITECTURE.md`

### `/docs/demos/`
Demo setup and walkthrough guides
- `DEMO_MULTI_TERMINAL.md`
- `DEMO_TASK_ORCHESTRATION.md`
- `MULTI_TERMINAL_SETUP.md`
- `REAL_COLLABORATION_SETUP.md`

### `/docs/development/`
Development guides and standards
- `CLAUDE.md` - Claude-specific instructions
- `DEVELOPMENT.md` - Development setup
- `DEVELOPMENT_STANDARDS.md` - Coding standards
- `INSTRUCTIONS.md` - General instructions
- `LLM_ROUTING_CONFIG.md` - LLM configuration

### `/docs/handoff/`
Onboarding and handoff documentation
- `ARCH-CTO_ONBOARDING.md` - CTO onboarding guide
- `HANDOFF_DOCUMENTATION.md` - Complete handoff guide
- `HANDOFF_NOTES_JAN_6_2025.md` - Historical notes

### `/docs/project/`
Project planning and management
- `BACKLOG.md` - Feature backlog
- `COMMERCIAL_VISION.md` - Business vision
- `PROJECT_PHASES.md` - Development phases
- `PROJECT_STATUS.md` - Current status
- `ROADMAP_2025.md` - 2025 roadmap
- And more...

### `/docs/sprints/`
Sprint documentation (23 files)
- Sprint plans, retrospectives, and completion reports
- From Sprint 1.1 through Sprint 1.9

### `/docs/status/`
Status reports and tracking
- `CURRENT_STATUS.md` - Latest project status
- `RELEASE_NOTES_v1.0.0.md` - v1.0.0 release notes
- `PHASE_1_LEARNINGS.md` - Phase 1 insights
- Various status checkpoints

### `/docs/theatrical/`
Theatrical monitoring documentation
- `THEATRICAL_AGENTS_DESIGN.md`
- `THEATRICAL_MONITORING_README.md`
- `THEATRICAL_REALITY_OVERVIEW.md`

### Key Documentation Files
- `/docs/README.md` - Documentation index
- `/docs/QUICK_START_GUIDE.md` - New developer guide
- `/docs/REORGANIZATION_SUMMARY.md` - Reorganization details

## Supporting Directories

### `/ARCHIVE/`
Historical and experimental code
- `collaboration_experiments/`
- `dev_tests/`
- `legacy_agents/`
- `legacy_scripts/`
- `old_orchestration/`
- `prototypes/`

### `/data/`
Runtime data storage
- `artifacts/` - Generated artifacts
- `workspaces/` - Agent workspaces

### `/exports/`
Export directory for logs and reports
- CSV performance reports
- JSON conversation logs
- `logs/` - Log files

### `/infrastructure/`
Infrastructure as code
- `docker/` - Docker configurations
- `grafana/` - Monitoring dashboards
- `prometheus/` - Metrics configuration

### `/research/`
Research and design documents
- `aiosv3_blueprint.md`

### `/scripts/`
Utility scripts
- `dev-setup.sh` - Development environment setup
- `install_python.sh` - Python installation
- `start.sh` - Startup scripts

### `/tests/`
Test suites
- `unit/` - Unit tests
- `integration/` - Integration tests
- `e2e/` - End-to-end tests
- `fixtures/` - Test fixtures
- `conftest.py` - Test configuration

## Quick Navigation

For new developers:
1. Start with `/docs/QUICK_START_GUIDE.md`
2. Read `/README.md` for project overview
3. Check `/docs/development/CLAUDE.md` for AI-specific instructions
4. Run `python3 launch_theatrical_demo.py` for interactive demo

For specific needs:
- **Architecture**: `/docs/architecture/`
- **Current Status**: `/docs/status/CURRENT_STATUS.md`
- **Sprint History**: `/docs/sprints/`
- **Theatrical Monitoring**: `/theatrical_monitoring/` and `/docs/theatrical/`

## Version Control

- Main branch: `main`
- Current version: `v1.0.0`
- Tagged releases in git

This structure ensures a clean, professional repository that scales well and makes it easy for new contributors to understand and navigate the project.