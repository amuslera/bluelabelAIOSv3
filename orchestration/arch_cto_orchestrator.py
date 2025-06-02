"""
ARCH-CTO Orchestrator - Direct agent orchestration and management system.

This module provides the orchestration framework for managing coding agents
as if they were junior developers reporting to a technical lead (Claude/CTO).
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from agents.base.enhanced_agent import EnhancedTask, EnhancedTaskResult
from agents.base.types import TaskType, Priority
from agents.specialists.backend_agent import BackendDeveloperAgent, create_backend_agent

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task lifecycle status."""
    PLANNED = "planned"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"


class ReviewOutcome(Enum):
    """Code review outcomes."""
    APPROVED = "approved"
    NEEDS_MINOR_CHANGES = "needs_minor_changes"
    NEEDS_MAJOR_CHANGES = "needs_major_changes"
    REJECTED = "rejected"


class TaskAssignment(BaseModel):
    """Task assignment with metadata."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    agent_type: str
    task: EnhancedTask
    status: TaskStatus = TaskStatus.PLANNED
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results and review
    result: Optional[EnhancedTaskResult] = None
    review_notes: List[str] = Field(default_factory=list)
    review_outcome: Optional[ReviewOutcome] = None
    revision_count: int = 0
    
    # Metrics
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None


class CodeReview(BaseModel):
    """Code review result."""
    task_id: str
    reviewer: str = "ARCH-CTO"
    outcome: ReviewOutcome
    summary: str
    detailed_feedback: List[str] = Field(default_factory=list)
    security_issues: List[str] = Field(default_factory=list)
    quality_score: int = Field(ge=1, le=10)  # 1-10 scale
    requires_revision: bool = False
    approval_notes: str = ""
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)


class OrchestrationMetrics(BaseModel):
    """Metrics for orchestration effectiveness."""
    total_tasks: int = 0
    completed_tasks: int = 0
    average_completion_time: float = 0.0
    average_review_cycles: float = 0.0
    agent_performance: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    quality_trends: List[float] = Field(default_factory=list)


class ARCHCTOOrchestrator:
    """
    ARCH-CTO Orchestrator for managing coding agents.
    
    Acts as a technical lead coordinating junior developer agents,
    providing task assignment, code review, and quality control.
    """

    def __init__(self):
        self.orchestrator_id = f"arch_cto_{uuid.uuid4().hex[:8]}"
        self.active_agents: Dict[str, Any] = {}
        self.task_assignments: Dict[str, TaskAssignment] = {}
        self.completed_reviews: List[CodeReview] = []
        self.metrics = OrchestrationMetrics()
        
        # Orchestration configuration
        self.max_revision_cycles = 3
        self.quality_threshold = 7  # Minimum quality score for approval
        self.review_checklist = self._get_review_checklist()

    async def initialize(self):
        """Initialize the orchestrator and prepare agent pool."""
        logger.info("🎯 Initializing ARCH-CTO Orchestrator...")
        
        # Initialize available agents
        # Start with Backend Agent
        backend_agent = await create_backend_agent()
        self.active_agents["backend"] = backend_agent
        
        logger.info(f"✅ ARCH-CTO Orchestrator initialized with {len(self.active_agents)} agents")

    async def assign_task(
        self,
        task_description: str,
        task_type: TaskType,
        agent_type: str = "backend",
        complexity: int = 5,
        priority: Priority = Priority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Assign a task to an appropriate agent.
        
        Args:
            task_description: Detailed task description
            task_type: Type of task (API_DEVELOPMENT, CODE_GENERATION, etc.)
            agent_type: Which agent to assign to ("backend", "frontend", etc.)
            complexity: Task complexity (1-10)
            priority: Task priority
            metadata: Additional task context
            
        Returns:
            task_id: Unique identifier for tracking
        """
        
        # Create enhanced task
        task = EnhancedTask(
            task_type=task_type,
            prompt=task_description,
            complexity=complexity,
            priority=priority,
            metadata=metadata or {}
        )
        
        # Get target agent
        if agent_type not in self.active_agents:
            raise ValueError(f"Agent type '{agent_type}' not available. Active agents: {list(self.active_agents.keys())}")
        
        agent = self.active_agents[agent_type]
        
        # Create assignment
        assignment = TaskAssignment(
            agent_id=agent.agent_id,
            agent_type=agent_type,
            task=task,
            status=TaskStatus.ASSIGNED,
            estimated_hours=self._estimate_task_hours(complexity, task_type)
        )
        
        self.task_assignments[assignment.task_id] = assignment
        self.metrics.total_tasks += 1
        
        logger.info(f"📋 Task assigned to {agent_type} agent: {assignment.task_id}")
        logger.info(f"   Task: {task_description[:100]}...")
        logger.info(f"   Complexity: {complexity}/10, Priority: {priority.value}")
        
        return assignment.task_id

    async def execute_task(self, task_id: str) -> EnhancedTaskResult:
        """
        Execute an assigned task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task execution result
        """
        
        if task_id not in self.task_assignments:
            raise ValueError(f"Task {task_id} not found")
        
        assignment = self.task_assignments[task_id]
        agent = self.active_agents[assignment.agent_type]
        
        # Update status
        assignment.status = TaskStatus.IN_PROGRESS
        assignment.started_at = datetime.utcnow()
        
        logger.info(f"🚀 Executing task {task_id} with {assignment.agent_type} agent...")
        
        try:
            # Execute task
            result = await agent.process_task(assignment.task)
            
            # Update assignment
            assignment.result = result
            assignment.status = TaskStatus.SUBMITTED
            assignment.submitted_at = datetime.utcnow()
            
            if assignment.started_at:
                assignment.actual_hours = (assignment.submitted_at - assignment.started_at).total_seconds() / 3600
            
            logger.info(f"✅ Task {task_id} submitted by {assignment.agent_type} agent")
            logger.info(f"   Success: {result.success}, Cost: ${result.cost:.4f}")
            
            return result
            
        except Exception as e:
            assignment.status = TaskStatus.FAILED
            logger.error(f"❌ Task {task_id} failed: {str(e)}")
            raise

    async def review_task(self, task_id: str) -> CodeReview:
        """
        Review a submitted task as the ARCH-CTO.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Code review result
        """
        
        if task_id not in self.task_assignments:
            raise ValueError(f"Task {task_id} not found")
        
        assignment = self.task_assignments[task_id]
        
        if assignment.status != TaskStatus.SUBMITTED:
            raise ValueError(f"Task {task_id} is not ready for review (status: {assignment.status})")
        
        if not assignment.result:
            raise ValueError(f"Task {task_id} has no result to review")
        
        assignment.status = TaskStatus.UNDER_REVIEW
        
        logger.info(f"🔍 Reviewing task {task_id}...")
        
        # Perform comprehensive code review
        review = await self._perform_code_review(assignment)
        
        # Update assignment based on review
        assignment.review_notes.append(review.summary)
        assignment.review_outcome = review.outcome
        
        if review.requires_revision:
            assignment.status = TaskStatus.NEEDS_REVISION
            assignment.revision_count += 1
            logger.info(f"📝 Task {task_id} needs revision (cycle {assignment.revision_count})")
        else:
            assignment.status = TaskStatus.APPROVED
            assignment.completed_at = datetime.utcnow()
            self.metrics.completed_tasks += 1
            logger.info(f"✅ Task {task_id} approved!")
        
        self.completed_reviews.append(review)
        self.metrics.quality_trends.append(review.quality_score)
        
        return review

    async def request_revision(self, task_id: str, revision_notes: str) -> str:
        """
        Request revisions to a task.
        
        Args:
            task_id: Task identifier
            revision_notes: Specific revision requirements
            
        Returns:
            New task_id for the revision
        """
        
        if task_id not in self.task_assignments:
            raise ValueError(f"Task {task_id} not found")
        
        assignment = self.task_assignments[task_id]
        
        if assignment.revision_count >= self.max_revision_cycles:
            logger.warning(f"⚠️ Task {task_id} exceeded max revision cycles ({self.max_revision_cycles})")
            assignment.status = TaskStatus.FAILED
            return task_id
        
        # Create revision task
        revised_prompt = f"{assignment.task.prompt}\n\nREVISION NOTES:\n{revision_notes}"
        
        revision_task_id = await self.assign_task(
            task_description=revised_prompt,
            task_type=assignment.task.task_type,
            agent_type=assignment.agent_type,
            complexity=assignment.task.complexity,
            priority=assignment.task.priority,
            metadata=assignment.task.metadata
        )
        
        # Link revision to original
        revision_assignment = self.task_assignments[revision_task_id]
        revision_assignment.revision_count = assignment.revision_count
        
        logger.info(f"🔄 Revision requested for task {task_id} -> {revision_task_id}")
        
        return revision_task_id

    async def _perform_code_review(self, assignment: TaskAssignment) -> CodeReview:
        """
        Perform detailed code review of task result.
        
        Args:
            assignment: Task assignment to review
            
        Returns:
            Code review result
        """
        
        result = assignment.result
        if not result or not result.output:
            return CodeReview(
                task_id=assignment.task_id,
                outcome=ReviewOutcome.REJECTED,
                summary="No output provided",
                quality_score=1,
                requires_revision=True
            )
        
        # Analyze the code/output
        feedback = []
        security_issues = []
        quality_score = 10  # Start with perfect score and deduct
        
        output = result.output.lower()
        
        # Check for basic quality indicators
        if "def " not in output and "class " not in output and "async def" not in output:
            feedback.append("No function or class definitions found - may be incomplete implementation")
            quality_score -= 2
        
        # Security checks
        if "password" in output and "hash" not in output:
            security_issues.append("Password handling without proper hashing")
            quality_score -= 3
        
        if "api_key" in output or "secret" in output:
            security_issues.append("Potential hardcoded secrets")
            quality_score -= 2
        
        # Quality checks
        if "try:" not in output and "except" not in output:
            feedback.append("Missing error handling")
            quality_score -= 1
        
        if "test" not in output:
            feedback.append("No tests provided")
            quality_score -= 2
        
        if len(result.output) < 200:
            feedback.append("Output seems too brief for the task complexity")
            quality_score -= 1
        
        # Check for proper structure
        if assignment.task.task_type == TaskType.CODE_GENERATION:
            if "@router" not in output and "@app" not in output:
                feedback.append("Missing FastAPI router or app decorators")
                quality_score -= 2
            
            if "response_model" not in output:
                feedback.append("Missing response model specification")
                quality_score -= 1
        
        # Determine outcome
        requires_revision = quality_score < self.quality_threshold or len(security_issues) > 0
        
        if quality_score >= 9 and not security_issues:
            outcome = ReviewOutcome.APPROVED
        elif quality_score >= 7 and not security_issues:
            outcome = ReviewOutcome.NEEDS_MINOR_CHANGES
        elif quality_score >= 5:
            outcome = ReviewOutcome.NEEDS_MAJOR_CHANGES
        else:
            outcome = ReviewOutcome.REJECTED
        
        summary = self._generate_review_summary(quality_score, feedback, security_issues, outcome)
        
        return CodeReview(
            task_id=assignment.task_id,
            outcome=outcome,
            summary=summary,
            detailed_feedback=feedback,
            security_issues=security_issues,
            quality_score=max(1, quality_score),
            requires_revision=requires_revision,
            approval_notes="" if requires_revision else "Code meets quality standards and is approved for production use."
        )

    def _generate_review_summary(
        self,
        quality_score: int,
        feedback: List[str],
        security_issues: List[str],
        outcome: ReviewOutcome
    ) -> str:
        """Generate human-readable review summary."""
        
        summary_parts = [f"Code quality score: {max(1, quality_score)}/10"]
        
        if security_issues:
            summary_parts.append(f"⚠️ {len(security_issues)} security issue(s) found")
        
        if feedback:
            summary_parts.append(f"📝 {len(feedback)} improvement(s) suggested")
        
        summary_parts.append(f"Decision: {outcome.value.replace('_', ' ').title()}")
        
        return " | ".join(summary_parts)

    def _estimate_task_hours(self, complexity: int, task_type: TaskType) -> float:
        """Estimate task completion time in hours."""
        
        base_hours = {
            TaskType.CODE_GENERATION: 2.0,
            TaskType.SYSTEM_DESIGN: 4.0,
            TaskType.TESTING: 2.5,
        }
        
        base = base_hours.get(task_type, 2.0)
        complexity_multiplier = complexity / 5.0  # Scale complexity to multiplier
        
        return base * complexity_multiplier

    def _get_review_checklist(self) -> List[str]:
        """Get standardized code review checklist."""
        return [
            "Code follows project style guidelines",
            "Proper error handling implemented",
            "Input validation and sanitization",
            "No hardcoded secrets or credentials",
            "Appropriate test coverage",
            "Clear documentation and comments",
            "Security best practices followed",
            "Performance considerations addressed",
            "Database operations are optimized",
            "API responses are consistent"
        ]

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get detailed status of a specific task."""
        
        if task_id not in self.task_assignments:
            return {"error": f"Task {task_id} not found"}
        
        assignment = self.task_assignments[task_id]
        
        status_info = {
            "task_id": task_id,
            "status": assignment.status.value,
            "agent_type": assignment.agent_type,
            "complexity": assignment.task.complexity,
            "assigned_at": assignment.assigned_at.isoformat(),
            "estimated_hours": assignment.estimated_hours,
            "actual_hours": assignment.actual_hours,
            "revision_count": assignment.revision_count,
        }
        
        if assignment.result:
            status_info.update({
                "success": assignment.result.success,
                "cost": assignment.result.cost,
                "model_used": assignment.result.model_used,
                "execution_time": assignment.result.execution_time
            })
        
        if assignment.review_outcome:
            status_info["review_outcome"] = assignment.review_outcome.value
            status_info["review_notes"] = assignment.review_notes
        
        return status_info

    def get_orchestration_metrics(self) -> OrchestrationMetrics:
        """Get comprehensive orchestration metrics."""
        
        # Update metrics
        if self.task_assignments:
            completion_times = [
                (a.completed_at - a.assigned_at).total_seconds() / 3600
                for a in self.task_assignments.values()
                if a.completed_at and a.assigned_at
            ]
            
            if completion_times:
                self.metrics.average_completion_time = sum(completion_times) / len(completion_times)
            
            revision_counts = [a.revision_count for a in self.task_assignments.values()]
            if revision_counts:
                self.metrics.average_review_cycles = sum(revision_counts) / len(revision_counts)
        
        return self.metrics

    async def shutdown(self):
        """Shutdown orchestrator and cleanup resources."""
        logger.info("🔄 Shutting down ARCH-CTO Orchestrator...")
        
        for agent in self.active_agents.values():
            await agent.stop()
        
        logger.info("✅ ARCH-CTO Orchestrator shutdown complete")


# Factory function for easy orchestrator creation
async def create_arch_cto_orchestrator() -> ARCHCTOOrchestrator:
    """Create and initialize ARCH-CTO Orchestrator."""
    orchestrator = ARCHCTOOrchestrator()
    await orchestrator.initialize()
    return orchestrator