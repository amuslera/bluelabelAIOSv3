"""
Task Manager Panel - Manage sprint tasks and assignments
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, DataTable, Button, Label, Select, Input
from textual.screen import ModalScreen


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    
    def get_icon(self) -> str:
        icons = {
            self.PENDING: "⚪",
            self.IN_PROGRESS: "🔵",
            self.COMPLETED: "✅",
            self.BLOCKED: "🔴"
        }
        return icons.get(self, "❓")


@dataclass
class Task:
    """Container for task information."""
    id: str
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[str] = None
    priority: str = "medium"
    
    def get_status_display(self) -> str:
        return f"{self.status.get_icon()} {self.status.value}"


class AssignTaskDialog(ModalScreen):
    """Modal dialog for task assignment."""
    
    def __init__(self, task: Task, agents: List[str], **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.agents = agents
        
    def compose(self) -> ComposeResult:
        """Create the dialog layout."""
        with Vertical(classes="modal-dialog"):
            yield Label(f"Assign Task: {self.task.id}", classes="panel-title")
            yield Static(f"Title: {self.task.title}")
            yield Static(f"Current: {self.task.assigned_to or 'Unassigned'}")
            
            # Agent selection
            yield Label("Select Agent:")
            options = [(agent, agent) for agent in self.agents]
            yield Select(options, id="agent-select")
            
            # Buttons
            with Horizontal():
                yield Button("Assign", variant="success", id="confirm")
                yield Button("Cancel", variant="default", id="cancel")
                
    @on(Button.Pressed, "#confirm")
    def handle_confirm(self):
        """Handle assignment confirmation."""
        select = self.query_one("#agent-select", Select)
        if select.value:
            self.dismiss(select.value)
            
    @on(Button.Pressed, "#cancel")
    def handle_cancel(self):
        """Handle cancellation."""
        self.dismiss(None)


class TaskManagerPanel(Widget):
    """Panel for managing sprint tasks."""
    
    tasks: reactive[Dict[str, Task]] = reactive({})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_agents = ["marcus-001", "alex-001", "sam-001", "jordan-001"]
        
    def compose(self) -> ComposeResult:
        """Create the panel layout."""
        with Vertical():
            yield Label("📋 Task Manager", classes="panel-title")
            
            # Task table
            table = DataTable(classes="task-list")
            table.add_columns("ID", "Title", "Status", "Assigned To")
            table.cursor_type = "row"
            yield table
            
            # Control buttons
            with Horizontal():
                yield Button("Assign Task", id="assign-task", classes="primary-button")
                yield Button("Update Status", id="update-status")
                yield Button("Load Sprint", id="load-sprint")
                
    async def on_mount(self) -> None:
        """Initialize when panel mounts."""
        # Load sprint tasks
        await self.load_sprint_tasks()
        
        # If no tasks, add demo tasks
        if not self.tasks:
            self.add_demo_tasks()
            
    async def load_sprint_tasks(self):
        """Load tasks from sprint plan."""
        sprint_file = Path("SPRINT_1_6_PLAN.md")
        
        if sprint_file.exists():
            # Parse sprint file for tasks
            # Simplified for this implementation
            self.app.log.info(f"Loading tasks from {sprint_file}")
            
        # For now, use hardcoded sprint tasks
        sprint_tasks = [
            Task("MON-001", "Complete WebSocket Monitoring Server", 
                 "Implement full monitoring server with auth", TaskStatus.IN_PROGRESS, "marcus-001"),
            Task("MON-002", "Add Metrics Collection System",
                 "Create Prometheus metrics collector", TaskStatus.PENDING),
            Task("CC-001", "Set up Control Center Structure",
                 "Create base UI structure", TaskStatus.COMPLETED, "alex-001"),
            Task("CC-002", "Implement Agent Orchestra Panel",
                 "Show active agents", TaskStatus.IN_PROGRESS, "alex-001"),
            Task("CC-003", "Implement Activity Monitor",
                 "Real-time activity feed", TaskStatus.IN_PROGRESS, "alex-001"),
            Task("CC-004", "Implement Task Manager",
                 "Task assignment UI", TaskStatus.IN_PROGRESS, "alex-001"),
            Task("CC-005", "Implement PR Review Panel",
                 "PR management interface", TaskStatus.PENDING),
            Task("AI-001", "Implement Error Recovery",
                 "Backend error recovery system", TaskStatus.COMPLETED, "marcus-001"),
        ]
        
        for task in sprint_tasks:
            self.tasks[task.id] = task
            
        self.update_table()
        
    def add_demo_tasks(self):
        """Add demonstration tasks."""
        demo_tasks = [
            Task("DEMO-001", "Example Task 1", "This is a demo task", 
                 TaskStatus.PENDING),
            Task("DEMO-002", "Example Task 2", "Another demo task",
                 TaskStatus.IN_PROGRESS, "marcus-001"),
            Task("DEMO-003", "Example Task 3", "Completed demo task",
                 TaskStatus.COMPLETED, "alex-001"),
        ]
        
        for task in demo_tasks:
            self.tasks[task.id] = task
            
        self.update_table()
        
    def update_table(self):
        """Update the task table display."""
        table = self.query_one(DataTable)
        table.clear()
        
        for task in self.tasks.values():
            # Style based on status
            status_class = f"task-{task.status.value.replace('_', '-')}"
            
            table.add_row(
                task.id,
                task.title[:40] + "..." if len(task.title) > 40 else task.title,
                task.get_status_display(),
                task.assigned_to or "Unassigned"
            )
            
    def refresh(self):
        """Public refresh method."""
        self.update_table()
        
    @on(Button.Pressed, "#assign-task")
    async def handle_assign_task(self):
        """Handle task assignment."""
        table = self.query_one(DataTable)
        
        if table.cursor_row is not None and table.cursor_row < len(self.tasks):
            task = list(self.tasks.values())[table.cursor_row]
            
            # Show assignment dialog
            agent = await self.app.push_screen_wait(
                AssignTaskDialog(task, self.available_agents)
            )
            
            if agent:
                # Update task assignment
                task.assigned_to = agent
                self.update_table()
                
                self.app.notify(
                    f"Task {task.id} assigned to {agent}",
                    severity="success"
                )
                
                # In production, update Redis/backend
                
    @on(Button.Pressed, "#update-status")
    def handle_update_status(self):
        """Handle status update."""
        table = self.query_one(DataTable)
        
        if table.cursor_row is not None and table.cursor_row < len(self.tasks):
            task = list(self.tasks.values())[table.cursor_row]
            
            # Cycle through statuses
            current_idx = list(TaskStatus).index(task.status)
            next_idx = (current_idx + 1) % len(TaskStatus)
            task.status = list(TaskStatus)[next_idx]
            
            self.update_table()
            
            self.app.notify(
                f"Task {task.id} status → {task.status.value}",
                severity="information"
            )
            
    @on(Button.Pressed, "#load-sprint")
    async def handle_load_sprint(self):
        """Handle loading sprint tasks."""
        self.app.notify("Reloading sprint tasks...", severity="information")
        await self.load_sprint_tasks()
        
    @on(DataTable.RowSelected)
    def handle_row_selected(self, event: DataTable.RowSelected):
        """Handle task selection."""
        if event.row_index < len(self.tasks):
            task = list(self.tasks.values())[event.row_index]
            self.app.notify(
                f"Task: {task.id}\n"
                f"Title: {task.title}\n"
                f"Status: {task.status.value}\n"
                f"Assigned: {task.assigned_to or 'Unassigned'}\n"
                f"Description: {task.description}",
                title="Task Details"
            )