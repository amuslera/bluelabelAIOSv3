"""Theatrical Monitoring Module for AIOSv3.

This module provides real-time visualization and monitoring of multi-agent orchestration.
"""

from .theatrical_orchestrator import TheatricalOrchestrator, demo_theatrical_orchestration
from .theatrical_monitoring_dashboard import TheatricalMonitoringApp

__all__ = [
    "TheatricalOrchestrator",
    "demo_theatrical_orchestration",
    "TheatricalMonitoringApp",
]