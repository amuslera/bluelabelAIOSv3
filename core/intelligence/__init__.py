"""
Intelligence Components for AIOSv3

Provides intelligent capabilities including error recovery,
learning systems, and decision-making components.
"""

from .error_recovery import (
    ErrorContext,
    ErrorPattern,
    ErrorRecoverySystem,
    ErrorSeverity,
    RecoveryResult,
    RecoveryStrategy,
)

__all__ = [
    'ErrorRecoverySystem',
    'ErrorPattern',
    'ErrorContext',
    'RecoveryResult',
    'ErrorSeverity',
    'RecoveryStrategy'
]
