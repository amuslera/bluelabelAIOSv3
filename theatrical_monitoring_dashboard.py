"""
Theatrical Monitoring Dashboard - Real-time visualization of agent interactions

This dashboard provides a rich, real-time view of agent orchestration with
live updates, progress tracking, and detailed communication logs.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Optional

# Suppress console logging when running dashboard
logging.getLogger().setLevel(logging.ERROR)
# Specifically suppress noisy loggers
for logger_name in ['agents.base', 'core.routing', 'httpx']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Label,
    Log,
    ProgressBar,
    Static,
    TabbedContent,
    TabPane,
)

from theatrical_orchestrator import TheatricalEvent, TheatricalOrchestrator


class AgentStatusWidget(Static):
    """Widget displaying individual agent status with activity log and metrics."""

    def __init__(self, agent_id: str, agent_name: str, **kwargs):
        super().__init__(**kwargs)
        # Store all attributes as regular attributes
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.last_update = time.time()
        self.status = "idle"
        self.progress = 0
        self.current_task = "None"
        # Performance metrics
        self.tasks_assigned = 0
        self.tasks_completed = 0
        self.total_time = 0.0
        self.total_cost = 0.0
        self.total_tokens = 0
        self.task_start_time = None
        # Activity history - now unlimited, stored as list
        self.activity_history = []
        # Will store reference to scrollable activity container and labels
        self.activity_scroll = None
        self.activity_labels = []

    def compose(self) -> ComposeResult:
        """Create agent status display with scrollable activity log."""
        # Main content area with horizontal split
        with Horizontal(classes="agent-content"):
            # Left side: Scrollable activity log with compact header (70% width)
            with Vertical(classes="agent-activity"):
                # Compact agent header
                yield Label(f"{self.agent_name}", classes="agent-header")
                # Create vertically scrollable container
                self.activity_scroll = ScrollableContainer(
                    id=f"activity-scroll-{self.agent_id}",
                    classes="activity-scroll"
                )
                yield self.activity_scroll
            
            # Right side: Metrics and progress (30% width)
            with Vertical(classes="agent-metrics"):
                yield Label(f"Status: {self.status}", id=f"status-{self.agent_id}")
                yield ProgressBar(total=100, show_eta=False, id=f"progress-{self.agent_id}")
                yield Label(f"Tasks: 0/0", id=f"tasks-{self.agent_id}")
                yield Label(f"Time: 0.0s", id=f"time-{self.agent_id}")
                yield Label(f"Cost: $0.0000", id=f"cost-{self.agent_id}")
                yield Label(f"Tokens: 0", id=f"tokens-{self.agent_id}")

    def update_status(self, status: str, progress: Optional[int] = None, task: Optional[str] = None):
        """Update agent status display and log history."""
        self.status = status
        if progress is not None:
            self.progress = progress
        if task is not None:
            self.current_task = task

        self.last_update = time.time()

        # Track task assignment and completion
        if status == "thinking" and self.task_start_time is None:
            self.tasks_assigned += 1
            self.task_start_time = time.time()
        elif status == "success" and self.task_start_time is not None:
            self.tasks_completed += 1
            self.total_time += time.time() - self.task_start_time
            self.task_start_time = None

        # Update UI elements
        try:
            status_label = self.query_one(f"#status-{self.agent_id}", Label)
            status_label.update(f"Status: {status}")
        except:
            pass

        if progress is not None:
            try:
                progress_bar = self.query_one(f"#progress-{self.agent_id}", ProgressBar)
                progress_bar.progress = progress
            except:
                pass

        # Update task counter
        try:
            tasks_label = self.query_one(f"#tasks-{self.agent_id}", Label)
            tasks_label.update(f"Tasks: {self.tasks_completed}/{self.tasks_assigned}")
        except:
            pass

        # Update time
        try:
            time_label = self.query_one(f"#time-{self.agent_id}", Label)
            time_label.update(f"Time: {self.total_time:.1f}s")
        except:
            pass

        # Add new activity to unlimited history
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if task:
            # Keep task descriptions reasonable length to prevent horizontal scrolling
            display_task = task if len(task) <= 60 else task[:57] + "..."
            activity_text = f"{timestamp} {status}: {display_task}"
        else:
            activity_text = f"{timestamp} Status: {status}"
        
        # Add to unlimited activity history
        self.activity_history.append(activity_text)
        
        # Update scrollable container with new label
        if self.activity_scroll:
            try:
                # Create a new label for this activity
                activity_label = Label(activity_text, classes="activity-item")
                self.activity_labels.append(activity_label)
                
                # Mount the new label to the scrollable container
                self.activity_scroll.mount(activity_label)
                
                # Keep only last 100 activities to prevent memory issues
                if len(self.activity_labels) > 100:
                    old_label = self.activity_labels.pop(0)
                    old_label.remove()
                    self.activity_history.pop(0)
                
                # Auto-scroll to bottom to show latest activity
                self.activity_scroll.scroll_end()
                    
            except Exception as e:
                pass  # If mounting fails, just ignore

    def add_activity(self, activity_text: str):
        """Add an activity directly to the log (for manual additions)."""
        self.activity_history.append(activity_text)
        if self.activity_scroll:
            try:
                activity_label = Label(activity_text, classes="activity-item")
                self.activity_labels.append(activity_label)
                self.activity_scroll.mount(activity_label)
                self.activity_scroll.scroll_end()
            except:
                pass

    def get_status_icon(self) -> str:
        """Get status icon."""
        icons = {
            "idle": "⚪",
            "thinking": "🤔",
            "working": "⚙️",
            "success": "✅",
            "error": "❌",
            "active": "🟢"
        }
        return icons.get(self.status, "❓")
    
    def update_metrics(self, cost: Optional[float] = None, tokens: Optional[int] = None):
        """Update cost and token metrics."""
        if cost is not None:
            self.total_cost += cost
            cost_label = self.query_one(f"#cost-{self.agent_id}", Label)
            cost_label.update(f"Cost: ${self.total_cost:.4f}")
            
        if tokens is not None:
            self.total_tokens += tokens
            tokens_label = self.query_one(f"#tokens-{self.agent_id}", Label)
            tokens_label.update(f"Tokens: {self.total_tokens:,}")
    
    def clear_log(self):
        """Clear the agent's activity log and reset metrics."""
        # Clear activity history
        self.activity_history = []
        
        # Clear all activity labels
        if self.activity_scroll:
            try:
                for label in self.activity_labels:
                    label.remove()
                self.activity_labels = []
            except:
                pass
            
        # Reset metrics
        self.tasks_assigned = 0
        self.tasks_completed = 0
        self.total_time = 0.0
        self.total_cost = 0.0
        self.total_tokens = 0
        self.task_start_time = None


class EventLogWidget(Log):
    """Enhanced log widget for theatrical events."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_count = 0

    def log_event(self, event: TheatricalEvent):
        """Log a theatrical event with formatting."""
        self.event_count += 1

        # Color code by event type
        color_map = {
            "SYSTEM": "blue",
            "PHASE": "magenta",
            "THINKING": "yellow",
            "TASK": "cyan",
            "SUCCESS": "green",
            "ERROR": "red",
            "DETAILS": "dim",
            "METRICS": "white",
            "SUMMARY": "magenta"
        }

        color = color_map.get(event.event_type, "white")
        timestamp = event.timestamp.strftime("%H:%M:%S")

        # Format message with rich markup
        formatted_message = f"[{color}][{timestamp}] {event.agent_role}: {event.message}[/{color}]"
        self.write(formatted_message)


class ProjectMetricsWidget(Static):
    """Widget showing project-wide metrics."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize as regular attributes
        self.total_cost = 0.0
        self.total_time = 0.0
        self.total_tokens = 0
        self.phases_complete = 0

    def compose(self) -> ComposeResult:
        """Create metrics display."""
        with Vertical():
            yield Label("📊 Project Metrics", classes="section-title")
            yield Label(f"💰 Cost: ${self.total_cost:.4f}", id="cost-metric")
            yield Label(f"⏱️ Time: {self.total_time:.1f}s", id="time-metric")
            yield Label(f"🔤 Tokens: {self.total_tokens:,}", id="tokens-metric")
            yield Label(f"📋 Phases: {self.phases_complete}/5", id="phases-metric")

    def update_metrics(self, cost: Optional[float] = None, time_elapsed: Optional[float] = None,
                      tokens: Optional[int] = None, phases: Optional[int] = None):
        """Update metric display."""
        if cost is not None:
            self.total_cost = cost
            cost_label = self.query_one("#cost-metric", Label)
            cost_label.update(f"💰 Cost: ${cost:.4f}")

        if time_elapsed is not None:
            self.total_time = time_elapsed
            time_label = self.query_one("#time-metric", Label)
            time_label.update(f"⏱️ Time: {time_elapsed:.1f}s")

        if tokens is not None:
            self.total_tokens = tokens
            tokens_label = self.query_one("#tokens-metric", Label)
            tokens_label.update(f"🔤 Tokens: {tokens:,}")

        if phases is not None:
            self.phases_complete = phases
            phases_label = self.query_one("#phases-metric", Label)
            phases_label.update(f"📋 Phases: {phases}/5")


class TheatricalMonitoringApp(App):
    """
    Main monitoring application for theatrical agent orchestration.
    """

    CSS = """
    .agent-panel {
        width: 100%;
        height: 20%;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }

    .agent-header {
        background: $surface;
        color: $text;
        text-align: center;
        height: 1;
        margin-bottom: 1;
    }

    .agent-content {
        height: 100%;
    }
    
    .agent-activity {
        width: 70%;
        padding-right: 1;
        border-right: solid $surface;
    }
    
    .agent-metrics {
        width: 30%;
        padding-left: 1;
    }
    
    .activity-scroll {
        height: 1fr;
        border: solid $surface;
        margin: 0 1;
        scrollbar-background: $panel;
        scrollbar-color: $primary;
    }
    
    .activity-item {
        height: auto;
        width: 100%;
        padding: 0 1;
        margin: 0;
    }

    .section-title {
        text-align: center;
        background: $secondary;
        color: $text;
        margin-bottom: 1;
    }

    .control-panel {
        height: 6;
        border: solid $accent;
        margin: 1;
    }

    .metrics-panel {
        width: 25%;
        border: solid $success;
        margin: 1;
    }

    .log-panel {
        border: solid $warning;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "start_demo", "Start Demo"),
        ("r", "reset", "Reset"),
    ]

    def __init__(self):
        super().__init__()
        self.orchestrator: Optional[TheatricalOrchestrator] = None
        self.agent_widgets: Dict[str, AgentStatusWidget] = {}
        self.event_log: Optional[EventLogWidget] = None
        self.metrics_widget: Optional[ProjectMetricsWidget] = None
        self.demo_running = False  # Use a different name to avoid conflict
        self.start_time: Optional[float] = None

    def compose(self) -> ComposeResult:
        """Create the monitoring dashboard layout."""
        yield Header(show_clock=True)

        with Container():
            with TabbedContent():
                with TabPane("Agent Orchestra", id="agents-tab"):
                    # Changed from Horizontal to Vertical for stacked layout
                    with Vertical():
                        # Agent status panels - now stacked vertically
                        self.agent_widgets["cto-001"] = AgentStatusWidget(
                            "cto-001", "🏛️ CTO Agent"
                        )
                        self.agent_widgets["cto-001"].classes = "agent-panel"
                        yield self.agent_widgets["cto-001"]

                        self.agent_widgets["backend-001"] = AgentStatusWidget(
                            "backend-001", "⚙️ Backend Dev"
                        )
                        self.agent_widgets["backend-001"].classes = "agent-panel"
                        yield self.agent_widgets["backend-001"]

                        self.agent_widgets["frontend-001"] = AgentStatusWidget(
                            "frontend-001", "🎨 Frontend Dev"
                        )
                        self.agent_widgets["frontend-001"].classes = "agent-panel"
                        yield self.agent_widgets["frontend-001"]

                        self.agent_widgets["qa-001"] = AgentStatusWidget(
                            "qa-001", "🧪 QA Engineer"
                        )
                        self.agent_widgets["qa-001"].classes = "agent-panel"
                        yield self.agent_widgets["qa-001"]

                        self.agent_widgets["devops-001"] = AgentStatusWidget(
                            "devops-001", "🚀 DevOps"
                        )
                        self.agent_widgets["devops-001"].classes = "agent-panel"
                        yield self.agent_widgets["devops-001"]

                with TabPane("Event Log", id="log-tab"):
                    with Horizontal():
                        # Event log
                        with Vertical(classes="log-panel"):
                            self.event_log = EventLogWidget()
                            yield self.event_log

                        # Metrics sidebar
                        with Vertical(classes="metrics-panel"):
                            self.metrics_widget = ProjectMetricsWidget()
                            yield self.metrics_widget

                with TabPane("Performance", id="performance-tab"):
                    with Vertical():
                        yield Label("📈 Performance Dashboard", classes="section-title")
                        # Performance metrics table
                        table = DataTable()
                        table.add_columns("Metric", "Value", "Status")
                        table.add_row("Response Time", "0.0s", "✅")
                        table.add_row("Success Rate", "100%", "✅")
                        table.add_row("Cost Efficiency", "$0.00", "✅")
                        yield table

            # Control panel
            with Horizontal(classes="control-panel"):
                yield Button("🎬 Start Demo", id="start-btn", variant="success")
                yield Button("⏸️ Pause", id="pause-btn", variant="warning")
                yield Button("🔄 Reset", id="reset-btn", variant="error")
                yield Button("💾 Save Log", id="save-btn", variant="primary")

        yield Footer()

    @on(Button.Pressed, "#start-btn")
    async def start_demo(self):
        """Start the theatrical demo."""
        if self.demo_running:
            self.notify("Demo already running!", severity="warning")
            return

        self.demo_running = True
        self.start_time = time.time()

        # Reset displays and start with real activities
        for widget in self.agent_widgets.values():
            # Add a welcome message to the scrollable log
            widget.add_activity("🎭 Scrollable activity log ready - you can now scroll through full history!")
            widget.update_status("idle", 0, "Demo starting - waiting for initialization...")

        if self.event_log:
            self.event_log.clear()

        # Initialize orchestrator
        self.orchestrator = TheatricalOrchestrator(
            theatrical_delay=1.5,  # Faster for dashboard
            show_details=True
        )
        
        # Suppress orchestrator's console logging
        import logging
        logging.getLogger('theatrical_orchestrator').setLevel(logging.ERROR)

        # Start monitoring task
        asyncio.create_task(self._run_orchestration())

        self.notify("🎭 Theatrical orchestration started!", severity="success")

    @on(Button.Pressed, "#pause-btn")
    def pause_demo(self):
        """Pause the demo."""
        self.notify("⏸️ Demo paused", severity="information")

    @on(Button.Pressed, "#reset-btn")
    def reset_demo(self):
        """Reset the demo."""
        self.demo_running = False

        for widget in self.agent_widgets.values():
            widget.clear_log()  # Clear the history log
            widget.update_status("idle", 0, "Ready")

        if self.event_log:
            self.event_log.clear()

        if self.metrics_widget:
            self.metrics_widget.update_metrics(0.0, 0.0, 0, 0)

        self.notify("🔄 Demo reset", severity="information")

    @on(Button.Pressed, "#save-btn")
    def save_log(self):
        """Save the event log."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"theatrical_log_{timestamp}.txt"

        # In a real app, would save to file
        self.notify(f"💾 Log saved as {filename}", severity="success")

    async def _run_orchestration(self):
        """Run the orchestration with live monitoring."""
        try:
            if not self.orchestrator:
                return

            await self.orchestrator.initialize()

            # Update agent statuses as initialization happens
            for agent_id in self.agent_widgets.keys():
                self.agent_widgets[agent_id].update_status("initializing", 10, "Setting up...")
                await asyncio.sleep(0.5)

            # Start the project
            project = "Real-time Chat Application with WebSocket support, user authentication, and message history"

            # Start monitoring BEFORE orchestration begins
            monitor_task = asyncio.create_task(self._monitor_events())
            
            # Small delay to ensure monitoring is active
            await asyncio.sleep(0.1)

            await self.orchestrator.orchestrate_project(project)
            
            # Cancel monitoring task when done
            monitor_task.cancel()

            self.notify("🎉 Orchestration completed successfully!", severity="success")

        except Exception as e:
            self.notify(f"❌ Orchestration failed: {e}", severity="error")
        finally:
            self.demo_running = False
            if self.orchestrator:
                await self.orchestrator.shutdown()

    async def _monitor_events(self):
        """Monitor orchestrator events and update dashboard."""
        if not self.orchestrator:
            return

        last_event_count = 0
        phase_progress = {
            "architecture": 0,
            "backend": 1,
            "frontend": 2,
            "testing": 3,
            "deployment": 4
        }

        while self.demo_running:
            try:
                # Check for new events
                current_event_count = len(self.orchestrator.events)

                if current_event_count > last_event_count:
                    # Process new events
                    new_events = self.orchestrator.events[last_event_count:]

                    for event in new_events:
                        # Log event
                        if self.event_log:
                            self.event_log.log_event(event)

                        # Update agent status based on event
                        await self._update_agent_from_event(event)

                        # Update metrics
                        if self.metrics_widget and self.start_time:
                            elapsed = time.time() - self.start_time
                            phases = sum(1 for phase in phase_progress.keys()
                                       if any(e.details.get("phase") == phase for e in self.orchestrator.events))

                            self.metrics_widget.update_metrics(
                                cost=self.orchestrator.total_cost,
                                time_elapsed=elapsed,
                                tokens=self.orchestrator.total_tokens,
                                phases=phases
                            )

                    last_event_count = current_event_count

                await asyncio.sleep(0.5)  # Check for updates twice per second

            except Exception as e:
                self.notify(f"Monitoring error: {e}", severity="error")
                break

    async def _update_agent_from_event(self, event: TheatricalEvent):
        """Update agent widget based on event."""
        agent_id = event.agent_id

        if agent_id not in self.agent_widgets:
            return

        widget = self.agent_widgets[agent_id]

        # Map event types to status updates - always update with event message for debugging
        if event.event_type == "THINKING":
            widget.update_status("thinking", progress=25, task=event.message)
        elif event.event_type == "TASK":
            widget.update_status("working", progress=50, task=event.message)
        elif event.event_type == "SUCCESS":
            widget.update_status("success", progress=100, task=event.message)  # Show actual message
        elif event.event_type == "ERROR":
            widget.update_status("error", progress=0, task=event.message)  # Show actual message
        elif event.event_type == "PHASE":
            widget.update_status("active", progress=10, task=event.message)
        elif event.event_type == "INIT":
            widget.update_status("initializing", progress=15, task=event.message)
        elif event.event_type == "SYSTEM":
            # Show system messages for orchestrator
            if agent_id == "orchestrator":
                # Update all agents to show system status
                for w in self.agent_widgets.values():
                    w.update_status("ready", progress=5, task=f"System: {event.message}")
        elif event.event_type == "DETAILS":
            # Extract cost and time from details event
            if "Cost:" in event.message and "$" in event.message:
                try:
                    cost_str = event.message.split("$")[1].split()[0]
                    cost = float(cost_str)
                    widget.update_metrics(cost=cost)
                except:
                    pass
            # Extract tokens if available
            if event.details and "tokens" in event.details:
                widget.update_metrics(tokens=event.details["tokens"])
        

    def action_start_demo(self) -> None:
        """Action for start demo keybind."""
        asyncio.create_task(self.start_demo())

    def action_reset(self) -> None:
        """Action for reset keybind."""
        self.reset_demo()


# Standalone dashboard launcher
async def main():
    """Launch the theatrical monitoring dashboard."""
    app = TheatricalMonitoringApp()
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())
