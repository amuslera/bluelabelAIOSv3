#!/usr/bin/env python3
"""
Multi-Agent Orchestration Demo with Real LLM Providers.

Demonstrates complete multi-agent collaboration using real Claude and OpenAI APIs
to build a Todo application with specification, backend, frontend, testing, and deployment.
"""

import asyncio
import logging
import os
import time
from datetime import datetime
from dotenv import load_dotenv

from core.routing.providers import ClaudeProvider, ClaudeConfig, OpenAIProvider, OpenAIConfig
from core.routing.router import LLMRouter, RoutingPolicy, RoutingStrategy
from agents.specialists.backend_agent import BackendDeveloperAgent, BackendAgentConfig
from agents.specialists.frontend_agent import FrontendDeveloperAgent, FrontendAgentConfig
from agents.specialists.qa_agent import QAEngineerAgent, QAAgentConfig
from agents.specialists.devops_agent import DevOpsEngineerAgent, DevOpsAgentConfig
from agents.base.enhanced_agent import EnhancedTask
from agents.base.types import TaskType, Priority

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RealLLMOrchestrationDemo:
    """Orchestrate multi-agent collaboration using real LLM providers."""

    def __init__(self):
        self.router = None
        self.agents = {}
        self.artifacts = {}
        self.metrics = {
            "start_time": None,
            "total_tokens": 0,
            "total_cost": 0.0,
            "phase_times": {},
            "provider_usage": {},
        }

    async def setup_infrastructure(self) -> None:
        """Set up LLM router and agents with real providers."""
        logger.info("🚀 Setting up Real LLM Infrastructure...")
        
        # Initialize router with cost-optimized strategy
        self.router = LLMRouter(
            default_policy=RoutingPolicy(
                strategy=RoutingStrategy.COST_OPTIMIZED,
                max_cost_per_request=0.50,  # Allow higher cost for complex tasks
            )
        )

        # Setup Claude provider
        claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        if claude_api_key:
            claude_config = ClaudeConfig(
                provider_name="claude",
                api_key=claude_api_key,
                timeout=60.0,  # Longer timeout for complex tasks
            )
            claude_provider = ClaudeProvider(claude_config)
            await claude_provider.initialize()
            self.router.register_provider("claude", claude_provider)
            logger.info("✅ Claude provider registered")

        # Setup OpenAI provider
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai_config = OpenAIConfig(
                provider_name="openai",
                api_key=openai_api_key,
                timeout=60.0,  # Longer timeout for complex tasks
            )
            openai_provider = OpenAIProvider(openai_config)
            await openai_provider.initialize()
            self.router.register_provider("openai", openai_provider)
            logger.info("✅ OpenAI provider registered")

        # Initialize router
        await self.router.initialize()

        # Setup agents
        await self._setup_agents()
        
        logger.info("🎯 Real LLM Infrastructure Ready!")

    async def _setup_agents(self) -> None:
        """Setup all specialist agents."""
        
        # Backend Developer Agent
        backend_config = BackendAgentConfig()
        self.agents["backend"] = BackendDeveloperAgent(backend_config)
        self.agents["backend"].router = self.router
        await self.agents["backend"].initialize()

        # Frontend Developer Agent
        frontend_config = FrontendAgentConfig()
        self.agents["frontend"] = FrontendDeveloperAgent(frontend_config)
        self.agents["frontend"].router = self.router
        await self.agents["frontend"].initialize()

        # QA Engineer Agent
        qa_config = QAAgentConfig()
        self.agents["qa"] = QAEngineerAgent(qa_config)
        self.agents["qa"].router = self.router
        await self.agents["qa"].initialize()

        # DevOps Engineer Agent
        devops_config = DevOpsAgentConfig()
        self.agents["devops"] = DevOpsEngineerAgent(devops_config)
        self.agents["devops"].router = self.router
        await self.agents["devops"].initialize()

        logger.info(f"✅ {len(self.agents)} specialist agents initialized")

    async def orchestrate_todo_app(self) -> None:
        """Orchestrate building a complete Todo application."""
        logger.info("\\n🎬 Starting Multi-Agent Todo App Orchestration with Real LLMs!")
        self.metrics["start_time"] = time.time()

        # Phase 1: CTO Specification (Claude as CTO)
        await self._phase1_specification()
        
        # Phase 2: Backend Development
        await self._phase2_backend_development()
        
        # Phase 3: Frontend Development
        await self._phase3_frontend_development()
        
        # Phase 4: QA Testing
        await self._phase4_qa_testing()
        
        # Phase 5: DevOps Deployment
        await self._phase5_devops_deployment()

        # Print final summary
        await self._print_orchestration_summary()

    async def _phase1_specification(self) -> None:
        """Phase 1: Create technical specification."""
        logger.info("\\n📋 Phase 1: CTO Technical Specification")
        phase_start = time.time()

        # CTO provides the specification (this is me as Claude)
        specification = {
            "project": "Todo API with React Frontend",
            "architecture": {
                "backend": {
                    "framework": "FastAPI",
                    "database": "SQLite (for demo)",
                    "features": ["CRUD operations", "User auth", "Validation"],
                    "endpoints": [
                        "POST /api/todos - Create todo",
                        "GET /api/todos - List todos",
                        "PUT /api/todos/{id} - Update todo",
                        "DELETE /api/todos/{id} - Delete todo"
                    ]
                },
                "frontend": {
                    "framework": "React with TypeScript",
                    "features": ["Todo list", "Add/edit/delete", "Filter/search", "Responsive design"],
                    "state": "React hooks (useState, useEffect)"
                },
                "deployment": {
                    "containerization": "Docker",
                    "orchestration": "Kubernetes",
                    "ci_cd": "GitHub Actions"
                }
            },
            "requirements": {
                "performance": "< 200ms API response",
                "testing": "80% code coverage",
                "security": "Input validation, CORS",
                "accessibility": "WCAG 2.1 AA compliance"
            }
        }

        self.artifacts["specification"] = specification
        self.metrics["phase_times"]["specification"] = time.time() - phase_start
        
        logger.info(f"✅ Phase 1 Complete: Technical specification created")
        logger.info(f"   Time: {self.metrics['phase_times']['specification']:.2f}s")

    async def _phase2_backend_development(self) -> None:
        """Phase 2: Backend development with FastAPI."""
        logger.info("\\n🔧 Phase 2: Backend Development")
        phase_start = time.time()

        task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt=f"""Create a complete FastAPI backend for a Todo application based on this specification:

{self.artifacts['specification']}

Requirements:
- FastAPI with SQLAlchemy ORM
- SQLite database for demo
- Pydantic models for validation
- CRUD operations for todos
- Basic error handling
- CORS middleware
- Health check endpoint

Include:
1. Complete main.py with all endpoints
2. Database models and schemas
3. Example usage and setup instructions

Be comprehensive but production-ready.""",
            complexity=8,
            priority=Priority.HIGH,
        )

        result = await self.agents["backend"].process_task(task)
        
        self.artifacts["backend_code"] = result.output
        self._update_metrics(result)
        self.metrics["phase_times"]["backend"] = time.time() - phase_start

        logger.info(f"✅ Phase 2 Complete: Backend implementation ready")
        logger.info(f"   Time: {self.metrics['phase_times']['backend']:.2f}s")
        logger.info(f"   Tokens: {result.tokens_used}, Cost: ${result.cost:.4f}")
        logger.info(f"   Provider: {result.provider_used}/{result.model_used}")

    async def _phase3_frontend_development(self) -> None:
        """Phase 3: Frontend development with React."""
        logger.info("\\n🎨 Phase 3: Frontend Development")
        phase_start = time.time()

        task = EnhancedTask(
            task_type=TaskType.CODE_GENERATION,
            prompt=f"""Create a complete React TypeScript frontend for the Todo application.

Backend API specification:
{self.artifacts['specification']['architecture']['backend']}

Requirements:
- React with TypeScript
- Modern hooks (useState, useEffect, useCallback)
- Responsive design with CSS modules or styled-components
- API integration with fetch/axios
- Loading states and error handling
- Form validation
- Clean, professional UI

Include:
1. Main App component
2. TodoList component
3. TodoItem component
4. AddTodo form component
5. CSS/styling
6. API service layer

Make it production-ready with proper TypeScript types and error boundaries.""",
            complexity=8,
            priority=Priority.HIGH,
        )

        result = await self.agents["frontend"].process_task(task)
        
        self.artifacts["frontend_code"] = result.output
        self._update_metrics(result)
        self.metrics["phase_times"]["frontend"] = time.time() - phase_start

        logger.info(f"✅ Phase 3 Complete: Frontend implementation ready")
        logger.info(f"   Time: {self.metrics['phase_times']['frontend']:.2f}s")
        logger.info(f"   Tokens: {result.tokens_used}, Cost: ${result.cost:.4f}")
        logger.info(f"   Provider: {result.provider_used}/{result.model_used}")

    async def _phase4_qa_testing(self) -> None:
        """Phase 4: QA testing and validation."""
        logger.info("\\n🧪 Phase 4: QA Testing")
        phase_start = time.time()

        task = EnhancedTask(
            task_type=TaskType.TESTING,
            prompt=f"""Create comprehensive tests for the Todo application.

Application Components:
- Backend: FastAPI with SQLAlchemy
- Frontend: React with TypeScript
- Features: CRUD operations, validation, error handling

Create:
1. Backend tests (pytest):
   - Unit tests for API endpoints
   - Integration tests for database operations
   - Validation tests for input/output
   - Error handling tests

2. Frontend tests (Jest + React Testing Library):
   - Component unit tests
   - Integration tests for user interactions
   - API mocking tests
   - Accessibility tests

3. E2E tests (Playwright):
   - Complete user workflows
   - Cross-browser compatibility

Include test setup, fixtures, and coverage configuration. Target 80% coverage.""",
            complexity=7,
            priority=Priority.HIGH,
        )

        result = await self.agents["qa"].process_task(task)
        
        self.artifacts["test_suite"] = result.output
        self._update_metrics(result)
        self.metrics["phase_times"]["testing"] = time.time() - phase_start

        logger.info(f"✅ Phase 4 Complete: Test suite ready")
        logger.info(f"   Time: {self.metrics['phase_times']['testing']:.2f}s")
        logger.info(f"   Tokens: {result.tokens_used}, Cost: ${result.cost:.4f}")
        logger.info(f"   Provider: {result.provider_used}/{result.model_used}")

    async def _phase5_devops_deployment(self) -> None:
        """Phase 5: DevOps deployment configuration."""
        logger.info("\\n🚀 Phase 5: DevOps Deployment")
        phase_start = time.time()

        task = EnhancedTask(
            task_type=TaskType.DEPLOYMENT,
            prompt=f"""Create complete deployment configuration for the Todo application.

Application Stack:
- Backend: FastAPI (Python)
- Frontend: React (Node.js build)
- Database: SQLite (can be replaced with PostgreSQL)

Create:
1. Dockerfiles:
   - Multi-stage backend Dockerfile
   - Optimized frontend Dockerfile
   - Docker Compose for local development

2. Kubernetes manifests:
   - Deployment configurations
   - Service definitions
   - ConfigMaps and Secrets
   - Ingress rules
   - HPA (Horizontal Pod Autoscaler)

3. CI/CD Pipeline (GitHub Actions):
   - Build and test workflow
   - Security scanning
   - Multi-environment deployment
   - Rollback capabilities

4. Monitoring setup:
   - Health checks
   - Prometheus metrics
   - Logging configuration

Include production-ready security best practices and scalability considerations.""",
            complexity=9,
            priority=Priority.HIGH,
        )

        result = await self.agents["devops"].process_task(task)
        
        self.artifacts["deployment_config"] = result.output
        self._update_metrics(result)
        self.metrics["phase_times"]["deployment"] = time.time() - phase_start

        logger.info(f"✅ Phase 5 Complete: Deployment configuration ready")
        logger.info(f"   Time: {self.metrics['phase_times']['deployment']:.2f}s")
        logger.info(f"   Tokens: {result.tokens_used}, Cost: ${result.cost:.4f}")
        logger.info(f"   Provider: {result.provider_used}/{result.model_used}")

    def _update_metrics(self, result) -> None:
        """Update orchestration metrics."""
        self.metrics["total_tokens"] += result.tokens_used
        self.metrics["total_cost"] += result.cost
        
        provider = result.provider_used
        if provider in self.metrics["provider_usage"]:
            self.metrics["provider_usage"][provider]["requests"] += 1
            self.metrics["provider_usage"][provider]["tokens"] += result.tokens_used
            self.metrics["provider_usage"][provider]["cost"] += result.cost
        else:
            self.metrics["provider_usage"][provider] = {
                "requests": 1,
                "tokens": result.tokens_used,
                "cost": result.cost,
            }

    async def _print_orchestration_summary(self) -> None:
        """Print comprehensive orchestration summary."""
        total_time = time.time() - self.metrics["start_time"]
        
        logger.info("\\n" + "="*70)
        logger.info("🎉 MULTI-AGENT ORCHESTRATION COMPLETE!")
        logger.info("="*70)
        
        # Overall metrics
        logger.info(f"⏱️  Total Time: {total_time:.2f} seconds")
        logger.info(f"🪙 Total Tokens: {self.metrics['total_tokens']:,}")
        logger.info(f"💰 Total Cost: ${self.metrics['total_cost']:.4f}")
        
        # Phase breakdown
        logger.info("\\n📊 Phase Breakdown:")
        for phase, phase_time in self.metrics["phase_times"].items():
            percentage = (phase_time / total_time) * 100
            logger.info(f"   {phase.title()}: {phase_time:.2f}s ({percentage:.1f}%)")
        
        # Provider usage
        logger.info("\\n🔧 Provider Usage:")
        for provider, usage in self.metrics["provider_usage"].items():
            logger.info(f"   {provider.title()}:")
            logger.info(f"     Requests: {usage['requests']}")
            logger.info(f"     Tokens: {usage['tokens']:,}")
            logger.info(f"     Cost: ${usage['cost']:.4f}")
        
        # Artifacts generated
        logger.info("\\n📄 Artifacts Generated:")
        for artifact_name, artifact_content in self.artifacts.items():
            if isinstance(artifact_content, str):
                size = len(artifact_content)
                logger.info(f"   {artifact_name.title()}: {size:,} characters")
            else:
                logger.info(f"   {artifact_name.title()}: Structured data")
        
        # Total code generated
        total_code_size = sum(
            len(content) for content in self.artifacts.values() 
            if isinstance(content, str)
        )
        logger.info(f"\\n📦 Total Code Generated: {total_code_size:,} characters ({total_code_size/1024:.1f}KB)")
        
        # Performance summary
        logger.info("\\n⚡ Performance Summary:")
        logger.info(f"   Code generation rate: {total_code_size/total_time:.0f} chars/second")
        logger.info(f"   Cost efficiency: ${self.metrics['total_cost']/total_code_size*1000:.3f} per 1K chars")
        logger.info(f"   Token efficiency: {self.metrics['total_tokens']/total_code_size*1000:.1f} tokens per 1K chars")

        # Router statistics
        logger.info("\\n🎯 Router Statistics:")
        router_status = await self.router.get_provider_status()
        for provider_name, status in router_status.items():
            stats = status.get("stats", {})
            success_rate = 100.0
            if stats.get("requests", 0) > 0:
                success_rate = (stats.get("successes", 0) / stats["requests"]) * 100
            logger.info(f"   {provider_name}: {success_rate:.1f}% success rate")
        
        logger.info("\\n🚀 REAL LLM MULTI-AGENT ORCHESTRATION SUCCESS!")

    async def save_artifacts(self) -> None:
        """Save all generated artifacts to files."""
        logger.info("\\n💾 Saving artifacts...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for artifact_name, content in self.artifacts.items():
            if isinstance(content, str):
                filename = f"todo_app_{artifact_name}_{timestamp}.md"
                with open(filename, "w") as f:
                    f.write(f"# {artifact_name.title()}\\n\\n")
                    f.write(content)
                logger.info(f"   💾 Saved {filename} ({len(content):,} chars)")
        
        logger.info("✅ All artifacts saved successfully!")

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.router:
            for provider in self.router.providers.values():
                await provider.shutdown()


async def main():
    """Main orchestration function."""
    logger.info("🚀 Real LLM Multi-Agent Orchestration Demo Starting...")
    
    demo = RealLLMOrchestrationDemo()
    
    try:
        # Setup infrastructure
        await demo.setup_infrastructure()
        
        # Run orchestration
        await demo.orchestrate_todo_app()
        
        # Save artifacts
        await demo.save_artifacts()
        
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        raise
    
    finally:
        # Cleanup
        await demo.cleanup()


if __name__ == "__main__":
    asyncio.run(main())