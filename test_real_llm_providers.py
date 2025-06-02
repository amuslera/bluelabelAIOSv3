#!/usr/bin/env python3
"""
Test script for real LLM provider integration.

Tests both Claude and OpenAI providers with actual API calls to validate
the complete LLM routing system works with real APIs.
"""

import asyncio
import logging
import os
import time
from typing import Dict, Any
from dotenv import load_dotenv

from core.routing.providers import (
    ClaudeProvider,
    ClaudeConfig,
    OpenAIProvider,
    OpenAIConfig,
    LLMRequest,
)
from core.routing.router import LLMRouter, RoutingContext, RoutingPolicy, RoutingStrategy
from agents.base.types import TaskType

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RealLLMProviderTester:
    """Test real LLM providers with actual API calls."""

    def __init__(self):
        self.router = LLMRouter()
        self.test_results: Dict[str, Any] = {
            "claude": {"initialized": False, "tests": []},
            "openai": {"initialized": False, "tests": []},
            "router": {"tests": []},
        }

    async def setup_providers(self) -> None:
        """Set up Claude and OpenAI providers with API keys from .env."""
        logger.info("Setting up real LLM providers...")

        # Get API keys from environment
        claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not claude_api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment")
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY not found in environment")

        # Initialize Claude provider
        if claude_api_key:
            try:
                claude_config = ClaudeConfig(
                    provider_name="claude",
                    api_key=claude_api_key,
                    timeout=30.0,
                    rate_limit_requests_per_minute=100,
                )
                claude_provider = ClaudeProvider(claude_config)
                await claude_provider.initialize()
                self.router.register_provider("claude", claude_provider)
                self.test_results["claude"]["initialized"] = True
                logger.info("✅ Claude provider initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Claude provider: {e}")
                self.test_results["claude"]["error"] = str(e)

        # Initialize OpenAI provider
        if openai_api_key:
            try:
                openai_config = OpenAIConfig(
                    provider_name="openai",
                    api_key=openai_api_key,
                    timeout=30.0,
                    rate_limit_requests_per_minute=200,
                )
                openai_provider = OpenAIProvider(openai_config)
                await openai_provider.initialize()
                self.router.register_provider("openai", openai_provider)
                self.test_results["openai"]["initialized"] = True
                logger.info("✅ OpenAI provider initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI provider: {e}")
                self.test_results["openai"]["error"] = str(e)

        # Initialize router
        await self.router.initialize()
        logger.info("✅ LLM Router initialized")

    async def test_individual_providers(self) -> None:
        """Test each provider individually."""
        logger.info("\n🧪 Testing individual providers...")

        test_request = LLMRequest(
            messages=[
                {"role": "user", "content": "Write a simple 'Hello, World!' function in Python. Be concise."}
            ],
            model_id="",  # Will be set per provider
            max_tokens=200,
            temperature=0.3,
        )

        # Test Claude provider
        if self.test_results["claude"]["initialized"]:
            await self._test_claude_provider(test_request)

        # Test OpenAI provider
        if self.test_results["openai"]["initialized"]:
            await self._test_openai_provider(test_request)

    async def _test_claude_provider(self, base_request: LLMRequest) -> None:
        """Test Claude provider with different models."""
        logger.info("Testing Claude provider...")
        
        claude_provider = self.router.providers["claude"]
        claude_models = ["claude-3-haiku-20240307", "claude-3-5-sonnet-20241022"]

        for model_id in claude_models:
            if claude_provider.has_model(model_id):
                try:
                    start_time = time.time()
                    request = base_request.model_copy()
                    request.model_id = model_id

                    response = await claude_provider.generate(request)
                    
                    test_result = {
                        "model": model_id,
                        "success": True,
                        "response_time": time.time() - start_time,
                        "tokens": response.total_tokens,
                        "cost": response.total_cost,
                        "content_length": len(response.content),
                        "content_preview": response.content[:100] + "..." if len(response.content) > 100 else response.content,
                    }
                    self.test_results["claude"]["tests"].append(test_result)
                    
                    logger.info(f"✅ Claude {model_id}: {response.total_tokens} tokens, ${response.total_cost:.4f}, {time.time() - start_time:.2f}s")
                    
                except Exception as e:
                    test_result = {
                        "model": model_id,
                        "success": False,
                        "error": str(e),
                    }
                    self.test_results["claude"]["tests"].append(test_result)
                    logger.error(f"❌ Claude {model_id} failed: {e}")

    async def _test_openai_provider(self, base_request: LLMRequest) -> None:
        """Test OpenAI provider with different models."""
        logger.info("Testing OpenAI provider...")
        
        openai_provider = self.router.providers["openai"]
        openai_models = ["gpt-4o-mini", "gpt-3.5-turbo"]

        for model_id in openai_models:
            if openai_provider.has_model(model_id):
                try:
                    start_time = time.time()
                    request = base_request.model_copy()
                    request.model_id = model_id

                    response = await openai_provider.generate(request)
                    
                    test_result = {
                        "model": model_id,
                        "success": True,
                        "response_time": time.time() - start_time,
                        "tokens": response.total_tokens,
                        "cost": response.total_cost,
                        "content_length": len(response.content),
                        "content_preview": response.content[:100] + "..." if len(response.content) > 100 else response.content,
                    }
                    self.test_results["openai"]["tests"].append(test_result)
                    
                    logger.info(f"✅ OpenAI {model_id}: {response.total_tokens} tokens, ${response.total_cost:.4f}, {time.time() - start_time:.2f}s")
                    
                except Exception as e:
                    test_result = {
                        "model": model_id,
                        "success": False,
                        "error": str(e),
                    }
                    self.test_results["openai"]["tests"].append(test_result)
                    logger.error(f"❌ OpenAI {model_id} failed: {e}")

    async def test_router_decisions(self) -> None:
        """Test router decision making with different strategies."""
        logger.info("\n🎯 Testing router decision making...")

        test_cases = [
            {
                "name": "Cost Optimized",
                "policy": RoutingPolicy(strategy=RoutingStrategy.COST_OPTIMIZED),
                "context": RoutingContext(
                    agent_id="test_agent",
                    task_type=TaskType.CODE_GENERATION,
                    complexity=3,
                ),
                "request": LLMRequest(
                    messages=[{"role": "user", "content": "Generate a simple Python function"}],
                    model_id="",
                    max_tokens=150,
                ),
            },
            {
                "name": "Performance Optimized",
                "policy": RoutingPolicy(strategy=RoutingStrategy.PERFORMANCE_OPTIMIZED),
                "context": RoutingContext(
                    agent_id="test_agent",
                    task_type=TaskType.SYSTEM_DESIGN,
                    complexity=8,
                ),
                "request": LLMRequest(
                    messages=[{"role": "user", "content": "Explain quantum computing concepts"}],
                    model_id="",
                    max_tokens=300,
                ),
            },
        ]

        for test_case in test_cases:
            try:
                start_time = time.time()
                
                # Get routing decision
                decision = await self.router.route_request(
                    test_case["request"],
                    test_case["context"],
                    test_case["policy"],
                )

                # Execute the request
                response = await self.router.execute_request(
                    test_case["request"],
                    decision,
                )

                test_result = {
                    "name": test_case["name"],
                    "success": True,
                    "provider": decision.provider_name,
                    "model": decision.model_id,
                    "reasoning": decision.reasoning,
                    "estimated_cost": decision.estimated_cost,
                    "actual_cost": response.total_cost,
                    "response_time": time.time() - start_time,
                    "tokens": response.total_tokens,
                }
                self.test_results["router"]["tests"].append(test_result)

                logger.info(f"✅ {test_case['name']}: {decision.provider_name}/{decision.model_id}")
                logger.info(f"   Reasoning: {decision.reasoning}")
                logger.info(f"   Cost: ${response.total_cost:.4f}, Time: {time.time() - start_time:.2f}s")

            except Exception as e:
                test_result = {
                    "name": test_case["name"],
                    "success": False,
                    "error": str(e),
                }
                self.test_results["router"]["tests"].append(test_result)
                logger.error(f"❌ {test_case['name']} failed: {e}")

    async def test_provider_health(self) -> None:
        """Test provider health checks."""
        logger.info("\n🏥 Testing provider health...")

        status = await self.router.get_provider_status()
        
        for provider_name, provider_status in status.items():
            health = provider_status["health"]
            is_healthy = health.get("is_healthy", False)
            response_time = health.get("response_time_ms", 0)
            
            logger.info(f"{provider_name}: {'✅ Healthy' if is_healthy else '❌ Unhealthy'} ({response_time:.0f}ms)")
            if not is_healthy:
                logger.info(f"   Error: {health.get('status_message', 'Unknown error')}")

    def print_summary(self) -> None:
        """Print test summary."""
        logger.info("\n📊 Test Summary")
        logger.info("=" * 50)

        # Provider initialization
        claude_init = "✅" if self.test_results["claude"]["initialized"] else "❌"
        openai_init = "✅" if self.test_results["openai"]["initialized"] else "❌"
        logger.info(f"Provider Initialization:")
        logger.info(f"  Claude: {claude_init}")
        logger.info(f"  OpenAI: {openai_init}")

        # Provider tests
        for provider in ["claude", "openai"]:
            tests = self.test_results[provider]["tests"]
            if tests:
                successful = sum(1 for t in tests if t["success"])
                total = len(tests)
                logger.info(f"{provider.title()} Tests: {successful}/{total} passed")
                
                if successful > 0:
                    total_cost = sum(t.get("cost", 0) for t in tests if t["success"])
                    avg_time = sum(t.get("response_time", 0) for t in tests if t["success"]) / successful
                    logger.info(f"  Total cost: ${total_cost:.4f}")
                    logger.info(f"  Avg response time: {avg_time:.2f}s")

        # Router tests
        router_tests = self.test_results["router"]["tests"]
        if router_tests:
            successful = sum(1 for t in router_tests if t["success"])
            total = len(router_tests)
            logger.info(f"Router Tests: {successful}/{total} passed")

        logger.info("\n🎉 Real LLM Provider Integration Test Complete!")


async def main():
    """Main test function."""
    logger.info("🚀 Starting Real LLM Provider Integration Tests")
    
    tester = RealLLMProviderTester()
    
    try:
        # Setup providers
        await tester.setup_providers()
        
        # Run tests
        await tester.test_individual_providers()
        await tester.test_router_decisions()
        await tester.test_provider_health()
        
        # Print summary
        tester.print_summary()
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    
    finally:
        # Cleanup
        for provider in tester.router.providers.values():
            await provider.shutdown()


if __name__ == "__main__":
    asyncio.run(main())