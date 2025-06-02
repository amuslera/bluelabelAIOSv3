#!/usr/bin/env python3
"""
Error Recovery System for AIOSv3

Provides intelligent error detection, pattern recognition, and recovery strategies
for the multi-agent system. This system learns from errors and improves over time.
"""

import asyncio
import json
import logging
import re
import time
import traceback
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

import redis.asyncio as redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"        # Can be ignored or logged
    MEDIUM = "medium"  # Should be handled but not critical
    HIGH = "high"      # Needs immediate handling
    CRITICAL = "critical"  # System-threatening


class RecoveryStrategy(Enum):
    """Available recovery strategies."""
    RETRY = "retry"
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    COMPENSATE = "compensate"
    ESCALATE = "escalate"
    IGNORE = "ignore"


@dataclass
class ErrorPattern:
    """Represents a known error pattern."""
    pattern_id: str
    error_type: type[Exception]
    message_pattern: Optional[str] = None
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    recovery_strategy: RecoveryStrategy = RecoveryStrategy.RETRY
    max_retries: int = 3
    backoff_base: float = 1.0
    fallback_action: Optional[str] = None
    occurrence_count: int = 0
    last_seen: Optional[float] = None
    success_rate: float = 0.0

    def matches(self, error: Exception) -> bool:
        """Check if an error matches this pattern."""
        if not isinstance(error, self.error_type):
            return False

        if self.message_pattern:
            error_message = str(error)
            return bool(re.search(self.message_pattern, error_message, re.IGNORECASE))

        return True


@dataclass
class ErrorContext:
    """Context information for an error."""
    error: Exception
    agent_id: str
    task_id: Optional[str] = None
    operation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    stack_trace: str = field(default_factory=lambda: "")
    additional_info: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0

    def __post_init__(self):
        if not self.stack_trace and self.error:
            self.stack_trace = traceback.format_exc()


@dataclass
class RecoveryResult:
    """Result of a recovery attempt."""
    success: bool
    strategy_used: RecoveryStrategy
    retry_count: int
    duration: float
    result: Optional[Any] = None
    error: Optional[Exception] = None


class ErrorRecoverySystem:
    """
    Intelligent error recovery system that learns from patterns
    and applies appropriate recovery strategies.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client: redis.Optional[Redis] = None
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.error_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._load_default_patterns()

    def _load_default_patterns(self):
        """Load default error patterns."""
        default_patterns = [
            ErrorPattern(
                pattern_id="network_timeout",
                error_type=asyncio.TimeoutError,
                severity=ErrorSeverity.MEDIUM,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                max_retries=3,
                backoff_base=2.0
            ),
            ErrorPattern(
                pattern_id="redis_connection",
                error_type=RedisError,
                message_pattern="connection",
                severity=ErrorSeverity.HIGH,
                recovery_strategy=RecoveryStrategy.CIRCUIT_BREAKER,
                max_retries=5,
                backoff_base=1.5
            ),
            ErrorPattern(
                pattern_id="rate_limit",
                error_type=Exception,
                message_pattern="rate.?limit|too.?many.?requests",
                severity=ErrorSeverity.MEDIUM,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                max_retries=5,
                backoff_base=5.0
            ),
            ErrorPattern(
                pattern_id="auth_failure",
                error_type=Exception,
                message_pattern="auth|unauthorized|forbidden",
                severity=ErrorSeverity.HIGH,
                recovery_strategy=RecoveryStrategy.ESCALATE,
                max_retries=1
            ),
            ErrorPattern(
                pattern_id="resource_exhausted",
                error_type=Exception,
                message_pattern="memory|disk.?full|quota",
                severity=ErrorSeverity.CRITICAL,
                recovery_strategy=RecoveryStrategy.ESCALATE,
                max_retries=0
            )
        ]

        for pattern in default_patterns:
            self.error_patterns[pattern.pattern_id] = pattern

    async def setup_redis(self):
        """Initialize Redis connection for pattern persistence."""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis_client.ping()

            # Load persisted patterns
            await self._load_patterns_from_redis()

            logger.info("Redis connection established for error recovery")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None

    async def _load_patterns_from_redis(self):
        """Load error patterns from Redis."""
        if not self.redis_client:
            return

        try:
            pattern_keys = await self.redis_client.keys("error_pattern:*")
            for key in pattern_keys:
                pattern_data = await self.redis_client.hgetall(key)
                if pattern_data:
                    # Reconstruct ErrorPattern (simplified for this example)
                    pattern_id = key.split(":")[-1]
                    # In production, properly deserialize the pattern
                    logger.debug(f"Loaded pattern {pattern_id} from Redis")
        except RedisError as e:
            logger.error(f"Failed to load patterns from Redis: {e}")

    async def _persist_pattern(self, pattern: ErrorPattern):
        """Persist error pattern to Redis."""
        if not self.redis_client:
            return

        try:
            key = f"error_pattern:{pattern.pattern_id}"
            # Simplified - in production, properly serialize all fields
            await self.redis_client.hset(key, mapping={
                "error_type": pattern.error_type.__name__,
                "severity": pattern.severity.value,
                "recovery_strategy": pattern.recovery_strategy.value,
                "occurrence_count": str(pattern.occurrence_count),
                "success_rate": str(pattern.success_rate)
            })
            await self.redis_client.expire(key, 86400 * 30)  # 30 days
        except RedisError as e:
            logger.error(f"Failed to persist pattern: {e}")

    def identify_pattern(self, error_context: ErrorContext) -> Optional[ErrorPattern]:
        """Identify which error pattern matches the given error."""
        for pattern in self.error_patterns.values():
            if pattern.matches(error_context.error):
                # Update pattern statistics
                pattern.occurrence_count += 1
                pattern.last_seen = time.time()
                return pattern

        # No pattern found - create a generic one
        return self._create_generic_pattern(error_context)

    def _create_generic_pattern(self, error_context: ErrorContext) -> ErrorPattern:
        """Create a generic pattern for unknown errors."""
        error_type = type(error_context.error)
        pattern_id = f"generic_{error_type.__name__}_{int(time.time())}"

        return ErrorPattern(
            pattern_id=pattern_id,
            error_type=error_type,
            severity=ErrorSeverity.MEDIUM,
            recovery_strategy=RecoveryStrategy.RETRY,
            max_retries=2
        )

    async def recover(self, error_context: ErrorContext,
                     operation: Callable, *args, **kwargs) -> RecoveryResult:
        """
        Attempt to recover from an error by applying appropriate strategies.
        
        Args:
            error_context: Context information about the error
            operation: The operation to retry/recover
            *args, **kwargs: Arguments for the operation
            
        Returns:
            RecoveryResult with outcome information
        """
        start_time = time.time()
        pattern = self.identify_pattern(error_context)

        if not pattern:
            # No pattern found, fail fast
            return RecoveryResult(
                success=False,
                strategy_used=RecoveryStrategy.IGNORE,
                retry_count=0,
                duration=time.time() - start_time,
                error=error_context.error
            )

        # Record error occurrence
        self._record_error(error_context, pattern)

        # Apply recovery strategy
        result = await self._apply_strategy(
            pattern, error_context, operation, *args, **kwargs
        )

        # Update pattern success rate
        if result.success:
            pattern.success_rate = (
                pattern.success_rate * 0.9 + 0.1
            )  # Exponential moving average
        else:
            pattern.success_rate *= 0.9

        # Persist updated pattern
        await self._persist_pattern(pattern)

        return result

    async def _apply_strategy(self, pattern: ErrorPattern,
                            error_context: ErrorContext,
                            operation: Callable, *args, **kwargs) -> RecoveryResult:
        """Apply the recovery strategy specified by the pattern."""
        strategy = pattern.recovery_strategy

        if strategy == RecoveryStrategy.RETRY:
            return await self._retry_strategy(pattern, error_context, operation, *args, **kwargs)
        elif strategy == RecoveryStrategy.RETRY_WITH_BACKOFF:
            return await self._retry_with_backoff_strategy(pattern, error_context, operation, *args, **kwargs)
        elif strategy == RecoveryStrategy.CIRCUIT_BREAKER:
            return await self._circuit_breaker_strategy(pattern, error_context, operation, *args, **kwargs)
        elif strategy == RecoveryStrategy.FALLBACK:
            return await self._fallback_strategy(pattern, error_context, operation, *args, **kwargs)
        elif strategy == RecoveryStrategy.ESCALATE:
            return await self._escalate_strategy(pattern, error_context)
        else:
            # IGNORE or unknown strategy
            return RecoveryResult(
                success=False,
                strategy_used=strategy,
                retry_count=0,
                duration=0,
                error=error_context.error
            )

    async def _retry_strategy(self, pattern: ErrorPattern,
                            error_context: ErrorContext,
                            operation: Callable, *args, **kwargs) -> RecoveryResult:
        """Simple retry strategy."""
        start_time = time.time()
        last_error = error_context.error

        for attempt in range(pattern.max_retries):
            try:
                result = await operation(*args, **kwargs)
                return RecoveryResult(
                    success=True,
                    strategy_used=RecoveryStrategy.RETRY,
                    retry_count=attempt + 1,
                    duration=time.time() - start_time,
                    result=result
                )
            except Exception as e:
                last_error = e
                logger.warning(f"Retry {attempt + 1}/{pattern.max_retries} failed: {e}")

        return RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.RETRY,
            retry_count=pattern.max_retries,
            duration=time.time() - start_time,
            error=last_error
        )

    async def _retry_with_backoff_strategy(self, pattern: ErrorPattern,
                                         error_context: ErrorContext,
                                         operation: Callable, *args, **kwargs) -> RecoveryResult:
        """Retry with exponential backoff."""
        start_time = time.time()
        last_error = error_context.error

        for attempt in range(pattern.max_retries):
            try:
                result = await operation(*args, **kwargs)
                return RecoveryResult(
                    success=True,
                    strategy_used=RecoveryStrategy.RETRY_WITH_BACKOFF,
                    retry_count=attempt + 1,
                    duration=time.time() - start_time,
                    result=result
                )
            except Exception as e:
                last_error = e
                wait_time = pattern.backoff_base ** attempt
                logger.warning(f"Retry {attempt + 1}/{pattern.max_retries} failed, waiting {wait_time}s: {e}")
                await asyncio.sleep(wait_time)

        return RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.RETRY_WITH_BACKOFF,
            retry_count=pattern.max_retries,
            duration=time.time() - start_time,
            error=last_error
        )

    async def _circuit_breaker_strategy(self, pattern: ErrorPattern,
                                      error_context: ErrorContext,
                                      operation: Callable, *args, **kwargs) -> RecoveryResult:
        """Circuit breaker pattern for preventing cascading failures."""
        breaker_id = f"{error_context.agent_id}:{error_context.operation or 'unknown'}"

        if breaker_id not in self.circuit_breakers:
            self.circuit_breakers[breaker_id] = CircuitBreaker(
                failure_threshold=3,
                recovery_timeout=60,
                expected_exception=pattern.error_type
            )

        breaker = self.circuit_breakers[breaker_id]

        try:
            result = await breaker.call(operation, *args, **kwargs)
            return RecoveryResult(
                success=True,
                strategy_used=RecoveryStrategy.CIRCUIT_BREAKER,
                retry_count=1,
                duration=0,
                result=result
            )
        except Exception as e:
            return RecoveryResult(
                success=False,
                strategy_used=RecoveryStrategy.CIRCUIT_BREAKER,
                retry_count=1,
                duration=0,
                error=e
            )

    async def _fallback_strategy(self, pattern: ErrorPattern,
                               error_context: ErrorContext,
                               operation: Callable, *args, **kwargs) -> RecoveryResult:
        """Fallback to alternative action."""
        if pattern.fallback_action:
            logger.info(f"Executing fallback action: {pattern.fallback_action}")
            # In a real implementation, execute the fallback
            return RecoveryResult(
                success=True,
                strategy_used=RecoveryStrategy.FALLBACK,
                retry_count=0,
                duration=0,
                result=f"Fallback: {pattern.fallback_action}"
            )
        else:
            return RecoveryResult(
                success=False,
                strategy_used=RecoveryStrategy.FALLBACK,
                retry_count=0,
                duration=0,
                error=Exception("No fallback action defined")
            )

    async def _escalate_strategy(self, pattern: ErrorPattern,
                               error_context: ErrorContext) -> RecoveryResult:
        """Escalate error to human operator or higher-level system."""
        logger.error(f"ESCALATION REQUIRED: {error_context.error}")

        # Send notification to monitoring system
        if self.redis_client:
            try:
                await self.redis_client.lpush(
                    "escalated_errors",
                    json.dumps({
                        "error_type": type(error_context.error).__name__,
                        "message": str(error_context.error),
                        "agent_id": error_context.agent_id,
                        "task_id": error_context.task_id,
                        "timestamp": error_context.timestamp,
                        "pattern_id": pattern.pattern_id
                    })
                )
            except Exception as e:
                logger.error(f"Failed to escalate error: {e}")

        return RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.ESCALATE,
            retry_count=0,
            duration=0,
            error=error_context.error
        )

    def _record_error(self, error_context: ErrorContext, pattern: ErrorPattern):
        """Record error occurrence for analysis."""
        key = f"{error_context.agent_id}:{pattern.pattern_id}"
        self.error_history[key].append({
            "timestamp": error_context.timestamp,
            "error_type": type(error_context.error).__name__,
            "message": str(error_context.error),
            "task_id": error_context.task_id,
            "retry_count": error_context.retry_count
        })

    def get_error_statistics(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get error statistics for analysis."""
        stats = {
            "total_errors": 0,
            "errors_by_pattern": {},
            "errors_by_severity": {s.value: 0 for s in ErrorSeverity},
            "recovery_success_rate": {},
            "most_common_errors": []
        }

        for pattern_id, pattern in self.error_patterns.items():
            if pattern.occurrence_count > 0:
                stats["total_errors"] += pattern.occurrence_count
                stats["errors_by_pattern"][pattern_id] = pattern.occurrence_count
                stats["errors_by_severity"][pattern.severity.value] += pattern.occurrence_count
                stats["recovery_success_rate"][pattern_id] = pattern.success_rate

        # Sort by occurrence
        stats["most_common_errors"] = sorted(
            stats["errors_by_pattern"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        return stats


class CircuitBreaker:
    """Circuit breaker implementation to prevent cascading failures."""

    class State(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60,
                 expected_exception: type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = self.State.CLOSED

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == self.State.OPEN:
            if self._should_attempt_reset():
                self.state = self.State.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = self.State.CLOSED

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = self.State.OPEN
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")


# Example usage
async def example_usage():
    """Example of using the error recovery system."""
    recovery_system = ErrorRecoverySystem()
    await recovery_system.setup_redis()

    # Simulate an operation that might fail
    async def flaky_operation():
        import random
        if random.random() < 0.7:
            raise TimeoutError("Operation timed out")
        return "Success!"

    # Create error context
    error_context = ErrorContext(
        error=TimeoutError("Initial timeout"),
        agent_id="test_agent",
        task_id="task_123",
        operation="flaky_operation"
    )

    # Attempt recovery
    result = await recovery_system.recover(
        error_context,
        flaky_operation
    )

    print(f"Recovery result: {result}")
    print(f"Error statistics: {recovery_system.get_error_statistics()}")


if __name__ == "__main__":
    asyncio.run(example_usage())
