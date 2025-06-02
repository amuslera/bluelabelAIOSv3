"""
LLM routing system for AIOSv3 platform.

Provides intelligent routing between cloud and local LLM providers based on
cost, privacy requirements, performance needs, and availability.
"""

from .providers import (
    ClaudeConfig,
    ClaudeProvider,
    LLMProvider,
    LLMRequest,
    LLMResponse,
    LocalConfig,
    LocalProvider,
    ModelCapability,
    ModelInfo,
    ModelSize,
    ModelType,
    ProviderConfig,
    ProviderHealthStatus,
)
from .router import (
    LLMRouter,
    RoutingContext,
    RoutingDecision,
    RoutingPolicy,
    RoutingStrategy,
)

__all__ = [
    # Router classes
    "LLMRouter",
    "RoutingStrategy",
    "RoutingPolicy",
    "RoutingContext",
    "RoutingDecision",
    # Provider classes
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "ModelInfo",
    "ModelCapability",
    "ModelSize",
    "ModelType",
    "ProviderConfig",
    "ProviderHealthStatus",
    "ClaudeProvider",
    "ClaudeConfig",
    "LocalProvider",
    "LocalConfig",
]
