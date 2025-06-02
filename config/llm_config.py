"""
LLM configuration for AIOSv3 platform.

Provides configuration for LLM providers and routing strategies.
"""

import os
from typing import Any

from core.routing.providers.claude import ClaudeConfig
from core.routing.router import RoutingStrategy


def get_claude_config() -> ClaudeConfig:
    """Get Claude provider configuration."""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required. "
            "Set it in your .env file or environment. "
            "For testing, use the mock provider instead."
        )

    return ClaudeConfig(
        provider_name="claude",
        api_key=api_key,
        timeout=30.0,
        max_retries=3,
        rate_limit_requests_per_minute=1000
    )


def get_llm_routing_config() -> dict[str, Any]:
    """Get LLM routing configuration."""
    return {
        "providers": {
            "claude": get_claude_config()
        },
        "default_strategy": RoutingStrategy.BALANCED,
        "fallback_providers": ["claude"],
        "cost_optimization": {
            "enabled": True,
            "max_cost_per_request": 0.10,  # $0.10 max per request
            "budget_alerts": True
        },
        "performance_requirements": {
            "max_response_time_ms": 30000,  # 30 seconds
            "min_availability": 0.99
        }
    }


# Environment-specific configurations
DEVELOPMENT_CONFIG = {
    "llm_routing": get_llm_routing_config(),
    "logging_level": "DEBUG",
    "enable_metrics": True,
    "mock_providers": False  # Set to True to use mock providers for testing
}

TESTING_CONFIG = {
    "llm_routing": get_llm_routing_config(),
    "logging_level": "INFO",
    "enable_metrics": False,
    "mock_providers": True  # Use mock providers in tests
}

PRODUCTION_CONFIG = {
    "llm_routing": get_llm_routing_config(),
    "logging_level": "WARNING",
    "enable_metrics": True,
    "mock_providers": False
}


def get_config(environment: str = "development") -> dict[str, Any]:
    """Get configuration for the specified environment."""
    configs = {
        "development": DEVELOPMENT_CONFIG,
        "testing": TESTING_CONFIG,
        "production": PRODUCTION_CONFIG
    }

    return configs.get(environment, DEVELOPMENT_CONFIG)
