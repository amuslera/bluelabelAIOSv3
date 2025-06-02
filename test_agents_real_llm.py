#!/usr/bin/env python3
"""
Test specialist agents with real LLM providers.

Tests each specialist agent (Backend, Frontend, QA, DevOps) using
real Claude and OpenAI APIs instead of mock responses.
"""

import asyncio
import logging
import os
import time
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


class AgentRealLLMTester:
    """Test specialist agents with real LLM providers."""

    def __init__(self):
        self.router = None
        self.agents = {}
        self.test_results = {}

    async def setup_router(self) -> None:
        """Set up LLM router with real providers."""
        logger.info("Setting up LLM router with real providers...")

        self.router = LLMRouter(
            default_policy=RoutingPolicy(
                strategy=RoutingStrategy.COST_OPTIMIZED,
                max_cost_per_request=0.10,
            )
        )

        # Get API keys
        claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        # Initialize Claude provider
        if claude_api_key:
            claude_config = ClaudeConfig(
                provider_name="claude",
                api_key=claude_api_key,
                timeout=30.0,
            )
            claude_provider = ClaudeProvider(claude_config)
            await claude_provider.initialize()
            self.router.register_provider("claude", claude_provider)
            logger.info("✅ Claude provider registered")

        # Initialize OpenAI provider
        if openai_api_key:
            openai_config = OpenAIConfig(
                provider_name="openai",
                api_key=openai_api_key,
                timeout=30.0,
            )
            openai_provider = OpenAIProvider(openai_config)
            await openai_provider.initialize()
            self.router.register_provider("openai", openai_provider)
            logger.info("✅ OpenAI provider registered")

        # Initialize router
        await self.router.initialize()
        logger.info("✅ LLM Router initialized")

    async def setup_agents(self) -> None:
        """Set up specialist agents with real LLM router."""
        logger.info("Setting up specialist agents...")

        # Backend Agent
        backend_config = BackendAgentConfig()
        self.agents["backend"] = BackendDeveloperAgent(backend_config)
        self.agents["backend"].router = self.router  # Assign router
        await self.agents["backend"].initialize()

        # Frontend Agent
        frontend_config = FrontendAgentConfig()
        self.agents["frontend"] = FrontendDeveloperAgent(frontend_config)
        self.agents["frontend"].router = self.router  # Assign router
        await self.agents["frontend"].initialize()

        # QA Agent
        qa_config = QAAgentConfig()
        self.agents["qa"] = QAEngineerAgent(qa_config)
        self.agents["qa"].router = self.router  # Assign router
        await self.agents["qa"].initialize()

        # DevOps Agent
        devops_config = DevOpsAgentConfig()
        self.agents["devops"] = DevOpsEngineerAgent(devops_config)
        self.agents["devops"].router = self.router  # Assign router
        await self.agents["devops"].initialize()

        logger.info(f"✅ {len(self.agents)} specialist agents initialized")

    def _get_task_type(self, agent_name: str) -> TaskType:
        """Get appropriate task type for agent."""
        task_types = {
            "backend": TaskType.CODE_GENERATION,
            "frontend": TaskType.CODE_GENERATION,
            "qa": TaskType.TESTING,
            "devops": TaskType.DEPLOYMENT,
        }
        return task_types.get(agent_name, TaskType.GENERAL)

    async def test_agent_tasks(self) -> None:
        """Test each agent with domain-specific tasks."""
        logger.info("\\n🧪 Testing agents with real LLM providers...")

        test_cases = {
            "backend": [
                "Create a FastAPI endpoint for user authentication with JWT tokens",
                "Design a database schema for a blog application with users, posts, and comments",
            ],
            "frontend": [
                "Create a React component for a user profile form with validation",
                "Build a responsive navigation bar with dropdown menus using CSS",
            ],
            "qa": [
                "Write unit tests for a user registration function that validates email and password",
                "Create an end-to-end test for a login flow using Playwright",
            ],
            "devops": [
                "Create a Kubernetes deployment manifest for a Node.js application",
                "Write a GitHub Actions workflow for CI/CD with testing and deployment",
            ],
        }

        for agent_name, tasks in test_cases.items():
            self.test_results[agent_name] = []
            
            for i, task in enumerate(tasks, 1):
                logger.info(f"Testing {agent_name} agent - Task {i}: {task[:50]}...")
                
                try:
                    start_time = time.time()
                    
                    # Create task object
                    task_obj = EnhancedTask(
                        task_type=self._get_task_type(agent_name),
                        prompt=task,
                        complexity=5,
                        priority=Priority.MEDIUM,
                    )
                    
                    # Execute task
                    result = await self.agents[agent_name].process_task(task_obj)
                    
                    execution_time = time.time() - start_time
                    
                    # Record results
                    test_result = {
                        "task": task,
                        "success": result.success,
                        "execution_time": execution_time,
                        "output_length": len(result.output or ""),
                        "tokens_used": result.tokens_used,
                        "cost": result.cost,
                        "provider_used": result.provider_used,
                        "model_used": result.model_used,
                    }
                    
                    self.test_results[agent_name].append(test_result)
                    
                    logger.info(f"✅ {agent_name} Task {i}: {execution_time:.2f}s, "
                              f"{test_result['tokens_used']} tokens, "
                              f"${test_result['cost']:.4f}")
                    
                except Exception as e:
                    test_result = {
                        "task": task,
                        "success": False,
                        "error": str(e),
                        "execution_time": time.time() - start_time,
                    }
                    
                    self.test_results[agent_name].append(test_result)
                    logger.error(f"❌ {agent_name} Task {i} failed: {e}")

    async def test_provider_distribution(self) -> None:
        """Test that tasks are properly distributed across providers."""
        logger.info("\\n📊 Analyzing provider distribution...")

        # Get router statistics
        router_status = await self.router.get_provider_status()
        
        for provider_name, status in router_status.items():
            stats = status.get("stats", {})
            requests = stats.get("requests", 0)
            successes = stats.get("successes", 0)
            total_cost = stats.get("total_cost", 0.0)
            
            logger.info(f"{provider_name}: {requests} requests, "
                       f"{successes} successes, ${total_cost:.4f} total cost")

    def print_summary(self) -> None:
        """Print comprehensive test summary."""
        logger.info("\\n📋 Agent Real LLM Integration Summary")
        logger.info("=" * 60)

        total_tasks = 0
        total_successful = 0
        total_cost = 0.0
        total_time = 0.0

        for agent_name, results in self.test_results.items():
            if not results:
                continue
                
            successful = sum(1 for r in results if r["success"])
            total_tasks += len(results)
            total_successful += successful
            
            agent_cost = sum(r.get("cost", 0) for r in results if r["success"])
            agent_time = sum(r.get("execution_time", 0) for r in results if r["success"])
            
            total_cost += agent_cost
            total_time += agent_time
            
            logger.info(f"{agent_name.upper()} Agent:")
            logger.info(f"  Tasks: {successful}/{len(results)} successful")
            if successful > 0:
                avg_time = agent_time / successful
                logger.info(f"  Avg time: {avg_time:.2f}s")
                logger.info(f"  Total cost: ${agent_cost:.4f}")
                
                # Show provider usage
                providers = {}
                for r in results:
                    if r["success"]:
                        provider = r.get("provider_used", "unknown")
                        providers[provider] = providers.get(provider, 0) + 1
                
                if providers:
                    provider_str = ", ".join(f"{p}: {c}" for p, c in providers.items())
                    logger.info(f"  Providers: {provider_str}")

        logger.info(f"\\nOVERALL RESULTS:")
        logger.info(f"  Success rate: {total_successful}/{total_tasks} ({total_successful/total_tasks*100:.1f}%)")
        logger.info(f"  Total cost: ${total_cost:.4f}")
        logger.info(f"  Total time: {total_time:.2f}s")
        
        if total_successful > 0:
            logger.info(f"  Avg cost per task: ${total_cost/total_successful:.4f}")
            logger.info(f"  Avg time per task: {total_time/total_successful:.2f}s")

        logger.info("\\n🎉 Agent Real LLM Integration Test Complete!")

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.router:
            for provider in self.router.providers.values():
                await provider.shutdown()


async def main():
    """Main test function."""
    logger.info("🚀 Starting Agent Real LLM Integration Tests")
    
    tester = AgentRealLLMTester()
    
    try:
        # Setup
        await tester.setup_router()
        await tester.setup_agents()
        
        # Run tests
        await tester.test_agent_tasks()
        await tester.test_provider_distribution()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    
    finally:
        # Cleanup
        await tester.cleanup()


if __name__ == "__main__":
    asyncio.run(main())