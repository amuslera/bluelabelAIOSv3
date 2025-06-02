"""
OpenAI provider implementation for AIOSv3 platform.

Provides integration with OpenAI's GPT API for cloud-based LLM services.
"""

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from typing import Any, Dict, List, Optional

import httpx

from .base import (
    LLMProvider,
    LLMRequest,
    LLMResponse,
    ModelCapability,
    ModelInfo,
    ModelSize,
    ModelType,
    ProviderConfig,
    ProviderHealthStatus,
)

logger = logging.getLogger(__name__)


class OpenAIConfig(ProviderConfig):
    """Configuration specific to OpenAI provider."""

    api_version: str = "v1"
    max_tokens_default: int = 4096
    temperature_default: float = 0.7
    organization_id: Optional[str] = None


class OpenAIProvider(LLMProvider):
    """
    Provider implementation for OpenAI's GPT API.

    Supports GPT-4, GPT-3.5 models with chat completions, function calling,
    and streaming responses.
    """

    # OpenAI model definitions
    OPENAI_MODELS = {
        "gpt-4-turbo": ModelInfo(
            id="gpt-4-turbo",
            name="GPT-4 Turbo",
            provider="openai",
            model_type=ModelType.CHAT,
            size=ModelSize.LARGE,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.REASONING,
                ModelCapability.ANALYSIS,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.MATH,
                ModelCapability.TOOL_USE,
                ModelCapability.VISION,
            ],
            context_length=128000,
            input_cost_per_token=10.0e-6,  # $10.00 per million tokens
            output_cost_per_token=30.0e-6,  # $30.00 per million tokens
            max_requests_per_minute=500,
            supports_streaming=True,
            supports_functions=True,
            privacy_level="cloud",
            performance_tier=5,
            availability=0.995,
        ),
        "gpt-4o": ModelInfo(
            id="gpt-4o",
            name="GPT-4o",
            provider="openai",
            model_type=ModelType.CHAT,
            size=ModelSize.LARGE,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.REASONING,
                ModelCapability.ANALYSIS,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.MATH,
                ModelCapability.TOOL_USE,
                ModelCapability.VISION,
                ModelCapability.AUDIO,
            ],
            context_length=128000,
            input_cost_per_token=5.0e-6,  # $5.00 per million tokens
            output_cost_per_token=15.0e-6,  # $15.00 per million tokens
            max_requests_per_minute=1000,
            supports_streaming=True,
            supports_functions=True,
            privacy_level="cloud",
            performance_tier=5,
            availability=0.995,
        ),
        "gpt-3.5-turbo": ModelInfo(
            id="gpt-3.5-turbo",
            name="GPT-3.5 Turbo",
            provider="openai",
            model_type=ModelType.CHAT,
            size=ModelSize.MEDIUM,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.REASONING,
                ModelCapability.ANALYSIS,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.TOOL_USE,
            ],
            context_length=16384,
            input_cost_per_token=0.5e-6,  # $0.50 per million tokens
            output_cost_per_token=1.5e-6,  # $1.50 per million tokens
            max_requests_per_minute=3500,
            supports_streaming=True,
            supports_functions=True,
            privacy_level="cloud",
            performance_tier=4,
            availability=0.995,
        ),
        "gpt-4o-mini": ModelInfo(
            id="gpt-4o-mini",
            name="GPT-4o Mini",
            provider="openai",
            model_type=ModelType.CHAT,
            size=ModelSize.SMALL,
            capabilities=[
                ModelCapability.TEXT_GENERATION,
                ModelCapability.CODE_GENERATION,
                ModelCapability.REASONING,
                ModelCapability.ANALYSIS,
                ModelCapability.CREATIVE_WRITING,
                ModelCapability.TOOL_USE,
            ],
            context_length=128000,
            input_cost_per_token=0.15e-6,  # $0.15 per million tokens
            output_cost_per_token=0.6e-6,  # $0.60 per million tokens
            max_requests_per_minute=5000,
            supports_streaming=True,
            supports_functions=True,
            privacy_level="cloud",
            performance_tier=3,
            availability=0.995,
        ),
    }

    def __init__(self, config: OpenAIConfig):
        """Initialize OpenAI provider."""
        super().__init__(config)
        self.config: OpenAIConfig = config
        self.client: Optional[httpx.AsyncClient] = None
        self.base_url = config.api_base or "https://api.openai.com"

        # Rate limiting
        self._request_timestamps: List[float] = []
        self._request_lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize the OpenAI provider and load available models."""
        logger.info("Initializing OpenAI provider")

        if not self.config.api_key:
            raise ValueError("OpenAI API key is required")

        # Initialize HTTP client
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        if self.config.organization_id:
            headers["OpenAI-Organization"] = self.config.organization_id

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
        )

        # Load available models
        self._models = self.OPENAI_MODELS.copy()

        # Verify API access
        await self._verify_api_access()

        logger.info(f"OpenAI provider initialized with {len(self._models)} models")

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response using OpenAI API."""
        if not self.client:
            raise RuntimeError("Provider not initialized")

        start_time = time.time()

        try:
            # Rate limiting
            await self._enforce_rate_limits()

            # Prepare request payload
            payload = self._prepare_request_payload(request)

            # Make API request
            response = await self.client.post("/v1/chat/completions", json=payload)
            response.raise_for_status()

            # Parse response
            response_data = response.json()
            return self._parse_response(request, response_data, start_time)

        except httpx.HTTPStatusError as e:
            logger.error(
                f"OpenAI API error: {e.response.status_code} - {e.response.text}"
            )
            raise
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            raise

    async def generate_stream(self, request: LLMRequest) -> AsyncIterator[str]:
        """Generate a streaming response using OpenAI API."""
        if not self.client:
            raise RuntimeError("Provider not initialized")

        try:
            # Rate limiting
            await self._enforce_rate_limits()

            # Prepare request payload
            payload = self._prepare_request_payload(request)
            payload["stream"] = True

            # Make streaming request
            async with self.client.stream(
                "POST", "/v1/chat/completions", json=payload
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data.strip() == "[DONE]":
                            break

                        try:
                            import json

                            event_data = json.loads(data)

                            if "choices" in event_data and event_data["choices"]:
                                delta = event_data["choices"][0].get("delta", {})
                                if "content" in delta and delta["content"]:
                                    yield delta["content"]

                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Error in OpenAI streaming: {e}")
            raise

    async def get_models(self) -> List[ModelInfo]:
        """Get list of available OpenAI models."""
        return list(self._models.values())

    async def health_check(self) -> ProviderHealthStatus:
        """Perform health check on OpenAI API."""
        if not self.client:
            return ProviderHealthStatus(
                provider_name=self.provider_name,
                is_healthy=False,
                status_message="Provider not initialized",
            )

        start_time = time.time()

        try:
            # Simple API health check
            response = await self.client.get("/v1/models", timeout=10.0)
            response_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                return ProviderHealthStatus(
                    provider_name=self.provider_name,
                    is_healthy=True,
                    response_time_ms=response_time,
                    available_models=list(self._models.keys()),
                    status_message="API accessible",
                )
            else:
                return ProviderHealthStatus(
                    provider_name=self.provider_name,
                    is_healthy=False,
                    response_time_ms=response_time,
                    status_message=f"API returned status {response.status_code}",
                )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return ProviderHealthStatus(
                provider_name=self.provider_name,
                is_healthy=False,
                response_time_ms=response_time,
                status_message=f"Health check failed: {e}",
            )

    async def shutdown(self) -> None:
        """Shutdown the provider and cleanup resources."""
        if self.client:
            await self.client.aclose()
            self.client = None
        logger.info("OpenAI provider shutdown completed")

    def _prepare_request_payload(self, request: LLMRequest) -> Dict[str, Any]:
        """Prepare the request payload for OpenAI API."""
        payload = {
            "model": request.model_id,
            "messages": request.messages,
            "max_tokens": request.max_tokens or self.config.max_tokens_default,
            "temperature": request.temperature,
        }

        # Optional parameters
        if request.top_p is not None:
            payload["top_p"] = request.top_p

        if request.frequency_penalty is not None:
            payload["frequency_penalty"] = request.frequency_penalty

        if request.presence_penalty is not None:
            payload["presence_penalty"] = request.presence_penalty

        if request.stop_sequences:
            payload["stop"] = request.stop_sequences

        # Function calling support
        if request.functions:
            payload["functions"] = request.functions
            if request.function_call:
                payload["function_call"] = request.function_call

        # User ID for tracking
        if request.user_id:
            payload["user"] = request.user_id

        return payload

    def _parse_response(
        self, request: LLMRequest, response_data: Dict[str, Any], start_time: float
    ) -> LLMResponse:
        """Parse OpenAI API response into LLMResponse."""
        response_time = (time.time() - start_time) * 1000

        # Extract content and function call
        choice = response_data["choices"][0]
        message = choice["message"]
        
        content = message.get("content", "") or ""
        function_call = message.get("function_call")

        # Extract usage information
        usage = response_data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        # Calculate costs
        model_info = self.get_model_info(request.model_id)
        input_cost = 0.0
        output_cost = 0.0

        if model_info:
            input_cost = input_tokens * model_info.input_cost_per_token
            output_cost = output_tokens * model_info.output_cost_per_token

        return LLMResponse(
            content=content,
            model_id=request.model_id,
            provider=self.provider_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=input_cost + output_cost,
            response_time_ms=response_time,
            finish_reason=choice.get("finish_reason"),
            function_call=function_call,
            request_id=response_data.get("id"),
        )

    async def _verify_api_access(self) -> None:
        """Verify API access by making a test request."""
        try:
            response = await self.client.get("/v1/models", timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid OpenAI API key")
            elif e.response.status_code == 403:
                raise ValueError("OpenAI API access forbidden")
            else:
                logger.warning(f"API verification returned {e.response.status_code}")
        except Exception as e:
            logger.warning(f"API verification failed: {e}")

    async def _enforce_rate_limits(self) -> None:
        """Enforce rate limiting for OpenAI API."""
        if (
            not hasattr(self.config, "rate_limit_requests_per_minute")
            or not self.config.rate_limit_requests_per_minute
        ):
            return

        async with self._request_lock:
            current_time = time.time()

            # Remove timestamps older than 1 minute
            self._request_timestamps = [
                ts for ts in self._request_timestamps if current_time - ts < 60
            ]

            # Check if we're at the rate limit
            if (
                len(self._request_timestamps)
                >= self.config.rate_limit_requests_per_minute
            ):
                # Calculate wait time until oldest request expires
                oldest_request = min(self._request_timestamps)
                wait_time = 60 - (current_time - oldest_request)

                if wait_time > 0:
                    logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)

            # Add current request timestamp
            self._request_timestamps.append(current_time)