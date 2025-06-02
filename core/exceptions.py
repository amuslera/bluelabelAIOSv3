"""
Centralized exception handling for AIOSv3 platform.

Provides consistent error handling patterns, logging, and recovery mechanisms.
"""

import logging
import traceback
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ErrorSeverity(Enum):
    """Error severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""

    CONFIGURATION = "configuration"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    NETWORK = "network"
    DATABASE = "database"
    LLM_PROVIDER = "llm_provider"
    AGENT_COMMUNICATION = "agent_communication"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    TIMEOUT = "timeout"
    EXTERNAL_API = "external_api"
    BUSINESS_LOGIC = "business_logic"
    UNKNOWN = "unknown"


class ErrorContext(BaseModel):
    """Context information for errors."""

    agent_id: str | None = None
    task_id: str | None = None
    conversation_id: str | None = None
    request_id: str | None = None
    user_id: str | None = None
    provider_name: str | None = None
    model_id: str | None = None
    timestamp: str | None = None
    additional_data: dict[str, Any] = Field(default_factory=dict)


class AIOSError(Exception):
    """Base exception for all AIOSv3 errors."""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: ErrorContext | None = None,
        cause: Exception | None = None,
        recoverable: bool = True,
        retry_after: float | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext()
        self.cause = cause
        self.recoverable = recoverable
        self.retry_after = retry_after

        # Capture stack trace
        self.stack_trace = traceback.format_exc()

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for logging/serialization."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "recoverable": self.recoverable,
            "retry_after": self.retry_after,
            "context": self.context.model_dump() if self.context else None,
            "cause": str(self.cause) if self.cause else None,
            "stack_trace": self.stack_trace,
        }

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


# Configuration Errors
class ConfigurationError(AIOSError):
    """Configuration-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.HIGH,
            recoverable=False,
            **kwargs
        )


class MissingConfigurationError(ConfigurationError):
    """Missing required configuration."""
    pass


class InvalidConfigurationError(ConfigurationError):
    """Invalid configuration values."""
    pass


# Authentication & Authorization Errors
class AuthenticationError(AIOSError):
    """Authentication-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            recoverable=False,
            **kwargs
        )


class AuthorizationError(AIOSError):
    """Authorization-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            recoverable=False,
            **kwargs
        )


# Validation Errors
class ValidationError(AIOSError):
    """Data validation errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            recoverable=False,
            **kwargs
        )


# Network & Communication Errors
class NetworkError(AIOSError):
    """Network-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.NETWORK,
            severity=ErrorSeverity.MEDIUM,
            recoverable=True,
            retry_after=5.0,
            **kwargs
        )


class TimeoutError(AIOSError):
    """Timeout-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.TIMEOUT,
            severity=ErrorSeverity.MEDIUM,
            recoverable=True,
            retry_after=10.0,
            **kwargs
        )


# LLM Provider Errors
class LLMProviderError(AIOSError):
    """LLM provider-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.LLM_PROVIDER,
            severity=ErrorSeverity.HIGH,
            recoverable=True,
            retry_after=30.0,
            **kwargs
        )


class ModelNotAvailableError(LLMProviderError):
    """Model not available."""
    pass


class RateLimitError(LLMProviderError):
    """Rate limit exceeded."""

    def __init__(self, message: str, retry_after: float = 60.0, **kwargs):
        super().__init__(
            message,
            retry_after=retry_after,
            **kwargs
        )


class InsufficientCreditsError(LLMProviderError):
    """Insufficient credits/quota."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            recoverable=False,
            **kwargs
        )


# Agent & Task Errors
class AgentError(AIOSError):
    """Agent-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.AGENT_COMMUNICATION,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )


class TaskExecutionError(AgentError):
    """Task execution errors."""
    pass


class AgentCommunicationError(AgentError):
    """Agent communication errors."""
    pass


class AgentNotFoundError(AgentError):
    """Agent not found."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            recoverable=False,
            **kwargs
        )


# Resource Errors
class ResourceError(AIOSError):
    """Resource-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.RESOURCE_EXHAUSTION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class MemoryExhaustionError(ResourceError):
    """Memory exhaustion."""
    pass


class DiskSpaceError(ResourceError):
    """Disk space exhaustion."""
    pass


# Database Errors
class DatabaseError(AIOSError):
    """Database-related errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            recoverable=True,
            retry_after=5.0,
            **kwargs
        )


class ConnectionError(DatabaseError):
    """Database connection errors."""
    pass


# External API Errors
class ExternalAPIError(AIOSError):
    """External API errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.EXTERNAL_API,
            severity=ErrorSeverity.MEDIUM,
            recoverable=True,
            retry_after=10.0,
            **kwargs
        )


# Business Logic Errors
class BusinessLogicError(AIOSError):
    """Business logic errors."""

    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.BUSINESS_LOGIC,
            severity=ErrorSeverity.LOW,
            recoverable=False,
            **kwargs
        )


# Error Handler Class
class ErrorHandler:
    """Centralized error handling and logging."""

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger or logging.getLogger(__name__)
        self.error_counts: dict[str, int] = {}

    def handle_error(
        self,
        error: Exception | AIOSError,
        context: ErrorContext | None = None,
        reraise: bool = True,
    ) -> AIOSError | None:
        """Handle an error with logging and optional re-raising."""

        # Convert to AIOSError if needed
        if isinstance(error, AIOSError):
            aios_error = error
        else:
            aios_error = AIOSError(
                message=str(error),
                cause=error,
                context=context,
            )

        # Update context if provided
        if context:
            aios_error.context = context

        # Log the error
        self._log_error(aios_error)

        # Track error counts
        self._track_error(aios_error)

        # Re-raise if requested
        if reraise:
            raise aios_error

        return aios_error

    def _log_error(self, error: AIOSError) -> None:
        """Log an error with appropriate level."""

        log_data = error.to_dict()

        if error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical("Critical error occurred", extra=log_data)
        elif error.severity == ErrorSeverity.HIGH:
            self.logger.error("High severity error occurred", extra=log_data)
        elif error.severity == ErrorSeverity.MEDIUM:
            self.logger.warning("Medium severity error occurred", extra=log_data)
        else:
            self.logger.info("Low severity error occurred", extra=log_data)

    def _track_error(self, error: AIOSError) -> None:
        """Track error counts for monitoring."""

        key = f"{error.category.value}:{error.error_code}"
        self.error_counts[key] = self.error_counts.get(key, 0) + 1

    def get_error_stats(self) -> dict[str, int]:
        """Get error statistics."""
        return self.error_counts.copy()

    def reset_error_stats(self) -> None:
        """Reset error statistics."""
        self.error_counts.clear()


# Global error handler instance
global_error_handler = ErrorHandler()


def handle_error(
    error: Exception | AIOSError,
    context: ErrorContext | None = None,
    reraise: bool = True,
) -> AIOSError | None:
    """Handle an error using the global error handler."""
    return global_error_handler.handle_error(error, context, reraise)


# Decorator for automatic error handling
def error_handler(
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    recoverable: bool = True,
    reraise: bool = True,
):
    """Decorator for automatic error handling."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AIOSError:
                # Re-raise AIOSError as-is
                raise
            except Exception as e:
                # Convert to AIOSError
                aios_error = AIOSError(
                    message=f"Error in {func.__name__}: {str(e)}",
                    category=category,
                    severity=severity,
                    recoverable=recoverable,
                    cause=e,
                )
                return handle_error(aios_error, reraise=reraise)

        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except AIOSError:
                # Re-raise AIOSError as-is
                raise
            except Exception as e:
                # Convert to AIOSError
                aios_error = AIOSError(
                    message=f"Error in {func.__name__}: {str(e)}",
                    category=category,
                    severity=severity,
                    recoverable=recoverable,
                    cause=e,
                )
                return handle_error(aios_error, reraise=reraise)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    return decorator


# Circuit breaker for resilient error handling
class CircuitBreaker:
    """Circuit breaker pattern for error resilience."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection."""

        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise AIOSError(
                    "Circuit breaker is open",
                    category=ErrorCategory.RESOURCE_EXHAUSTION,
                    severity=ErrorSeverity.HIGH,
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker."""
        import time
        return (
            self.last_failure_time is not None and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )

    def _on_success(self) -> None:
        """Handle successful call."""
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self) -> None:
        """Handle failed call."""
        import time
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
